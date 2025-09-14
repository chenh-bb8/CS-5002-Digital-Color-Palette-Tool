import tkinter as tk
from tkinter import messagebox
import colorsys

class ColorPalette(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master.title("Color Palette")

        # Frames, left: Hue, mid: square, right: RGB number
        self.left_frame = tk.Frame(self.master)
        self.mid_frame = tk.Frame(self.master)
        self.right_frame = tk.Frame(self.master)

        self.left_frame.pack(side="left", padx=10, pady=10)
        self.mid_frame.pack(side= "left", padx=10, pady=10)
        self.right_frame.pack(side="right", padx=10, pady=10)

        # Size set, 256 for later use
        self.square_size = 256
        self.hue_bar_height = 256
        self.hue_bar_width = 30

        # HSV values
        self.hue = 0.0
        self.saturation = 1.0
        self.value = 1.0

        # Hue canvas
        self.hue_canvas = tk.Canvas(self.left_frame, width = self.hue_bar_width, height = self.hue_bar_height, bd= 3)
        self.hue_canvas.pack()
        self.hue_canvas.bind("<Button-1>", self.hue_click)

        # Draw the hue bar
        self.draw_hue_bar()

        # Color square
        self.color_canvas = tk.Canvas(self.mid_frame, width = self.square_size, height=self.square_size,bd = 3, relief = "sunken")
        self.color_canvas.pack()
        self.color_canvas.bind("<Button-1>", self.canvas_click)

        # Draw the square
        self.draw_color_square()

        # Color Display (user picked)
        self.color_display = tk.Canvas(self.right_frame, width = 50, height = 50, bd = 3, relief = "sunken")
        self.color_display.pack(padx = 10, pady = 10)

        # RGB Entries
        self.r_var = tk.StringVar(value = "255")
        self.g_var = tk.StringVar(value = "0")
        self.b_var = tk.StringVar(value = "0")

        # Label set
        tk.Label(self.right_frame, text = "R").pack(anchor = "w")
        self.r_entry = tk.Entry(self.right_frame, textvariable=self.r_var, width = 5)
        self.r_entry.pack(anchor = "w")

        tk.Label(self.right_frame, text="G").pack(anchor="w")
        self.g_entry = tk.Entry(self.right_frame, textvariable=self.g_var, width=5)
        self.g_entry.pack(anchor="w")

        tk.Label(self.right_frame, text="B").pack(anchor="w")
        self.b_entry = tk.Entry(self.right_frame, textvariable=self.b_var, width=5)
        self.b_entry.pack(anchor="w")

        self.update_button = tk.Button(self.right_frame, text="Update Color", command=self.update_color_from_rgb)
        self.update_button.pack(padx = 10,pady = 10)

        # Conversion button
        self.conversion_button = tk.Button(self.right_frame, text="Conversions", command= self.show_conversion)
        self.conversion_button.pack(padx = 10, pady = 10)

        # Show hex
        self.hex_var = tk.StringVar(value="#ffffff")
        tk.Label(self.right_frame, text="Hex:").pack(anchor="w")
        self.hex_label = tk.Label(self.right_frame, textvariable=self.hex_var, width=10)
        self.hex_label.pack(anchor="w", pady=5)

        # Initial color display
        self.update_color_display()


    def hsv_to_hex(self, h, s, v):
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'

    # The left frame
    def draw_hue_bar(self):
        for y in range(self.hue_bar_height):
            h = y/(self.hue_bar_height - 1)
            # This is a hue bar, so set s and v equal to 1.0
            hex_color = self.hsv_to_hex(h,1.0,1.0)
            # Draw line by line
            self.hue_canvas.create_line(0,y,self.hue_bar_width,y, fill = hex_color)

    # The mid frame, a square to change saturation and value for the selected hue
    def draw_color_square(self):
        self.color_canvas.delete("all")
        # In vertical, v decrease from top to bottom
        for y in range(self.square_size):
            v = 1 - (y/(self.square_size-1))
            # In horizon, s increase form left ro right
            for x in range(0, self.square_size):
                s = x / (self.square_size -1)
                hex_color = self.hsv_to_hex(self.hue, s, v)
                self.color_canvas.create_rectangle(x,y,x+1, y+1, outline = hex_color,fill = hex_color)

    # Click to choose hue
    def hue_click(self, event):
        y = event.y
        if 0 <= y < self.hue_bar_height:
            self.hue = y / (self.hue_bar_height - 1)
            self.draw_color_square()
            self.update_color_display()

    # Click to set s and v for hue
    def canvas_click(self, event):
        x,y = event.x, event.y
        # Check the area of Square
        if 0 <= x <= self.square_size and 0<= y <= self.square_size:
            self.saturation = x / (self.square_size -1)
            self.value = 1 - y/(self.square_size -1)
            self.update_color_display()

    # Update the color display
    def update_color_display(self):
        r,g,b = colorsys.hsv_to_rgb(self.hue,self.saturation, self.value)
        R, G, B = int(r*255), int(g*255), int(b*255)
        hex_color = f'#{R:02x}{G:02x}{B:02x}'
        self.color_display.delete("all")
        self.color_display.create_rectangle(0,0,50,50, fill = hex_color, outline = hex_color)

        # Update the number in Entry
        self.r_var.set(str(R))
        self.g_var.set(str(G))
        self.b_var.set(str(B))

        # Update hex label
        self.hex_var.set(hex_color)
        self.hex_label.config()

    # Allow user to entry R G B and update
    def update_color_from_rgb(self):
        try:
            R = int(self.r_var.get())
            G = int(self.g_var.get())
            B = int(self.b_var.get())

            # If user entry over 255 or less than 0, change it to 255 or 0
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
            self.saturation = s
            self.value = v

            # Redraw hue bar selection (no direct indicator, but hue changed)
            # Redraw the square with the new hue
            self.draw_color_square()
            self.update_color_display()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter integer values for R, G, and B.")

    # Convert RGB to CMYK (By formula)
    def rgb_to_CMYK(self, R, G, B):
        r = R / 255.0
        g = G / 255.0
        b = B / 255.0

        k = 1 - max(r, g, b)

        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)

        return (c, m, y, k)

    # Show HSV and CMYK based on current RGB
    def show_conversion(self):
        #Same as previous
        R = int(self.r_var.get())
        G = int(self.g_var.get())
        B = int(self.b_var.get())

        R = max(0, min(R, 255))
        G = max(0, min(G, 255))
        B = max(0, min(B, 255))

        r = R / 255.0
        g = G / 255.0
        b = B / 255.0

        # RGB TO HSV
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        # 0° to 360°（Red circle back to Red)
        h_deg = h * 360

        # RGB to CMYK
        c, m, y, k = self.rgb_to_CMYK(R, G, B)

        details = (
            f"Current RGB: ({R}, {G}, {B})\n\n"
            f"HSV: (H={h_deg:.2f}°, S={s:.2f}, V={v:.2f})\n\n"
            f"CMYK: (C={c:.2f}, M={m:.2f}, Y={y:.2f}, K={k:.2f})"
        )

        messagebox.showinfo("Color Conversions", details)

if __name__ == "__main__":
    main_window = tk.Tk()
    palette = ColorPalette(master = main_window)
    palette.mainloop()


