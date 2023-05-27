from converter import Converter
from tkinter import filedialog
from PIL import Image
import customtkinter
import tkinter


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
        self.right_bar_frame.grid(row=0, column=2,  pady=(6, 0))

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
            Converter(self.files, type_file, delete_file)
        else:
            print('Файл(ы) для конвертации не выбран(ы)')

    def open_files(self):
        self.files = filedialog.askopenfilenames()
        if len(self.files) != 0:
            self.text_loger.delete('1.0', 'end')
            text = 'Выбранные файлы на конвертацию:\n'
            filepath_print = text + str(self.files).replace(',', ',\n')
            self.text_loger.insert('1.0', text=filepath_print)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.logo_image = customtkinter.CTkImage(Image.open('./icon/logo.ico'), size=(26, 26))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.title('Одна секунда конвертер')
        self.my_frame = MyFrame(master=self, height=450, width=600, corner_radius=0, fg_color="transparent")
        self.my_frame.grid(row=0, column=0, sticky="nsew")


if __name__ == '__main__':
    app = App()
    app.iconbitmap('./icon/logo.ico')
    app.resizable(False, False)
    app.mainloop()
