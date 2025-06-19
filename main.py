import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

class ImageOverlayApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Overlay App")
        master.geometry("1200x800")
        master.configure(bg="#f0f0f0")

        self.base_img_cv = None
        self.overlay_img_cv = None
        self.original_overlay_dims = None
        self.composed_img_cv = None

        top_frame = tk.Frame(self.master, bg="#e0e0e0", bd=2, relief="groove")
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.load_base_btn = tk.Button(top_frame, text="Load Base Image",
                                      command=self.load_base_image,
                                      bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                                      relief="raised", bd=3, padx=10, pady=5)
        self.load_base_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.load_overlay_btn = tk.Button(top_frame, text="Load Overlay Image",
                                         command=self.load_overlay_image,
                                         bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                                         relief="raised", bd=3, padx=10, pady=5)
        self.load_overlay_btn.pack(side=tk.LEFT, padx=5, pady=5)

        slider_frame = tk.Frame(top_frame, bg="#e0e0e0")
        slider_frame.pack(side=tk.LEFT, padx=15)

        tk.Label(slider_frame, text="X Pos", bg="#e0e0e0", font=("Arial", 9)).grid(row=0, column=0, padx=5)
        self.x_slider = ttk.Scale(slider_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                  command=self.update_image, length=100)
        self.x_slider.set(0)
        self.x_slider.grid(row=0, column=1, padx=5)

        tk.Label(slider_frame, text="Y Pos", bg="#e0e0e0", font=("Arial", 9)).grid(row=0, column=2, padx=5)
        self.y_slider = ttk.Scale(slider_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                  command=self.update_image, length=100)
        self.y_slider.set(0)
        self.y_slider.grid(row=0, column=3, padx=5)

        tk.Label(slider_frame, text="Alpha", bg="#e0e0e0", font=("Arial", 9)).grid(row=0, column=4, padx=5)
        self.alpha_slider = ttk.Scale(slider_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                      command=self.update_image, length=100)
        self.alpha_slider.set(100)
        self.alpha_slider.grid(row=0, column=5, padx=5)

        tk.Label(slider_frame, text="Size %", bg="#e0e0e0", font=("Arial", 9)).grid(row=0, column=6, padx=5)
        self.size_slider = ttk.Scale(slider_frame, from_=10, to=300, orient=tk.HORIZONTAL,
                                     command=self.update_image, length=100)
        self.size_slider.set(100)
        self.size_slider.grid(row=0, column=7, padx=5)

        self.export_btn = tk.Button(top_frame, text="Export Image",
                                    command=self.export_image,
                                    bg="#FF5722", fg="white", font=("Arial", 10, "bold"),
                                    relief="raised", bd=3, padx=10, pady=5,
                                    state="disabled")
        self.export_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.canvas = tk.Canvas(self.master, bg="#ffffff", bd=2, relief="sunken")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.canvas_img = None

        self.update_image()
        self.master.bind("<Configure>", lambda e: self.update_image() if hasattr(self, "canvas") else None)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if not file_path:
            return None

        img_cv = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        if img_cv is None:
            return None

        if len(img_cv.shape) == 2:
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_GRAY2BGR)
        elif img_cv.shape[2] == 1:
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_GRAY2BGR)
        return img_cv

    def load_base_image(self):
        img = self.load_image()
        if img is not None:
            self.base_img_cv = img
            self.update_image()

    def load_overlay_image(self):
        img = self.load_image()
        if img is not None:
            self.overlay_img_cv = img
            h, w = img.shape[:2]
            self.original_overlay_dims = (w, h)
            self.update_image()

    def set_slider_states(self, state):
        for slider in [self.x_slider, self.y_slider, self.alpha_slider, self.size_slider]:
            slider.state([state])

    def update_image(self, event=None):
        if self.base_img_cv is None:
            if not hasattr(self, "canvas"):
                return
            self.canvas.delete("all")
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()
            self.canvas.create_rectangle(0, 0, w, h, fill="black")
            self.canvas.create_text(w/2, h/2,
                                    text="Load Base Image to Start", fill="white", font=("Arial", 20, "bold"))
            self.set_slider_states("disabled")
            self.export_btn.config(state="disabled")
            return

        self.set_slider_states("!disabled")

        base_h, base_w = self.base_img_cv.shape[:2]
        display_img = self.base_img_cv.copy()

        if display_img.shape[2] == 4:
            display_img = cv2.cvtColor(display_img, cv2.COLOR_BGRA2BGR)

        if self.overlay_img_cv is not None and self.original_overlay_dims is not None:
            alpha = self.alpha_slider.get() / 100.0
            size_percent = self.size_slider.get() / 100.0
            orig_w, orig_h = self.original_overlay_dims
            new_w = max(1, int(orig_w * size_percent))
            new_h = max(1, int(orig_h * size_percent))

            overlay_resized = cv2.resize(self.overlay_img_cv, (new_w, new_h), interpolation=cv2.INTER_AREA)

            x_pos = int((self.x_slider.get() / 100.0) * (base_w - new_w))
            y_pos = int((self.y_slider.get() / 100.0) * (base_h - new_h))

            x_pos = max(0, min(x_pos, base_w - new_w))
            y_pos = max(0, min(y_pos, base_h - new_h))

            if overlay_resized.shape[2] == 4:
                overlay_rgb = overlay_resized[:, :, :3]
                alpha_mask = (overlay_resized[:, :, 3] / 255.0) * alpha
                alpha_mask_3 = cv2.merge([alpha_mask, alpha_mask, alpha_mask])
            else:
                overlay_rgb = overlay_resized
                alpha_mask_3 = np.ones((new_h, new_w, 3), dtype=np.float32) * alpha

            roi = display_img[y_pos:y_pos + new_h, x_pos:x_pos + new_w].astype(np.float32)
            blended = roi * (1 - alpha_mask_3) + overlay_rgb * alpha_mask_3
            display_img[y_pos:y_pos + new_h, x_pos:x_pos + new_w] = blended.astype(np.uint8)

        self.composed_img_cv = display_img.copy()
        self.export_btn.config(state="normal")

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        if canvas_w < 10 or canvas_h < 10:
            return

        img_h, img_w = display_img.shape[:2]
        scale = min(canvas_w / img_w, canvas_h / img_h)
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
        resized = cv2.resize(display_img, (new_w, new_h), interpolation=cv2.INTER_AREA)

        canvas_img = np.ones((canvas_h, canvas_w, 3), dtype=np.uint8) * 255
        x_offset = (canvas_w - new_w) // 2
        y_offset = (canvas_h - new_h) // 2
        canvas_img[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = resized

        canvas_img_rgb = cv2.cvtColor(canvas_img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(canvas_img_rgb)
        imgtk = ImageTk.PhotoImage(image=img_pil)
        self.canvas_img = imgtk

        self.canvas.delete("all")
        self.canvas.create_image(canvas_w // 2, canvas_h // 2, image=imgtk, anchor="center")

    def export_image(self):
        if self.composed_img_cv is None:
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if not file_path:
            return
        cv2.imwrite(file_path, self.composed_img_cv)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageOverlayApp(root)
    root.mainloop()
