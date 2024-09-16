"""Liquimager App."""
from PIL import Image, ImageDraw, ImageFont
from threading import Thread
import customtkinter as ctk
from ui_elements import (
    Label,
    FileButton,
    FileButtonSeperator,
    Slider,
    MainFrame,
    FramesSeperator,
    ImageLabel,
    ImageFrame,
)


class ImageManager:
    """Image Manager Class because my procedural methods didn't work."""

    def __init__(self):
        self.orig_image = None
        self.image = None
        self.width_image = 0
        self.height_image = 0

    def set_new_image(self, new_image: Image.Image):
        """Sets a new image.
        \nnew_image: The image to be set.
        \n*args: None | **kwargs: None
        """

        self.orig_image = new_image
        self.image = new_image.copy()
        self.width_image, self.height_image = new_image.size

    def update_image(self, new_image: Image.Image):
        """Updates the current image.
        \nnew_image: The image to be set.
        \n*args: None | **kwargs: None
        """

        self.image = new_image.copy()
        self.width_image, self.height_image = new_image.size

    def delete_image(self):
        """Deletes the selected image.
        \nnew_image: The image to be set.
        \n*args: None | **kwargs: None
        """

        self.orig_image, self.image, self.width_image, self.height_image = (
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

        return (int(self.width_image / scale), int(self.height_image / scale))

    def get_image(self) -> Image.Image:
        """Returns the current image.
        \n*args: None | **kwargs: None
        """
        return self.image or Image.new(mode="RGBA", size=(0, 0))


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

        FramesSeperator(self)

        image_frame = ImageFrame(self)
        image_label = ImageLabel(image_frame)

        ##################################################
        # Callbacks                                      #
        ##################################################

        def open_image():
            """Callback for file_button, manages the image selection.
            *args: None | **kwargs: None
            """

            if im.orig_image is None:
                file_path = ctk.filedialog.askopenfilename(
                    filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.jfif")]
                )

                if file_path:
                    im.set_new_image(
                        new_image=Image.open(file_path)
                        or Image.new(mode = "RGBA", size = (0, 0))
                    )

                    file_button.configure(text="Remove File")

                    image_label.configure(
                        text="No Image Selected",
                        image=ctk.CTkImage(
                            dark_image = im.get_image(),
                            size = im.fit_image(
                                image = im.get_image(),
                                width = 720,
                                height = 520,
                            ),
                        ),
                    )
            else:
                im.delete_image()
                file_button.configure(text="Open File")
                image_label.configure(text="No Image Selected",
                    image = ctk.CTkImage(
                        dark_image=im.get_image(),
                        size=(0, 0)
                    ),
                )

        file_button.configure(command=open_image)

if __name__ == "__main__":
    App().mainloop()
