import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

class Visualization:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.visualization_active = False
        self.animation = None

    def create_3d_visualization(self):
        if self.visualization_active:
            return

        self.visualization_active = True
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111, projection='3d')

        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))

        self.sphere = self.ax.plot_surface(
            x, y, z,
            facecolors=self.calculate_rgb_colors(x, y, z),
            rstride=4, cstride=4, shade=False
        )
        self.ax.set_axis_off()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True, fill="both")

        self.animation = FuncAnimation(
            self.fig, self.update_animation,
            frames=100, interval=50, blit=False
        )

    def calculate_rgb_colors(self, x, y, z):
        r = (x + 1) / 2
        g = (y + 1) / 2
        b = (z + 1) / 2
        return np.dstack((r, g, b))

    def update_animation(self, frame):
        angle = np.radians(frame * 3.6)
        x_new = self.x * np.cos(angle) - self.y * np.sin(angle)
        y_new = self.x * np.sin(angle) + self.y * np.cos(angle)
        z_new = self.z

        self.sphere.remove()
        self.sphere = self.ax.plot_surface(
            x_new, y_new, z_new,
            facecolors=self.calculate_rgb_colors(x_new, y_new, z_new),
            rstride=4, cstride=4, shade=False
        )
        return self.sphere,

    def remove_3d_visualization(self):
        if not self.visualization_active:
            return

        if self.animation:
            self.animation.event_source.stop()

        self.visualization_active = False