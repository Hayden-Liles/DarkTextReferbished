import tkinter as tk
import customtkinter

from controllers.MapController import mapController
from controllers.PlayerController import playerController


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.configureWindow()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        self.map_frame = mapController.checkMapExists(self)
        playerController.checkPlayer(self.map_frame)

        # SECTION TESTING LAYOUT
        self.button = customtkinter.CTkButton(self, text="test")
        self.button.grid(row=0, column=0, pady=(
            20, 0), padx=(20, 0), sticky='nw')
        
        # NOTE the binding for keypress event listener
        self.bind('<KeyRelease>', self.keyPress)
        

    def configureWindow(self):
        self.geometry("1000x900")
        self.title("Dark Text")

    def keyPress(self, event):
        key = event.keysym
        if key in ('Up', 'Down', 'Left', 'Right'):
            playerController.movePlayer(key, self.map_frame)



if __name__ == "__main__":
    app = App()
    app.mainloop()