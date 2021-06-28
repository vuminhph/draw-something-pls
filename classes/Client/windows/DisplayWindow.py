from tkinter import messagebox, Toplevel
# from PIL import Image


class DisplayWindow:
    def __init__(self, GUI):
        self._window = Toplevel()
        self._GUI = GUI
        self._game_controller = GUI.get_game_controller()

        self._window.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self._game_controller.logout()
            # self._window.destroy()
            self._window.quit()
            self._GUI.get_game_window().destroy()

    def __del__(self):
        print("Window is destroyed")

    def _close(self):
        self._window.destroy()
