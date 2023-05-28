from PIL import Image
import pillow_avif
import os.path
import os


class Converter:
    def __init__(self, files: tuple, type_files: int, delete_file: str):
        self.files = files
        self.type_file = type_files
        self.delete_file = delete_file

    def delete_files(self, file):
        result_messages = 'Исходный файл не удалялся, снята галочка "Удалить исходный файл"'
        if self.delete_file == 'on':
            try:
                os.remove(file)
                return 'Удаление исходного файла успешно выполнено'
            except:
                return 'Ошибка удаления исходного файла: ' + file
        return result_messages

    def convert_file(self, from_, in_):
        result_messages = ""
        for file in self.files:
            if not os.path.exists(file):
                result_messages += 'Файл не существует: ' + file + '\n'
            else:
                image = Image.open(file)
                if str(file).endswith(from_.lower()) or (str(file).endswith(from_.upper())):
                    image.save(str(file).replace(f'.{from_}', f'.{in_}'))
                    delete_result = self.delete_files(file)
                    result_messages += f'Конвертация успешно выполнена\n{delete_result}\n'
                else:
                    file_format = os.path.splitext(file)[1]
                    result_messages += (f'Неверный формат файла. Выбран формат конвертации с {from_} в {in_},'
                                        f' у файла в данный момент формат {str(file_format)}') + '\n'
        return result_messages
