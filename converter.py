from PIL import Image
import imagecodecs
import pillow_avif
import os.path
import time
import PIL
import os


def check_time(start_time):
    elapsed_time = time.time() - start_time
    rounded_time = round(elapsed_time)
    minutes = (rounded_time % 3600) // 60
    seconds = rounded_time % 60
    return f"Время работы: {minutes} минут, {seconds} секунд(ы)\nКонвертация завершена.\n"


def check_file(file, from_):
    if str(file).endswith(from_.lower()) or (str(file).endswith(from_.upper())):
        return True
    return False


def format_error(file, from_, in_):
    file_format = os.path.splitext(file)[1]
    return (f'Неверный формат файла. Выбран формат конвертации с {from_} в {in_},'
            f' у файла в данный момент формат {str(file_format)}') + '\n'


class Converter:
    def __init__(self, files: tuple, type_files: int, delete_file: str):
        self.files = files
        self.type_file = type_files
        self.delete_file = delete_file

    def image_codecs_method(self, file, from_, in_):
        if check_file(file, from_) is True:
            image = imagecodecs.imread(file)
            imagecodecs.imwrite(str(file).replace(from_, in_), image)
            result = self.delete_files(file)
            return f'Конвертация успешно выполнена\n{result}\n'
        else:
            return format_error(file, from_, in_)

    def pillow_method(self, image, file, from_, in_):
        if check_file(file, from_) is True:
            image.save(str(file).replace(f'.{from_}', f'.{in_}'))
            result = self.delete_files(file)
            return f'Конвертация успешно выполнена\n{result}\n'
        else:
            return format_error(file, from_, in_)

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
                try:
                    image = Image.open(file)
                except PIL.UnidentifiedImageError:
                    messages = self.image_codecs_method(file, from_, in_)
                    result_messages += messages
                else:
                    messages = self.pillow_method(image, file, from_, in_)
                    result_messages += messages
        return result_messages
