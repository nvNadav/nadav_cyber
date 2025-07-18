from pathlib import Path
# d:\Videos\Lockdownprotocol

def traverse_files(file_path):
    for path in Path(file_path).iterdir:
        if path.is_dir():
            flag = traverse_files(path)
        else:
            flag = other_func(path)
        if not flag:
            return False
        
    return True


def other_func(file):
    pass