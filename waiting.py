from tkinter import *
from tkinter import font
from tkinter import ttk

class Waiting:
	# constructor method
	def __init__(self):
		self.__wait_window = Tk()

		# Main wait window
		self.__wait_window.title("Please wait...")
		self.__wait_window.resizable(width=False,
									 height=False)
		self.__wait_window.configure(width=500,
									 height=200)

		# Label
		self.__label = Label(self.__wait_window,
							 text="Waiting for other players...",
							 font="Tamoha 14 bold")
		self.__label.place(relwidth=1,
						   relheight=0.2)

		# Waiting logo
		self.__frame_count = 8
		self.__wait_logo = [PhotoImage(file='./images/waiting.gif',
									format='gif -index %i' %(i))
									for i in range(self.__frame_count)]
		self.__wait_logo_label = Label(self.__wait_window)
		self.__wait_logo_label.place(relheight=0.5,
									 relwidth=1,
									 rely=0.25)
		
		# Countdown placement
		self.__timer = StringVar()
		self.__timer.set("30s") # The countdown timer
		self.__countdown_timer = Label(self.__wait_window,
										textvariable=self.__timer,
										font="Helvetica 14")
		self.__countdown_timer.place(relwidth=1,
									 relheight=0.25,
									 rely=0.75)

		# Set the main loop
		self.__wait_window.after(0, self.__update_frame, 0)
		self.__wait_window.mainloop()

	def __update_frame(self, i):
		frame = self.__wait_logo[i]
		i += 1
		if i == self.__frame_count:
			i = 0
		self.__wait_logo_label.configure(image=frame)
		self.__wait_window.after(100, self.__update_frame, i)
		
wait = Waiting()