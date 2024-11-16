import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

def create_directory(path):
    """Створює директорію, якщо її ще немає."""
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        print(f"Помилка створення директорії '{path}': {e}")

def copy_file(file_path, target_dir):
    """Копіює файл до відповідної папки за розширенням."""
    try:
        extension = os.path.splitext(file_path)[1][1:]  # Отримуємо розширення без точки
        if not extension:  # Пропускаємо файли без розширення
            return
        
        target_path = os.path.join(target_dir, extension)
        create_directory(target_path)
        shutil.copy2(file_path, target_path)
        print(f"Файл '{file_path}' скопійовано до '{target_path}'.")
    except Exception as e:
        print(f"Помилка під час копіювання файлу '{file_path}': {e}")

def process_directory(source_dir):
    """Обробляє директорію та повертає список файлів для копіювання."""
    files_to_copy = []
    try:
        for root, _, files in os.walk(source_dir):
            for file in files:
                files_to_copy.append(os.path.join(root, file))
    except Exception as e:
        print(f"Помилка обробки директорії '{source_dir}': {e}")
    return files_to_copy

def main():
    # Отримуємо шляхи
    if len(sys.argv) < 2:
        print("Використання: python script.py <джерельна_директорія> [цільова_директорія]")
        return
    
    source_dir = sys.argv[1]
    target_dir = sys.argv[2] if len(sys.argv) > 2 else "dist"

    if not os.path.exists(source_dir):
        print(f"Джерельна директорія '{source_dir}' не існує.")
        return

    create_directory(target_dir)

    # Етап 1: Отримуємо список файлів
    print("Отримання списку файлів...")
    files_to_copy = process_directory(source_dir)
    if not files_to_copy:
        print(f"У директорії '{source_dir}' не знайдено файлів для копіювання.")
        return
    
    # Етап 2: Копіюємо файли у потоках
    print("Копіювання файлів...")
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(copy_file, file, target_dir): file for file in files_to_copy}
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Помилка під час копіювання: {e}")

    print(f"Файли успішно відсортовано в директорії '{target_dir}'.")

if __name__ == "__main__":
    main()
