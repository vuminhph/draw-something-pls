from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfile, asksaveasfilename
from tkinter import messagebox
import tkinter.ttk as ttk
import io
from tkinter.tix import WINDOW
from PIL import Image


class Paint():
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'
    DEFAULT_WIDTH = 576
    DEFAULT_HEIGHT = 576
    CANVAS_BG = 'white'
    WINDOW_BG = '#17202A'
    LINE_WIDTH_OFFSET = 3
    ERASER_WIDTH_OFFSET = 13
    TIME_LIMIT = 30

    # Called when an instance of the class is created
    def __init__(self):
        self.__root = Tk()
        self.__root.geometry("576x760")
        self.__root.title("Paint")
        self.__root.configure(bg=self.WINDOW_BG)
        self.__root.resizable(False, False)

        self.__style = ttk.Style()
        self.__style.configure("myStyle.Horizontal.TScale",
                             background=self.WINDOW_BG)

        self.__pen_button = Button(
            self.__root, height=1, width=7, bg='#eba134', text='Pen', command=self.__use_pen, font='Consolas')
        self.__pen_button.grid(row=0, column=0, pady=8)

        self.__eraser_button = Button(
            self.__root, height=1, width=7, bg='#de7c7c', text='Eraser', command=self.__use_eraser, font='Consolas')
        self.__eraser_button.grid(row=0, column=1)

        self.__color_button = Button(
            self.__root, height=1, width=7, bg='#8ad190', text='Color', command=self.__choose_color, font='Consolas')
        self.__color_button.grid(row=0, column=2)

        self.__reset_button = Button(
            self.__root, height=1, width=7, bg='#815f96', text='Clear', command=self.__clear_all, font='Consolas')
        self.__reset_button.grid(row=0, column=3)

        # self.save_button = Button(self.__root, height=1, width=4, bg='#e8b443', text='Finish', command=self.quit)
        # self.save_button.grid(row=0, column=4)

        self.__choose_size_slide = ttk.Scale(
            self.__root, from_=1, to=10, orient=HORIZONTAL, style="myStyle.Horizontal.TScale")
        self.__choose_size_slide.grid(row=1, column=0, pady=10)

        self.__choose_eraser_size_button = ttk.Scale(
            self.__root, from_=1, to=10, orient=HORIZONTAL, style="myStyle.Horizontal.TScale")
        self.__choose_eraser_size_button.grid(row=1, column=1)

        self.__timerLabel = Label(
            self.__root, bg=self.WINDOW_BG, fg=self.CANVAS_BG, font=('Consolas bold', 20))
        self.__timerLabel.grid(row=2, column=0, columnspan=4, pady=5)
        self.countdown()

        self.__canvas = Canvas(self.__root, bg=self.CANVAS_BG,
                        width=self.DEFAULT_WIDTH, height=self.DEFAULT_HEIGHT)
        self.__canvas.grid(row=3, columnspan=4)

        self.kw = StringVar()
        self.__keyword = Label(self.__root, textvariable=self.kw, bg=self.WINDOW_BG, fg=self.CANVAS_BG, font='Consolas 20 bold')
        self.__keyword.grid(row=4, columnspan=4)

        self.HAS_THREAD = False
        self.__setup()
        self.__root.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.__root.mainloop()

    def countdown(self):
        self.TIME_LIMIT -= 1
        if self.TIME_LIMIT > 0:
            self.__timerLabel.config(text='<< ' + str(self.TIME_LIMIT) + ' >>')
            if self.TIME_LIMIT <= 5:
                self.__timerLabel.config(fg="red")
            self.__root.after(1000, self.countdown)
        else:
            self.__quit()

    def __setup(self):
        self.__old_x = None
        self.__old_y = None
        self.__line_width = self.__choose_size_slide.get()
        self.__eraser_width = self.__choose_eraser_size_button.get()
        self.__color = self.DEFAULT_COLOR
        self.__eraser_on = False
        self.__active_button = self.__pen_button
        self.__canvas.bind('<B1-Motion>', self.__paint)
        self.__canvas.bind('<ButtonRelease-1>', self.__reset)

    def __use_pen(self):
        self.__eraser_on = False
        self.__activate_button(self.__pen_button)

    def __choose_color(self):
        self.__color = askcolor(color=self.__color)[1]

    def __use_eraser(self):
        self.__activate_button(self.__eraser_button, eraser_mode=True)

    def __clear_all(self):
        temp_button = self.__active_button
        self.__activate_button(self.__reset_button, eraser_mode=False)
        self.__canvas.delete('all')
        self.__reset_button.config(relief=RAISED)
        self.__activate_button(temp_button, eraser_mode=self.__eraser_on)

    def __activate_button(self, some_button, eraser_mode=False):
        self.__active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.__active_button = some_button
        self.__eraser_on = eraser_mode

    def __paint(self, event):
        self.__line_width = self.__choose_size_slide.get()
        paint_color = self.__canvas["bg"] if self.__eraser_on else self.__color
        if self.__old_x and self.__old_y:
            if self.__eraser_on:
                self.__canvas.create_line(self.__old_x, self.__old_y, event.x, event.y,
                                   width=self.__line_width+self.ERASER_WIDTH_OFFSET, fill=paint_color,
                                   capstyle=ROUND, smooth=TRUE, splinesteps=36)
            else:
                self.__canvas.create_line(self.__old_x, self.__old_y, event.x, event.y,
                                   width=self.__line_width+self.LINE_WIDTH_OFFSET, fill=paint_color,
                                   capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.__old_x = event.x
        self.__old_y = event.y

    def __reset(self, event):
        self.__old_x, self.__old_y = None, None

    def __save(self):
        # path = './Pictures/'
        ps = self.__canvas.postscript(colormode='color')
        # filename = asksaveasfilename(defaultextension='.jpg')
        save_dir = './saves'
        filename = 'image.png'
        path = save_dir + '/' + filename
        print(path)
        if path:
            img = Image.open(io.BytesIO(ps.encode('utf-8')))
            img.save(path)

    def __quit(self):
        self.__save()
        self.__root.destroy()

    def __on_closing(self):
        # when press the x button
        self.__quit()


if __name__ == '__main__':
    Paint()