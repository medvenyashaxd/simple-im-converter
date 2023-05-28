from PIL import Image
import pillow_avif
import os
import os.path


class Converter:
    def __init__(self, files: tuple, type_files: int, delete_file: str):
        self.files = files
        self.type_file = type_files
        self.delete_file = delete_file
        if self.type_file == 1:
            self.convert_file('avif', 'png')
        if self.type_file == 2:
            self.convert_file('webp', 'png')

    def delete_files(self, file):
        if self.delete_file == 'on':
            try:
                os.remove(file)
                print('Удаление исходного файла успешно выполнено')
            except:
                print('Ошибка удаления исходного файла ' + str(file))

    def convert_file(self, from_, in_):
        for file in self.files:
            if os.path.exists(file):
                image = Image.open(file)
                if str(file).endswith(from_.lower()) or (str(file).endswith(from_.upper())):
                    image.save(str(file).replace(f'.{from_}', f'.{in_}'))
                    print('Конвертация успешно выполнена')
                    self.delete_files(file)
                else:
                    file_format = os.path.splitext(file)[1]
                    print(f'Неверный формат файла. Выбран формат конвертации с {from_} в {in_},'
                          f' у файла в данный момент формат {str(file_format)}')
            else:
                print('Файл не существует', file)


