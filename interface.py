from converter import Converter, check_time
from tkinter import filedialog
from PIL import Image
import customtkinter
import threading
import tkinter
import time

customtkinter.set_appearance_mode('Dark')
customtkinter.set_default_color_theme('dark-blue')


class MyFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.files = None
        self.grid_columnconfigure(1, weight=1)

        # main
        self.text_loger = customtkinter.CTkTextbox(self, corner_radius=0, height=400, width=800)
        self.text_loger.grid(row=0, column=1, padx=(5, 0), pady=(5, 0))

        self.button_open_file = customtkinter.CTkButton(self, text='Выбрать файл(ы)', corner_radius=0,
                                                        fg_color='#3f4544',
                                                        text_color='#faf7f7', command=self.open_files)
        self.button_open_file.grid(row=1, column=1, padx=(50, 0), pady=(8, 0))

        self.button_convert = customtkinter.CTkButton(self, text='Начать конвертацию', corner_radius=0,
                                                      command=self.go_to_convert)
        self.button_convert.grid(row=1, column=1, padx=(350, 0), pady=(8, 0))

        self.check_var = customtkinter.StringVar(value="on")
        checkbox = customtkinter.CTkCheckBox(self, text="Удалить исходный файл",
                                             variable=self.check_var, onvalue="on", offvalue="off")
        checkbox.grid(row=1, column=1, padx=(0, 290), pady=(8, 0))

        # right bar
        self.right_bar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.right_bar_frame.grid(row=0, column=2, pady=(6, 0))

        self.label_type_convert = customtkinter.CTkLabel(self.right_bar_frame, text_color='#faf7f7', text='Формат:')
        self.label_type_convert.grid(row=0, column=0, pady=(150, 0))

        self.radio_var = tkinter.IntVar(value=1)
        self.radiobutton_1 = customtkinter.CTkRadioButton(self.right_bar_frame, text="AVIF в PNG",
                                                          variable=self.radio_var, value=1)
        self.radiobutton_2 = customtkinter.CTkRadioButton(self.right_bar_frame, text="WEBP в PNG",
                                                          variable=self.radio_var, value=2)
        self.radiobutton_1.grid(row=1, column=0, pady=(0, 0), padx=(5, 5))
        self.radiobutton_2.grid(row=2, column=0, pady=(8, 170), padx=(5, 5))

    def go_to_convert(self):
        type_file = self.radio_var.get()
        delete_file = self.check_var.get()
        if self.files is not None:
            converter = Converter(self.files, type_file, delete_file)

            def convert_and_get_log():
                start_time = time.time()
                self.text_loger.insert('end', 'Процесс конвертации начался...\n')
                if type_file == 1 and len(self.files) != 0:
                    avif_convert = converter.convert_file('avif', 'png')
                    self.text_loger.insert('end', avif_convert)
                    time_convect = check_time(start_time)
                    self.text_loger.insert('end', time_convect)
                elif type_file == 2 and len(self.files) != 0:
                    webp_convert = converter.convert_file('webp', 'png')
                    self.text_loger.insert('end', webp_convert)
                    time_convect = check_time(start_time)
                    self.text_loger.insert('end', time_convect)
                else:
                    self.text_loger.insert('end', 'Файл(ы) для конвертации не выбран(ы)\n')

            threading.Thread(target=convert_and_get_log).start()

        else:
            self.text_loger.insert('end', 'Файл(ы) для конвертации не выбран(ы)\n')

    def open_files(self):
        self.files = filedialog.askopenfilenames()
        if len(self.files) != 0:
            self.text_loger.delete('1.0', 'end')
            text = 'Выбранные файлы на конвертацию:'
            filepath_print = text + str(self.files).replace(',', ',\n') + '\n'
            self.text_loger.insert('1.0', text=filepath_print)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.logo_image = customtkinter.CTkImage(Image.open('./icon/logo.ico'), size=(26, 26))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.title('Одна секунда конвертер')
        self.my_frame = MyFrame(master=self, height=450, width=800, corner_radius=0, fg_color="transparent")
        self.my_frame.grid(row=0, column=0, sticky="nsew")


if __name__ == '__main__':
    width = 800
    height = 450
    x = 560
    y = 260
    app = App()
    app.iconbitmap('./icon/logo.ico')
    app.geometry(f'{width}x{height}+{x}+{y}')
    app.resizable(False, False)
    app.mainloop()
