def read_html(path):
    try:
        with open(path, encoding="utf-8") as template:
            return template.read()
    except FileNotFoundError:
        print(f"Файл не найден: {path}")
    except PermissionError:
        print(f"Нет доступа к файлу: {path}")
    except UnicodeDecodeError:
        print(f"Ошибка кодировки при чтении: {path}")
    except OSError as e:
        print(f"Ошибка чтения файла {path}: {e}")
    return None
