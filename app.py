'''
Buffer setup template suggested on mgl official repo : https://github.com/moderngl/moderngl/blob/master/examples/compute_shader_ssbo.py
'''
import weakref
import numpy as np
import os
import moderngl_window as mglw
from moderngl_window import Timer
from PySide2.QtGui import QIcon

from settings_widget import *
from helpers import *
from config import *

# Load glsl code
items_vertex_shader_code = source(os.path.join(SHADER_DIRPATH, "items_vertex.glsl"))
# Geometry shader turning the points into triangle strips.
# This can also be done with point sprites.
items_geo_shader = source(os.path.join(SHADER_DIRPATH, "items_geo.glsl"))
items_fragment_shader_code = source(os.path.join(SHADER_DIRPATH, "items_fragment.glsl"))
compute_worker_shader_code = source(os.path.join(SHADER_DIRPATH, "boids.glsl"))

class CustomComputeShaderSSBO(mglw.WindowConfig):
    title = "Boids Compute Shader SSBO"
    gl_version = 4, 3  # Required opengl version
    window_size = 600, 600  # Initial window size
    aspect_ratio = 1.0  # Force viewport aspect ratio (regardless of window size)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.COUNT = 256  # number of balls
        self.STRUCT_SIZE = 12  # number of floats per item/ball

        # Program for drawing the balls / items
        self.program = self.ctx.program(
            vertex_shader=items_vertex_shader_code,
            geometry_shader=items_geo_shader,
            fragment_shader=items_fragment_shader_code
        )

        # Load compute shader
        compute_shader_code_parsed = compute_worker_shader_code.replace("%COMPUTE_SIZE%", str(self.COUNT))
        self.compute_shader = self.ctx.compute_shader(compute_shader_code_parsed)

        # Create the two buffers the compute shader will write and read from
        compute_data = np.fromiter(gen_initial_data(self.COUNT), dtype="f4")
        self.compute_buffer_a = self.ctx.buffer(compute_data)
        self.compute_buffer_b = self.ctx.buffer(compute_data)
        self.compute_shader['coef_r1']=0
        self.compute_shader['coef_r2']=0
        self.compute_shader['coef_r3']=0

        # Prepare vertex arrays to drawing balls using the compute shader buffers are input
        # We use 4x4 (padding format) to skip the velocity data (not needed for drawing the balls)
        self.balls_a = self.ctx.vertex_array(
            self.program, [(self.compute_buffer_a, '4f 4x4 4f', 'in_vert', 'in_col')],
        )
        self.balls_b = self.ctx.vertex_array(
            self.program, [(self.compute_buffer_b, '4f 4x4 4f', 'in_vert', 'in_col')],
        )

    def render(self, time, frame_time):
        # Calculate the next position of the balls with compute shader
        self.compute_buffer_a.bind_to_storage_buffer(0)
        self.compute_buffer_b.bind_to_storage_buffer(1)
        self.compute_shader.run(group_x=self.STRUCT_SIZE)

        # Batch draw the balls
        self.balls_b.render(mode=self.ctx.POINTS)

        # Swap the buffers and vertex arrays around for next frame
        self.compute_buffer_a, self.compute_buffer_b = self.compute_buffer_b, self.compute_buffer_a
        self.balls_a, self.balls_b = self.balls_b, self.balls_a

    @classmethod
    def run(cls):
        window_str = 'moderngl_window.context.pyside2.Window'
        window_cls = mglw.get_window_cls(window_str)

        # Calculate window size
        size = cls.window_size

        # Resolve cursor
        show_cursor = cls.cursor

        window = window_cls(
            title=cls.title,
            size=size,
            fullscreen=cls.fullscreen,
            resizable=cls.resizable,
            gl_version=cls.gl_version,
            aspect_ratio=cls.aspect_ratio,
            vsync=cls.vsync,
            samples=cls.samples,
            cursor=show_cursor if show_cursor is not None else True,
        )
        window.print_context_info()
        mglw.activate_context(window=window)
        timer = Timer()
        config = cls(ctx=window.ctx, wnd=window, timer=timer)
        # Avoid the event assigning in the property setter for now
        # We want the even assigning to happen in WindowConfig.__init__
        # so users are free to assign them in their own __init__.
        window._config = weakref.ref(config)

        window._widget.setWindowIcon(QIcon(os.path.join(IMG_DIRPATH, "better_ob_icon.png")))
        # Swap buffers once before staring the main loop.
        # This can trigged additional resize events reporting
        # a more accurate buffer size
        window.swap_buffers()
        window.set_default_viewport()

        simSettings = SimSettings()
        compute_data = np.fromiter(gen_initial_data(config.COUNT), dtype="f4")

        timer.start()

        while not window.is_closing:
            current_time, delta = timer.next_frame()
            simSettings.show()
            config.compute_shader['coef_r1']=simSettings.getSettingValue(0)
            config.compute_shader['coef_r2']=simSettings.getSettingValue(1)
            config.compute_shader['coef_r3']=simSettings.getSettingValue(2)

            if (simSettings.resetHasBeenClicked):
                simSettings.resetHasBeenClicked = False 
                config.compute_buffer_a.write(compute_data)
                config.compute_buffer_b.write(compute_data)

            if config.clear_color is not None:
                window.clear(*config.clear_color)

            # Always bind the window framebuffer before calling render
            window.use()
            try :
                fps = 1/delta 
            except:
                fps = 1
            window._widget.setWindowTitle(f'{fps:.2f}' + " FPS")
            window.render(current_time, delta)
            if not window.is_closing:
                window.swap_buffers()

        _, duration = timer.stop()
        window.destroy()


if __name__ == "__main__":
    CustomComputeShaderSSBO.run()