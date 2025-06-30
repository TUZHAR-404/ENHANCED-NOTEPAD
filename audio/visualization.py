from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import numpy as np
import customtkinter as ctk

class Visualization:
    def __init__(self, parent_frame):
        self.visualization_active = False
        self.animation = None
        self.parent_frame = parent_frame
        self.fig = None
        self.ax = None
        self.sphere = None

    def create_3d_visualization(self):
        if self.visualization_active:
            return

        self.visualization_active = True
        self.visualization_frame = ctk.CTkFrame(self.parent_frame)
        self.visualization_frame.pack(expand=True, fill="both", padx=5, pady=5)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111, projection='3d')

        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        self.x = np.outer(np.cos(u), np.sin(v))
        self.y = np.outer(np.sin(u), np.sin(v))
        self.z = np.outer(np.ones(np.size(u)), np.cos(v))

        self.sphere = self.ax.plot_surface(
            self.x, self.y, self.z,
            facecolors=self.calculate_rgb_colors(self.x, self.y, self.z),
            rstride=4, cstride=4, shade=False
        )
        self.ax.set_axis_off()
        self.ax.set_xlim([-1.5, 1.5])
        self.ax.set_ylim([-1.5, 1.5])
        self.ax.set_zlim([-1.5, 1.5])
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.visualization_frame)
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

        if hasattr(self, 'visualization_frame'):
            self.visualization_frame.destroy()
            del self.visualization_frame

        self.visualization_active = False