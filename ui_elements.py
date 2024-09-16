"""Required UI Elements for Liquimager."""
import customtkinter as ctk

class Label(ctk.CTkLabel):
    """Text label to label sliders and dropdowns.
        \nmaster: The parent UI element.
        \nposition: The position of the slider (an xy tuple).
        \n*args: None
        \n**kwargs: None
    """
    def __init__(self, master: ctk.CTkBaseClass, position: tuple, text: str):
        super().__init__(
            master,
            text          = text,
            font          = ('Montserrat', 13),
            text_color    = '#888888',
            bg_color      = 'transparent',
            corner_radius = 12
        )
        self.place(x = position[0], y = position[1])

class FileButton(ctk.CTkButton):
    """Button, for selecting an image file/removing selected image file.
        \nmaster: The parent UI element.
        \n*args: None
        \n**kwargs: None
    """
    def __init__(self, master: ctk.CTkBaseClass):
        super().__init__(
            master,
            text          = 'Open File',
            font          = ('Montserrat', 24),
            corner_radius = 12
        )

        self.image_file = None
        self._set_dimensions(320,50)
        self.place(x = 20, y = 20)


class FileButtonSeperator(ctk.CTkFrame):
    """Frames Seperator, that will separate the main frame from the image frame.
        \nmaster: The parent UI element.
        \n*args: None
        \n**kwargs: None
    """
    def __init__(self, master: ctk.CTkBaseClass):
        super().__init__(master, corner_radius = 2, fg_color='#555555')
        self.place(x = 398, y = 20)
        self._set_dimensions(300,2)

class Slider(ctk.CTkSlider):
    """Slider for adjusting the position of the text.
        \nmaster: The parent UI element.
        \nposition: The position of the slider (an xy tuple).
        \n*args: None
        \n**kwargs: None
    """
    def __init__(self, master: ctk.CTkBaseClass, position: tuple):
        super().__init__(
            master,
            from_         = 0,
            to            = 100,
            corner_radius = 12,
            orientation   = 'horizontal',
            bg_color      = 'transparent'
        )
        self.place(x = position[0], y = position[1])

class MainFrame(ctk.CTkFrame):
    """Main Frame, that will contain all the main buttons.
        \nmaster: The parent UI element.
        \n*args: None
        \n**kwargs: None
    """
    def __init__(self, master: ctk.CTk):
        super().__init__(master, corner_radius = 24)
        self.place(x = 20, y = 20)
        self._set_dimensions(360,560)

class FramesSeperator(ctk.CTkFrame):
    """Frames Seperator, that will separate the main frame from the image frame.
        \nmaster: The parent UI element.
        \n*args: None
        \n**kwargs: None
    """
    def __init__(self, master: ctk.CTk):
        super().__init__(master, corner_radius = 8)
        self.place(x = 398, y = 20)
        self._set_dimensions(4,560)

class ImageLabel(ctk.CTkLabel):
    """Label, that will display the selected image.
        \nmaster: The parent UI element.
        \n*args: None
        \n**kwargs: None
    """
    def __init__(self, master: ctk.CTkBaseClass):
        super().__init__(
            master,
            corner_radius = 8,
            text          = 'No Image Selected',
            font          = ('Montserrat', 24)
        )
        self._set_dimensions(720,520)
        self.place(x = 20, y = 20)
        self.image = None

class ImageFrame(ctk.CTkFrame):
    """Image Frame, that will contain the image preview.
        \nmaster: The parent UI element.
        \n*args: None
        \n**kwargs: None
    """
    def __init__(self, master: ctk.CTk):
        super().__init__(master, corner_radius = 24)
        self._set_dimensions(760,560)
        self.place(x = 420, y = 20)
