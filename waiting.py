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
									 height=300)

		# Label
		self.__label = Label(self.__wait_window,
							 text="Waiting for other players...",
							 font="Tamoha 14 bold")
		self.__label.place(relwidth=1,
							relheight=0.15)

		# Waiting logo
		self.__wait_logo = PhotoImage(file='./images/waiting.gif',
									format='gif -index 2').subsample(2)
		self.__wait_logo_label = Label(self.__wait_window,
										image=self.__wait_logo)
		self.__wait_logo_label.place(relheight=0.7,
									 relwidth=0.7,
									 relx=0.15,
									 rely=0.15)
		
		# Countdown placement
		timer = "30s" # The countdown timer
		self.__countdown_timer = Label(self.__wait_window,
										textvariable=timer,
										font="Helvetica 14")
		self.__countdown_timer.place(relwidth=1,
									 relheight=0.15,
									 rely=0.85)

		# Set the main loop
		self.__wait_window.mainloop()
		
wait = Waiting()