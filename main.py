import tkinter
import tkinter.messagebox
import customtkinter
from speedtest import Speedtest

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


def get_results():  # function gets previous test results
    with open('results.txt') as f:
        results = f.readlines()
        return ''.join(results)


class Root(customtkinter.CTk):
    width = 800
    height = 500

    def __init__(self):
        super().__init__()

        self.title("Internet Speed Test")
        self.geometry(f"{Root.width}x{Root.height}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # what happens upon closing the window

        # Window grid setup
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---Left frame---

        self.frame_left = customtkinter.CTkFrame(master=self, width=200, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        # Result frame
        self.label_results = customtkinter.CTkLabel(master=self.frame_left,
                                                    text=get_results(),
                                                    height=470,
                                                    corner_radius=6, fg_color=("white", "gray25"),
                                                    justify=tkinter.CENTER)
        self.label_results.grid(column=0, row=0, padx=15, pady=15)

        # ---Right frame---
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # Configuration of the frame grid
        self.frame_right.rowconfigure((1, 2, 3), weight=1)
        self.frame_right.rowconfigure((0, 4), weight=10)
        self.frame_right.columnconfigure((0, 1, 2), weight=1)

        # Labels
        self.label_speed = customtkinter.CTkLabel(master=self.frame_right,
                                                  text='',
                                                  text_font=("Roboto Medium", -16),
                                                  justify=tkinter.LEFT)
        self.label_speed.grid(row=3, column=1, pady=10, padx=20)

        # Buttons
        self.thread_button = customtkinter.CTkOptionMenu(master=self.frame_right, values=['Multi', 'Single'],
                                                         command=self.change_thread)
        self.thread_button.grid(row=5, column=1, pady=10, padx=20)

        self.start_button = customtkinter.CTkButton(master=self.frame_right, text='Start', command=self.speed_test)
        self.start_button.grid(row=6, column=1, pady=10, padx=20)

        # set default values
        self.thread_button.set('Multi')
        self.thread = 'Multi'

    def on_closing(self):  # ends tkinter session on closing of the window
        self.destroy()

    def change_thread(self, new_value):  # function for changing the speedtest thread option (unfortunately doesn't work because of the limitations of the speedtest module)
        self.thread = new_value
        print(self.thread)

    def speed_test(self):
        test = Speedtest()  # initiates speedtest
        down = round(test.download() / (10 ** 6), 2)
        up = round(test.upload() / (10 ** 6), 2)
        self.label_speed.configure(text=f"Download speed: {down} Mbps\nUpload speed: {up} Mbps")  # updates label to current results
        with open('results.txt', 'a') as f:  # updates file with results
            f.write(f'Download {down} and Upload {up}\n')
        self.label_results.configure(text=get_results())  # refresh of results in tkinter


if __name__ == "__main__":
    root = Root()
    root.mainloop()
