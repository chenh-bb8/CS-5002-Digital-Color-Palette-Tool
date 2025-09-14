import tkinter as tk
from tkinter import messagebox
import colorsys


class ColorPicker(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("Color Picker Demo")

        # HSV values
        self.hue = 0.0  # [0,1]
        self.sat = 1.0  # [0,1]
        self.val = 1.0  # [0,1]

        # Dimensions
        self.square_size = 256
        self.hue_bar_height = 256
        self.hue_bar_width = 30

        # Frames
        self.left_frame = tk.Frame(self.master)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.middle_frame = tk.Frame(self.master)
        self.middle_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.right_frame = tk.Frame(self.master)
        self.right_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Hue canvas
        self.hue_canvas = tk.Canvas(self.left_frame, width=self.hue_bar_width, height=self.hue_bar_height, bd=2,
                                    relief=tk.SUNKEN)
        self.hue_canvas.pack()
        self.hue_canvas.bind("<Button-1>", self.on_hue_click)

        # Draw the hue gradient
        self.draw_hue_bar()

        # Color square
        self.color_canvas = tk.Canvas(self.middle_frame, width=self.square_size, height=self.square_size, bd=2,
                                      relief=tk.SUNKEN)
        self.color_canvas.pack()
        self.color_canvas.bind("<Button-1>", self.on_canvas_click)

        # Color display
        self.color_display = tk.Canvas(self.right_frame, width=50, height=50, bd=2, relief=tk.SUNKEN)
        self.color_display.pack(pady=5)

        # RGB entries
        self.r_var = tk.StringVar(value="255")
        self.g_var = tk.StringVar(value="0")
        self.b_var = tk.StringVar(value="0")

        tk.Label(self.right_frame, text="R:").pack(anchor="w")
        self.r_entry = tk.Entry(self.right_frame, textvariable=self.r_var, width=5)
        self.r_entry.pack(anchor="w")

        tk.Label(self.right_frame, text="G:").pack(anchor="w")
        self.g_entry = tk.Entry(self.right_frame, textvariable=self.g_var, width=5)
        self.g_entry.pack(anchor="w")

        tk.Label(self.right_frame, text="B:").pack(anchor="w")
        self.b_entry = tk.Entry(self.right_frame, textvariable=self.b_var, width=5)
        self.b_entry.pack(anchor="w")

        self.update_button = tk.Button(self.right_frame, text="Update Color", command=self.update_color_from_rgb)
        self.update_button.pack(pady=5)

        # Button to show conversions
        self.conversion_button = tk.Button(self.right_frame, text="Show Conversions", command=self.show_conversions)
        self.conversion_button.pack(pady=5)

        # Draw initial color square and display
        self.draw_color_square()
        self.update_color_display()

    def hsv_to_hex(self, h, s, v):
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))

    def draw_hue_bar(self):
        """Draw a vertical gradient representing hue from 0° to 360°."""
        # Hue goes from 0 (red) to 1 (back to red) through all colors.
        # We will map each pixel row to a hue value.
        for y in range(self.hue_bar_height):
            h = y / (self.hue_bar_height - 1)
            # Saturation=1, Value=1 for a pure hue
            hex_color = self.hsv_to_hex(h, 1.0, 1.0)
            # Draw a line segment for each pixel row
            self.hue_canvas.create_line(0, y, self.hue_bar_width, y, fill=hex_color)

    def on_hue_click(self, event):
        """User clicked on the hue bar. Update hue based on y position."""
        y = event.y
        if 0 <= y < self.hue_bar_height:
            self.hue = y / (self.hue_bar_height - 1)
            self.draw_color_square()
            self.update_color_display()

    def draw_color_square(self):
        """Draw the saturation-value gradient for the current hue."""
        self.color_canvas.delete("all")
        step = 4  # Drawing every 4 pixels horizontally to improve performance
        for y in range(self.square_size):
            val = 1 - (y / (self.square_size - 1))
            for x in range(0, self.square_size, step):
                sat = x / (self.square_size - 1)
                hex_color = self.hsv_to_hex(self.hue, sat, val)
                self.color_canvas.create_rectangle(x, y, x + step, y + 1, outline=hex_color, fill=hex_color)

    def on_canvas_click(self, event):
        """User clicked on the color square to pick saturation and value."""
        x, y = event.x, event.y
        if 0 <= x < self.square_size and 0 <= y < self.square_size:
            self.sat = x / (self.square_size - 1)
            self.val = 1 - (y / (self.square_size - 1))
            self.update_color_display()

    def update_color_display(self):
        """Update the color display and the RGB entries."""
        r, g, b = colorsys.hsv_to_rgb(self.hue, self.sat, self.val)
        R, G, B = int(r * 255), int(g * 255), int(b * 255)

        hex_color = '#{:02x}{:02x}{:02x}'.format(R, G, B)
        self.color_display.delete("all")
        self.color_display.create_rectangle(0, 0, 50, 50, fill=hex_color, outline=hex_color)

        # Update entries
        self.r_var.set(str(R))
        self.g_var.set(str(G))
        self.b_var.set(str(B))

    def update_color_from_rgb(self):
        """Update HSV based on given RGB and redraw."""
        try:
            R = int(self.r_var.get())
            G = int(self.g_var.get())
            B = int(self.b_var.get())

            R = max(0, min(R, 255))
            G = max(0, min(G, 255))
            B = max(0, min(B, 255))

            self.r_var.set(str(R))
            self.g_var.set(str(G))
            self.b_var.set(str(B))

            r = R / 255.0
            g = G / 255.0
            b = B / 255.0

            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            self.hue = h
            self.sat = s
            self.val = v

            # Redraw hue bar selection (no direct indicator, but hue changed)
            # Redraw the square with the new hue
            self.draw_color_square()
            self.update_color_display()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter integer values for R, G, and B.")

    def rgb_to_cmyk(self, R, G, B):
        r = R / 255.0
        g = G / 255.0
        b = B / 255.0
        k = 1 - max(r, g, b)
        if k < 1:
            c = (1 - r - k) / (1 - k)
            m = (1 - g - k) / (1 - k)
            y = (1 - b - k) / (1 - k)
        else:
            c = 0
            m = 0
            y = 0
        return (c, m, y, k)

    def show_conversions(self):
        """Show HSV and CMYK conversions for the current RGB color."""
        try:
            R = int(self.r_var.get())
            G = int(self.g_var.get())
            B = int(self.b_var.get())

            R = max(0, min(R, 255))
            G = max(0, min(G, 255))
            B = max(0, min(B, 255))

            r = R / 255.0
            g = G / 255.0
            b = B / 255.0

            # RGB to HSV
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            h_deg = h * 360

            # RGB to CMYK
            c, m, y, k = self.rgb_to_cmyk(R, G, B)

            details = (
                f"Current RGB: ({R}, {G}, {B})\n\n"
                f"HSV: (H={h_deg:.2f}°, S={s:.2f}, V={v:.2f})\n\n"
                f"CMYK: (C={c:.2f}, M={m:.2f}, Y={y:.2f}, K={k:.2f})"
            )

            messagebox.showinfo("Color Conversions", details)

        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid integer values for R, G, and B.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ColorPicker(master=root)
    app.mainloop()
