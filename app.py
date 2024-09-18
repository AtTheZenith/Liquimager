"""Liquimager App."""

from time import time
from typing import Callable

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont

from ui_elements import (
    FileButton,
    FileButtonSeperator,
    FramesSeperator,
    ImageFrame,
    ImageLabel,
    Label,
    MainFrame,
    Slider,
)


class ImageManager:
    """Image Manager Class because my procedural methods didn't work."""

    def __init__(self):
        self._orig_image = None
        self._image = None
        self._width_image = 0
        self._height_image = 0

    def set_new_image(self, new_image: Image.Image):
        """Sets a new image.
        new_image: The image to be set.
        \n*args: None | **kwargs: None
        """

        self._orig_image = new_image.convert("RGBA")
        self._image = self._orig_image.copy()
        self._width_image, self._height_image = self._orig_image.size

    def update_image(self, new_image: Image.Image):
        """Updates the current image.
        \nnew_image: The image to be set.
        \n*args: None | **kwargs: None
        """

        self._image = new_image.convert("RGBA")
        self._width_image, self._height_image = new_image.size

    def delete_image(self):
        """Deletes the selected image.
        \nnew_image: The image to be set.
        \n*args: None | **kwargs: None
        """

        self._orig_image, self._image, self._width_image, self._height_image = (
            None,
            None,
            0,
            0,
        )

    def fit_image(self, image: Image.Image, width: int, height: int) -> tuple:
        """Fits the image to a given width and height.
        \nimage: The image to fit.
        \nwidth: The width to fit the image to.
        \nheight: The height to fit the image to.
        \n*args: None | **kwargs: None
        """

        x_scale = image.width / width
        y_scale = image.height / height

        scale = max(x_scale, y_scale)

        return (int(self._width_image / scale), int(self._height_image / scale))

    def get_orig_image(self) -> Image.Image:
        """Returns the original image.
        \n*args: None | **kwargs: None
        """
        return (self._orig_image and self._orig_image or Image.new(mode="RGBA", size=(0, 0)))

    def get_image(self) -> Image.Image:
        """Returns the current image.
        \n*args: None | **kwargs: None
        """
        return self._image or Image.new(mode="RGBA", size=(0, 0))

    def get_image_size(self) -> tuple:
        """Returns the size of the current image as a tuple.
        \n*args: None | **kwargs: None
        """
        return (self._width_image, self._height_image)


im = ImageManager()


class App(ctk.CTk):
    """App class, call 'App().mainloop()' to run."""

    def __init__(self):
        super().__init__()
        self.title("Liquimager")
        self.geometry("1200x600")
        self.resizable(False, False)

        ##################################################
        # UI Elements                                    #
        ##################################################

        main_frame = MainFrame(self)

        file_button = FileButton(main_frame)
        FileButtonSeperator(main_frame)

        Label(master=main_frame, position=(17, 100), text="Horizontal Position")
        Label(master=main_frame, position=(17, 150), text="Vertical Position")

        x_slider = Slider(master=main_frame, position=(24, 125))
        y_slider = Slider(master=main_frame, position=(24, 175))

        FramesSeperator(self)

        image_frame = ImageFrame(self)
        image_label = ImageLabel(image_frame)

        ##################################################
        # Callbacks                                      #
        ##################################################

        def set_option_access(access: bool):
            """ """
            for item in [x_slider, y_slider]:
                if isinstance(item, ctk.CTkSlider):
                    item.set(0)
                    item.configure(to=im.get_image_size()[1] or 1)
                item.configure(state=(access and "normal" or "disabled"))

        set_option_access(access=False)

        def refresh_closure() -> Callable:
            last_call = time()
            image = im.get_orig_image()

            def refresh_image(_):
                nonlocal last_call, image
                if time() - last_call < 0.033:
                    print("debounce")
                    return

                last_call = time()
                print("undebounce")

                x_pos, y_pos = x_slider.get(), y_slider.get()

                if im.get_orig_image() != image:
                    image = im.get_orig_image()

                watermark = image.copy()
                drawing = ImageDraw.Draw(watermark, "RGBA")

                font_name = "arial"
                font = ImageFont.truetype(f"C:/Windows/Fonts/{font_name}.ttf", size=40)

                drawing.text(
                    xy   = (x_pos, y_pos),
                    text = "Watermark",
                    fill = (255, 255, 255, 128),
                    font = font,
                )

                im.update_image(watermark)

                image_label.configure(
                    image=ctk.CTkImage(
                        dark_image=im.get_image(),
                        size=im.fit_image(image=im.get_image(), width=720, height=520),
                    )
                )

            return refresh_image

        ref_fun = refresh_closure()

        def open_image():
            """Callback for file_button, manages the image selection.
            *args: None | **kwargs: None
            """

            if im.get_image_size() == (0, 0):
                file_path = ctk.filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.jfif")])

                if file_path:
                    im.set_new_image(new_image=Image.open(file_path))
                    file_button.configure(text="Remove File")
                    set_option_access(access=True)
                    image_label.configure(text="")
                    ref_fun(0)
            else:
                im.delete_image()
                file_button.configure(text="Open File")
                set_option_access(access=False)
                image_label.configure(
                    text="No Image Selected",
                    image=ctk.CTkImage(dark_image=Image.new(mode="RGBA", size=(0, 0)), size=(0, 0)),
                )

        ##################################################
        # Callback binding                               #
        ##################################################

        file_button.configure(command=open_image)
        x_slider.configure(command=ref_fun)
        y_slider.configure(command=ref_fun)


if __name__ == "__main__":
    App().mainloop()
