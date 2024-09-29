"""Required UI Elements for Liquimager."""

import customtkinter as ctk

COLORS = {
    "MainButton": "#2D5FC4",
    "MainButtonHover": "#2255BB",
    "AltButton": "#DDDDDD",
    "AltButtonHover": "#FFFFFF",
    "MainText": "#FFFFFF",
    "AltText": "#666666",
    "Window": "#242424",
    "MainFrame": "#2B2B2B",
    "AltFrame": "#444444",
}


class Label(ctk.CTkLabel):
    """Text label to label sliders and dropdowns.
    \nmaster: The parent UI element.
    \nposition: The position of the slider (an xy tuple).
    \n*args: None | **kwargs: None
    """

    def __init__(self, master: ctk.CTkBaseClass, position: tuple, text: str):
        super().__init__(
            master,
            text=text,
            font=("Montserrat", 13),
            text_color=COLORS["AltText"],
            bg_color="transparent",
            corner_radius=12,
        )
        self.place(x=position[0], y=position[1])


class Slider(ctk.CTkSlider):
    """Slider for adjusting the position of the text.
    \nmaster: The pareadnt UI element.
    \nposition: The position of the slider (an xy tuple).
    \n*args: None | **kwargs: None
    """

    def __init__(self, master: ctk.CTkBaseClass, position: tuple):
        super().__init__(
            master,
            from_=0,
            to=400,
            number_of_steps=400,
            width=312,
            height=18,
            corner_radius=12,
            orientation="horizontal",
            bg_color="transparent",
            fg_color=COLORS["AltFrame"],
            button_color=COLORS["AltButton"],
            progress_color=COLORS["MainButton"],
            button_hover_color=COLORS["AltButtonHover"],
            button_corner_radius=12,
        )
        self.place(x=position[0], y=position[1])


class TextField(ctk.CTkEntry):
    """Text field for entering text.
    \nmaster: The parent UI element.
    \nsize: The size of the text field
    \nposition: The position of the text field (an xy tuple).
    \n*args: None | **kwargs: None
    """

    def __init__(self, master: ctk.CTkBaseClass, size: tuple, position: tuple):
        super().__init__(
            master,
            width=size[0],
            height=size[1],
            corner_radius=5,
            border_width=2,
            bg_color="transparent",
            fg_color=COLORS["MainFrame"],
            placeholder_text_color=COLORS["MainText"],
            text_color=COLORS["MainText"],
            border_color=COLORS["AltFrame"],
            placeholder_text="0",
            font=("Montserrat", 12),
        )
        self.place(x=position[0], y=position[1])


class FileButton(ctk.CTkButton):
    """Button, for selecting an image file/removing selected image file.
    \nmaster: The parent UI element.
    \n*args: None | **kwargs: None
    """

    def __init__(self, master: ctk.CTkBaseClass):
        super().__init__(
            master,
            text="Open File",
            font=("Montserrat", 24),
            corner_radius=12,
            fg_color=COLORS["MainButton"],
            hover_color=COLORS["MainButtonHover"],
            width=320,
            height=50,
        )

        self.place(x=20, y=20)


class FileButtonSeperator(ctk.CTkFrame):
    """Frames Seperator, that will separate the main frame from the image frame.
    \nmaster: The parent UI element.
    \n*args: None | **kwargs: None
    """

    def __init__(self, master: ctk.CTkBaseClass):
        super().__init__(
            master, corner_radius=2, fg_color=COLORS["AltFrame"], width=300, height=2
        )
        self.place(x=30, y=89)


class MainFrame(ctk.CTkFrame):
    """Main Frame, that will contain all the main buttons.
    \nmaster: The parent UI element.
    \n*args: None | **kwargs: None
    """

    def __init__(self, master: ctk.CTk):
        super().__init__(master, corner_radius=24, width=360, height=560)
        self.place(x=20, y=20)


class FramesSeperator(ctk.CTkFrame):
    """Frames Seperator, that will separate the main frame from the image frame.
    \nmaster: The parent UI element.
    \n*args: None | **kwargs: None
    """

    def __init__(self, master: ctk.CTk):
        super().__init__(master, corner_radius=8, width=4, height=560)
        self.place(x=398, y=20)


class ImageLabel(ctk.CTkLabel):
    """Label, that will display the selected image.
    \nmaster: The parent UI element.
    \n*args: None | **kwargs: None
    """

    def __init__(self, master: ctk.CTkBaseClass):
        super().__init__(
            master,
            corner_radius=8,
            text="No Image Selected",
            font=("Montserrat", 24),
            width=720,
            height=520,
        )
        self.place(x=20, y=20)
        self.image = None


class ImageFrame(ctk.CTkFrame):
    """Image Frame, that will contain the image preview.
    \nmaster: The parent UI element.
    \n*args: None | **kwargs: None
    """

    def __init__(self, master: ctk.CTk):
        super().__init__(master, corner_radius=24, width=760, height=560)
        self.place(x=420, y=20)
