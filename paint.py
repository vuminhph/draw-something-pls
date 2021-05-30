from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfile, asksaveasfilename
import io
import os
from PIL import Image


class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'
    DEFAULT_WIDTH = 600
    DEFAULT_HEIGHT = 600
    DEFAULT_BG = 'white'
    LINE_WIDTH_OFFSET = 3
    ERASER_WIDTH_OFFSET = 13

    # Called when an instance of the class is created
    def __init__(self):

        self.root = Tk()

        self.pen_button = Button(self.root, text='Pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.eraser_button = Button(
            self.root, text='Eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=1)

        self.color_button = Button(
            self.root, text='Color', command=self.choose_color)
        self.color_button.grid(row=0, column=2)

        self.reset_button = Button(
            self.root, text='Clear all', command=self.clear_all)
        self.reset_button.grid(row=0, column=3)

        self.choose_size_button = Scale(
            self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=1, column=0)

        self.choose_eraser_size_button = Scale(
            self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_eraser_size_button.grid(row=1, column=1)

        self.save_button = Button(self.root, text='Save', command=self.save)
        self.save_button.grid(row=0, column=4)

        self.c = Canvas(self.root, bg=self.DEFAULT_BG,
                        width=self.DEFAULT_WIDTH, height=self.DEFAULT_HEIGHT)
        self.c.grid(row=2, columnspan=5)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.eraser_width = self.choose_eraser_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.eraser_on = False
        self.activate_button(self.pen_button)

    def choose_color(self):
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def clear_all(self):
        temp_button = self.active_button
        self.activate_button(self.reset_button, eraser_mode=False)
        self.c.delete('all')
        self.reset_button.config(relief=RAISED)
        self.activate_button(temp_button, eraser_mode=self.eraser_on)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = self.c["bg"] if self.eraser_on else self.color
        if self.old_x and self.old_y:
            if self.eraser_on:
                self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                                   width=self.line_width+self.ERASER_WIDTH_OFFSET, fill=paint_color,
                                   capstyle=ROUND, smooth=TRUE, splinesteps=36)
            else:
                self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                                   width=self.line_width+self.LINE_WIDTH_OFFSET, fill=paint_color,
                                   capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def save(self):
        ps = self.c.postscript(colormode='color')
        # filename = asksaveasfilename(defaultextension='.jpg')
        save_dir = './saves'
        filename = 'image.png'
        path = os.path.join(save_dir, filename)
        print(path)
        if path:
            img = Image.open(io.BytesIO(ps.encode('utf-8')))
            img.save(path)


if __name__ == '__main__':
    Paint()
