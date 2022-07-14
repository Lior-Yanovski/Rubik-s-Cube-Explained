import struct

import numpy as np
import zengl

from window import Window


def quatmul(A, B):
    ax, ay, az, aw = A.T
    bx, by, bz, bw = B.T
    return np.array([
        ax * bw + ay * bz - az * by + aw * bx,
        -ax * bz + ay * bw + az * bx + aw * by,
        ax * by - ay * bx + az * bw + aw * bz,
        -ax * bx - ay * by - az * bz + aw * bw,
    ]).T


def rotate(A, B):
    return B + np.cross(np.cross(B, A[:, :3]) - B * A[:, [3, 3, 3]], A[:, :3]) * 2.0


class Cube:
    def __init__(self):
        self.state = np.frombuffer(bytearray(open('assets/state.bin', 'rb').read()), 'f4')
        self.positions = self.state[0:108].reshape(27, 4)[:, :3]
        self.rotations = self.state[108:216].reshape(27, 4)
        self.colors = self.state[216:972].reshape(27, 7, 4)

    def rotate(self, layer, angle):
        subset = np.arange(27)[np.round(rotate(self.rotations, self.positions) + 1.0)[:, layer // 3] == layer % 3]
        quat = np.array([0.0, 0.0, 0.0, np.cos(angle / 2.0)])
        quat[layer // 3] = np.sin(angle / 2.0)
        self.rotations[subset] = quatmul(quat, self.rotations[subset])


class Preview:
    def __init__(self):
        self.window = Window(1280, 720)
        self.ctx = zengl.context()

        self.image = self.ctx.image(self.window.size, 'rgba8unorm-srgb', samples=4)
        self.depth = self.ctx.image(self.window.size, 'depth24plus', samples=4)
        self.image.clear_value = (0.03, 0.03, 0.03, 1.0)

        self.vertex_buffer = self.ctx.buffer(open('assets/cube.bin', 'rb').read())
        self.state_buffer = self.ctx.buffer(size=3888)
        self.uniform_buffer = self.ctx.buffer(size=80)

        self.ctx.includes['common'] = '''
            layout (std140) uniform Common {
                mat4 mvp;
                vec4 eye;
            };
        '''

        self.ctx.includes['qtransform'] = '''
            vec3 qtransform(vec4 q, vec3 v) {
                return v + 2.0 * cross(cross(v, q.xyz) - q.w * v, q.xyz);
            }
        '''

        self.pipeline = self.ctx.pipeline(
            vertex_shader='''
                #version 330

                #include "common"
                #include "qtransform"

                layout (std140) uniform State {
                    vec4 positions[27];
                    vec4 rotations[27];
                    vec4 colors[189];
                };

                layout (location = 0) in vec3 in_vertex;
                layout (location = 1) in vec3 in_normal;
                layout (location = 2) in int in_color;

                out vec3 v_vertex;
                out vec3 v_normal;
                out vec3 v_color;

                void main() {
                    vec3 vertex = in_vertex * positions[gl_InstanceID].w + positions[gl_InstanceID].xyz;
                    v_vertex = qtransform(rotations[gl_InstanceID], vertex);
                    v_normal = qtransform(rotations[gl_InstanceID], in_normal);
                    v_color = colors[gl_InstanceID * 7 + in_color].rgb;
                    gl_Position = mvp * vec4(v_vertex, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330

                #include "common"

                in vec3 v_vertex;
                in vec3 v_normal;
                in vec3 v_color;

                layout (location = 0) out vec4 out_color;

                void main() {
                    float lum = dot(normalize(eye.xyz - v_vertex), normalize(v_normal)) * 0.7 + 0.3;
                    out_color = vec4(v_color * lum, 1.0);
                }
            ''',
            layout=[
                {
                    'name': 'Common',
                    'binding': 0,
                },
                {
                    'name': 'State',
                    'binding': 1,
                },
            ],
            resources=[
                {
                    'type': 'uniform_buffer',
                    'binding': 0,
                    'buffer': self.uniform_buffer,
                },
                {
                    'type': 'uniform_buffer',
                    'binding': 1,
                    'buffer': self.state_buffer,
                },
            ],
            framebuffer=[self.image, self.depth],
            topology='triangles',
            cull_face='back',
            vertex_buffers=zengl.bind(self.vertex_buffer, '3f 3f 1i', 0, 1, 2),
            vertex_count=self.vertex_buffer.size // zengl.calcsize('3f 3f 1i'),
            instance_count=27,
        )

        self.backfaces = self.ctx.pipeline(
            vertex_shader='''
                #version 330

                #include "common"
                #include "qtransform"

                layout (std140) uniform State {
                    vec4 positions[27];
                    vec4 rotations[27];
                    vec4 colors[189];
                };

                layout (location = 0) in vec3 in_vertex;
                layout (location = 1) in vec3 in_normal;
                layout (location = 2) in int in_color;

                out vec3 v_vertex;
                out vec3 v_normal;
                out vec3 v_color;

                void main() {
                    vec3 vertex = in_vertex * positions[gl_InstanceID].w + positions[gl_InstanceID].xyz;
                    v_vertex = qtransform(rotations[gl_InstanceID], vertex);
                    v_normal = qtransform(rotations[gl_InstanceID], in_normal);
                    v_color = colors[gl_InstanceID * 7 + in_color].rgb;
                    gl_Position = mvp * vec4(v_vertex, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330

                #include "common"

                in vec3 v_vertex;
                in vec3 v_normal;
                in vec3 v_color;

                layout (location = 0) out vec4 out_color;

                void main() {
                    if (v_color.r < 0.2 && v_color.g < 0.2 && v_color.b < 0.2) {
                        discard;
                    }
                    float lum = dot(normalize(eye.xyz - v_vertex), normalize(-v_normal)) * 0.7 + 0.3;
                    out_color = vec4(v_color * lum, 0.05);
                }
            ''',
            layout=[
                {
                    'name': 'Common',
                    'binding': 0,
                },
                {
                    'name': 'State',
                    'binding': 1,
                },
            ],
            resources=[
                {
                    'type': 'uniform_buffer',
                    'binding': 0,
                    'buffer': self.uniform_buffer,
                },
                {
                    'type': 'uniform_buffer',
                    'binding': 1,
                    'buffer': self.state_buffer,
                },
            ],
            blending={
                'enable': True,
                'src_color': 'src_alpha',
                'dst_color': 'one_minus_src_alpha',
            },
            framebuffer=[self.image],
            topology='triangles',
            cull_face='front',
            vertex_buffers=zengl.bind(self.vertex_buffer, '3f 3f 1i', 0, 1, 2),
            vertex_count=self.vertex_buffer.size // zengl.calcsize('3f 3f 1i'),
            instance_count=27,
        )

    def set_camera(self, eye, target=(0.0, 0.0, 0.0)):
        camera = zengl.camera(eye, target, aspect=self.window.aspect, fov=45.0)
        self.uniform_buffer.write(struct.pack('64s3f4x', camera, *eye))

    def show(self, state, transparent=False):
        self.state_buffer.write(state)
        self.image.clear()
        self.depth.clear()
        self.pipeline.render()
        if transparent:
            self.backfaces.render()
        self.image.blit()
        if not self.window.update():
            exit()
