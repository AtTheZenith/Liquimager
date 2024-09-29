"""Liquimager App."""

from time import time
from typing import Callable

import customtkinter as ctk
from numexpr import NumExpr as evaluate
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
	TextField
)


class ImageManager:
	"""Image Manager Class because my procedural methods didn't work."""

	def __init__(self):
		self._orig_image = None
		self._image = None
		self._width_image = 0
		self._height_image = 0

	def set_new_image(self, new_image: Image.Image) -> None:
		"""Sets a new image.
		new_image: The image to be set.
		\n*args: None | **kwargs: None
		"""

		self._orig_image = new_image.convert("RGBA")
		self._image = self._orig_image.copy()
		self._width_image, self._height_image = self._orig_image.size

	def update_image(self, new_image: Image.Image) -> None:
		"""Updates the current image.
		\nnew_image: The image to be set.
		\n*args: None | **kwargs: None
		"""

		self._image = new_image.convert("RGBA")
		self._width_image, self._height_image = new_image.size

	def delete_image(self) -> None:
		"""Deletes the selected image.
		\nnew_image: The image to be set.
		\n*args: None | **kwargs: None
		"""

		self._orig_image, self._image, self._width_image, self._height_image = (None, None,0,0)

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
		return (self._width_image != 0 and self._width_image or 400, self._height_image != 0 and self._height_image or 400)


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

		Label(master=main_frame, position=(17, 98), text="Horizontal Position")
		Label(master=main_frame, position=(17, 148), text="Vertical Position")

		x_slider = Slider(master=main_frame, position=(24, 125))
		y_slider = Slider(master=main_frame, position=(24, 175))

		x_entry = TextField(master=main_frame, size=(120,20), position=(210,101))
		y_entry = TextField(master=main_frame, size=(120,20), position=(210,151))

		x_val = ctk.StringVar(master=x_entry, value='0', name='x')
		y_val = ctk.StringVar(master=y_entry, value='0', name='y')

		FramesSeperator(self)

		image_frame = ImageFrame(self)
		image_label = ImageLabel(image_frame)

		##################################################
		# Callbacks                                      #
		##################################################

		def set_option_access(access: bool) -> None:
			"""Disables/Enables the UI Elements.
				\naccess: bool (Enable or Disable)
				\n*args: None | **kwargs: None
			"""

			for item in [x_slider, x_entry, y_slider, y_entry, x_val, y_val]:
				if not isinstance(item, ctk.StringVar):
					item.configure(state=(access and "normal" or "disabled"))
				if isinstance(item, Slider):
					item.set(0)
					axis = 0 if item == x_slider else 1
					item.configure(
						to=im.get_image_size()[axis],
						number_of_steps=im.get_image_size()[axis]
					)
				elif isinstance(item, ctk.StringVar):
					item.set('0')

		set_option_access(access=False)


		def refresh_closure() -> Callable:
			last_call = time()
			image = im.get_orig_image()

			def _() -> None:
				nonlocal last_call, image

				if (im.get_image().size == (0,0)):
					return

				if time() - last_call < (1/120):
					return

				last_call = time()

				if im.get_orig_image() != image:
					image = im.get_orig_image()

				watermark = image.copy()
				drawing = ImageDraw.Draw(watermark, "RGBA")

				font_name = "arial"
				font = ImageFont.truetype(f"C:/Windows/Fonts/{font_name}.ttf", size=40)

				drawing.text(
					xy   = (x_slider.get(), y_slider.get()),
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

			return _

		refresh_image: Callable = refresh_closure()

		def open_image() -> None:
			"""Callback for file_button, manages the image selection.
			*args: None | **kwargs: None
			"""

			if im.get_image().size == (0, 0):
				file_path = ctk.filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.jfif")])

				if file_path:
					im.set_new_image(new_image=Image.open(file_path))
					file_button.configure(text="Remove File")
					set_option_access(access=True)
					image_label.configure(text="")
					refresh_image()
			else:
				im.delete_image()
				file_button.configure(text="Open File")
				set_option_access(access=False)
				image_label.configure(
					text="No Image Selected",
					image=ctk.CTkImage(dark_image=Image.new(mode="RGBA", size=(0, 0)), size=(0, 0)),
				)

		def x_slider_func(num) -> None:
			x_val.set(str(int(num)))

		def y_slider_func(num) -> None:
			y_val.set(str(int(num)))

		def x_val_callback(str1, str2, str3) -> None:
			if '..' in x_val.get() or not set(x_val.get()).issubset(set('0123456789+-*/.')):
				x_val.set(''.join(filter('0123456789+-*/.'.__contains__, x_val.get().replace('..', '.'))))
				return

			if str(x_slider.get()) != (x_val.get()):
				try:
					x_slider.set(evaluate(ex=x_val.get())().astype(int).item())
					refresh_image()
				except Exception:
					return

		def y_val_callback(str1, str2, str3) -> None:
			if '..' in y_val.get() or not set(y_val.get()).issubset(set('0123456789+-*/.')):
				y_val.set(''.join(filter('0123456789+-*/'.__contains__, y_val.get().replace('..', '.'))))
				return

			if str(y_slider.get()) != (y_val.get()):
				try:
					y_slider.set(evaluate(ex=y_val.get())().astype(int).item())
					refresh_image()
				except Exception:
					return

		##################################################
		# Callback binding                               #
		##################################################

		file_button.configure(command=open_image)

		x_slider.configure(command=x_slider_func)
		y_slider.configure(command=y_slider_func)

		x_entry.configure(textvariable=x_val)
		y_entry.configure(textvariable=y_val)

		x_val.trace_add(mode='write', callback=x_val_callback)
		y_val.trace_add(mode='write', callback=y_val_callback)


if __name__ == "__main__":
	App().mainloop()
