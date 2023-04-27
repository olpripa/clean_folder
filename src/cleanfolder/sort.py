from pathlib import Path
import sys
import os
import shutil
from src.cleanfolder.normalize import normalize

# with destination folders and known extensions

dict_groups = {"images": ['jpeg', 'jpg', 'bmp', 'gif', 'tiff', 'png'],
               "documents": ['csv', 'doc', 'docx', 'pdf', 'ppt', 'pptx', 'rtf', 'xls', 'xlsx', 'txt'],
               "audio": ['aac', 'amr', 'mp3', 'wav', 'wma', 'wav'],
               "video": ['avi', 'mov', 'mp4', 'mpeg', 'mkv'],
               "archives": ['zip', 'gz', 'tar']}

# Lists of filenames to return
dict_files_name = {"images": [],
                   "documents": [],
                   "audio": [],
                   "video": [],
                   "archives": [],
                   "others": []}


# Lists (set) of file extensions to return
ext_known = set()
ext_unknown = set()

cur_dir = Path('')

# List of folders to ignore


def folder_to_ignore(cur_dir, dict_groups):
    list_f = []
    for k in dict_groups:
        list_f.append(Path((cur_dir), str(k)))
    return list_f

# номарлізуємо та переносимо файли по групам
def fd_rename_and_move(element_path):
    global dict_files_name, ext_known, ext_unknown
    target = None

    if element_path.is_dir():
        # Delete empty directory
        if len(os.listdir(element_path)) == 0:
            shutil.rmtree(element_path)
            return element_path.parent
        else:
            target = Path(element_path.parent, normalize(element_path.name))
            


    if element_path.is_file():
        
        ext = element_path.suffix
        # формуємо шлях призначення
        target = Path(element_path.parent, normalize(element_path.name.rstrip(ext)) + ext)
        unknown = True
        for group in dict_groups:
            if element_path.suffix.lstrip('.').lower() in dict_groups[group]:
                unknown = False
                # Заповнюємо список файлів по групам
                dict_files_name[group].append(normalize(element_path.name.rstrip(ext)) + ext)
                # Заповнюємо множину відомих розширень
                ext_known.add(ext)
                # змінюємо шлях призначення
                target = Path(cur_dir, str(group), normalize(element_path.name.rstrip(ext)) + ext)
                # створюємо папки по групам
                dir_to = cur_dir / group 
                dir_to.mkdir(exist_ok=True)
        if unknown:
            ext_unknown.add(ext)
    
    return fd_conflict(element_path, target)


def fd_conflict(element_path, target):
    
    try:
        ext = element_path.suffix
        if element_path.is_dir():
            return element_path.rename(str(target))
        elif element_path.suffix.lstrip('.').lower() in dict_groups['archives']:
            target_arch = Path(str(target).rstrip(ext))
            shutil.unpack_archive(element_path, target_arch)

        elif element_path.is_file():
            shutil.move(element_path, target)

    except FileExistsError:
        if element_path.is_dir():
            target = Path(str(target).rstrip(ext) + '_')
            return element_path.rename(str(target))
        
        elif element_path.is_file():
            target = Path(str(target).rstrip(ext) + '_' + ext)
            fd_conflict(element_path, target)

        
def parse_folder_recursion(path):
    # recursion through directories
    for element_path in path.iterdir():
        
        if element_path.is_dir() and element_path not in folder_to_ignore(cur_dir, dict_groups):
            element_path = fd_rename_and_move(element_path)
            parse_folder_recursion(element_path)  # рекурсія
        else:
            fd_rename_and_move(element_path)

def main():
    global cur_dir
    cur_dir = Path(sys.argv[1])
    if os.path.exists(cur_dir) and cur_dir.is_dir():
        print(f'Скрипт {__name__} по сортуванню файлів в папці {cur_dir} запущено')
        parse_folder_recursion(cur_dir)
        print(f'Файли по групам {dict_files_name} \n Знайдено відомі розширення {ext_known} \n невідоімі розширення {ext_unknown}')
    else:
        print(f'папку {cur_dir} не знайдено')
    

if __name__ == "__main__":
    main()