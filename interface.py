from converter import Converter, print_time
from tkinter import filedialog
from PIL import Image
import customtkinter
import threading
import tkinter
import time

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")


class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(1, weight=1)
        self.files = None

        # Text box for result or error messages
        self.text_loger = customtkinter.CTkTextbox(
            self, corner_radius=0,
            height=400, width=800
        )
        self.text_loger.grid(
            row=0, column=1,
            padx=(5, 0), pady=(5, 0)
        )
        self.text_loger.insert("end", "Выбранные файлы на конвертацию:\n")

        self.choose_file_button = customtkinter.CTkButton(
            self, text="Выбрать файл(ы)",
            corner_radius=0, fg_color="#3f4544",
            text_color="#faf7f7", command=self.open_files,
        )
        self.choose_file_button.grid(
            row=1, column=1,
            padx=(50, 0), pady=(8, 0)
        )

        self.convert_button = customtkinter.CTkButton(
            self, text="Начать конвертацию",
            corner_radius=0, command=self.send_for_conversion
        )
        self.convert_button.grid(
            row=1, column=1,
            padx=(350, 0), pady=(8, 0)
        )

        self.check_var = customtkinter.StringVar(
            value="on"
        )
        checkbox_for_delete = customtkinter.CTkCheckBox(
            self, text="Удалить исходный файл",
            variable=self.check_var,
            onvalue="on", offvalue="off",
        )
        checkbox_for_delete.grid(
            row=1, column=1,
            padx=(0, 290), pady=(8, 0)
        )

        # right frame
        self.right_bar_frame = customtkinter.CTkFrame(
            self, corner_radius=0
        )
        self.right_bar_frame.grid(
            row=0, column=2,
            pady=(6, 0)
        )

        self.label_type_convert = customtkinter.CTkLabel(
            self.right_bar_frame,
            text_color="#faf7f7",
            text="Формат:"
        )
        self.label_type_convert.grid(
            row=0, column=0, pady=(150, 0)
        )

        self.type_file_var = tkinter.IntVar(value=1)
        self.avif_to_png_button = customtkinter.CTkRadioButton(
            self.right_bar_frame, text="AVIF в PNG",
            variable=self.type_file_var, value=1
        )
        self.webp_to_png_button = customtkinter.CTkRadioButton(
            self.right_bar_frame, text="WEBP в PNG",
            variable=self.type_file_var, value=2
        )
        self.avif_to_png_button.grid(
            row=1, column=0,
            pady=(0, 0), padx=(5, 5)
        )
        self.webp_to_png_button.grid(
            row=2, column=0,
            pady=(8, 170), padx=(5, 5)
        )

    def send_for_conversion(self):
        type_file = self.type_file_var.get()
        delete_file = self.check_var.get()
        if self.files is not None:
            converter = Converter(self.files, type_file, delete_file)

            def send():
                start_time = time.time()
                self.text_loger.insert("end", "\nПроцесс конвертации начался...\n")
                if type_file == 1 and len(self.files) != 0:
                    avif_convert = converter.convert_file("avif", "png")
                    self.text_loger.insert("end", avif_convert)
                    time_convect = print_time(start_time)
                    self.text_loger.insert("end", time_convect)
                elif type_file == 2 and len(self.files) != 0:
                    webp_convert = converter.convert_file("webp", "png")
                    self.text_loger.insert("end", webp_convert)
                    time_convect = print_time(start_time)
                    self.text_loger.insert("end", time_convect)
                else:
                    self.text_loger.insert(
                        "end", "Файл(ы) для конвертации не выбран(ы)\n"
                    )

            threading.Thread(target=send).start()
        else:
            self.text_loger.insert("end", "Файл(ы) для конвертации не выбран(ы)\n")

    def open_files(self):
        """Function for selecting files"""
        self.files = filedialog.askopenfilenames()
        text = "Выбранные файлы на конвертацию:"
        if len(self.files) != 0:
            self.text_loger.delete("1.0", "end")
            print_file_path = text + str(self.files).replace(",", ",\n") + "\n"
            self.text_loger.insert("1.0", text=print_file_path)
        else:
            text = "Выбранные файлы на конвертацию:"
            self.text_loger.delete("1.0", "end")
            self.text_loger.insert("end", text)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.logo_image = customtkinter.CTkImage(
            Image.open("./icon/logo.ico"),
            size=(26, 26)
        )
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.title("One second converter")
        self.my_frame = MainFrame(
            master=self, height=450,
            width=800, corner_radius=0,
            fg_color="transparent"
        )
        self.my_frame.grid(
            row=0, column=0,
            sticky="nsew"
        )


if __name__ == "__main__":
    width = 600
    height = 450
    x = 700
    y = 260
    app = App()
    app.iconbitmap("./icon/logo.ico")
    app.geometry(f"{width}x{height}+{x}+{y}")
    app.resizable(False, False)
    app.mainloop()
