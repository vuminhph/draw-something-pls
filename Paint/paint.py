from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfile, asksaveasfilename
from tkinter import messagebox
import tkinter.ttk as ttk
import io
import os
from tkinter.tix import WINDOW
from PIL import Image

class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'
    DEFAULT_WIDTH = 600
    DEFAULT_HEIGHT = 600
    CANVAS_BG = 'white'
    WINDOW_BG = '#17202A'
    LINE_WIDTH_OFFSET = 3
    ERASER_WIDTH_OFFSET = 13
    TIME_LIMIT = 30

    # Called when an instance of the class is created
    def __init__(self):
        self.root = Tk()
        self.root.geometry("600x700")
        self.root.title("Paint")
        self.root.configure(bg=self.WINDOW_BG)

        self.style = ttk.Style()
        self.style.configure("myStyle.Horizontal.TScale", background = self.WINDOW_BG)

        self.pen_button = Button(self.root, height=1, width=7, bg='#eba134', text='Pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0, pady=8)
     
        self.eraser_button = Button(
            self.root, height=1, width=7, bg='#de7c7c', text='Eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=1)

        self.color_button = Button(
            self.root, height=1, width=7, bg='#8ad190', text='Color', command=self.choose_color)
        self.color_button.grid(row=0, column=2)

        self.reset_button = Button(
            self.root, height=1, width=7, bg='#815f96', text='Clear', command=self.clear_all)
        self.reset_button.grid(row=0, column=3)

        # self.save_button = Button(self.root, height=1, width=4, bg='#e8b443', text='Finish', command=self.quit)
        # self.save_button.grid(row=0, column=4)

        self.choose_size_slide = ttk.Scale(
            self.root, from_=1, to=10, orient=HORIZONTAL, style="myStyle.Horizontal.TScale")
        self.choose_size_slide.grid(row=1, column=0, pady=10)
        
        self.choose_eraser_size_button = ttk.Scale(
            self.root,from_=1, to=10, orient=HORIZONTAL, style="myStyle.Horizontal.TScale")
        self.choose_eraser_size_button.grid(row=1, column=1)

        self.timerLabel = Label(self.root, bg=self.WINDOW_BG, fg=self.CANVAS_BG, font=('Helvatical bold',30))
        self.timerLabel.grid(row=2, column=0, columnspan=4, pady=20)
        self.countdown()

        self.c = Canvas(self.root, bg=self.CANVAS_BG,
                        width=self.DEFAULT_WIDTH, height=self.DEFAULT_HEIGHT)
        self.c.grid(row=3, columnspan=4)

        self.HAS_THREAD = False
        self.setup()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    
    def countdown(self):
        self.TIME_LIMIT -= 1
        if self.TIME_LIMIT > 0:
            self.timerLabel.config(text='<< ' + str(self.TIME_LIMIT) + ' >>')
            if self.TIME_LIMIT <=5:
                self.timerLabel.config(fg="red")
            self.root.after(1000, self.countdown)
        else:
            self.quit()


    
    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_slide.get()
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
        self.line_width = self.choose_size_slide.get()
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
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        save_dir = './saves'
        filename = 'image.png'
        path = os.path.join(cur_dir, save_dir, filename)
        print(path)
        if path:
            img = Image.open(io.BytesIO(ps.encode('utf-8')))
            img.save(path)
    
    def quit(self):
        self.save()
        self.root.destroy()

    def on_closing(self):
        #when press the x button
        self.quit()


if __name__ == '__main__':
    Paint()
