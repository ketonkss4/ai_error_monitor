import os


def get_file_at_path(absolute_path):
    try:
        print(f"Reading file at path: {absolute_path}")
        with open(absolute_path, "r") as file:
            print(f"File read successfully")
            return file.read()
    except FileNotFoundError:
        print(f"File not found at path: {absolute_path}")
        return None
    

def retrieve_directory_contents_hierarchy(absolute_directory_path: str,
                                          include_files: bool = False) -> str:
    exclude_dirs = ['node_modules', 'venv', '__pycache__', '.git', 'outputs']  # List of directories to exclude

    def list_files_recursive(directory: str, prefix: str = '', include_files: bool = True) -> str:
        file_hierarchy = ''
        for item in os.listdir(directory):
            # Skip excluded directories and any directory starting with '.'
            if item in exclude_dirs or item.startswith('.') or item.startswith('_'):
                continue
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path) and include_files:
                file_hierarchy += f"{prefix}{str(item)}\n"
            elif os.path.isdir(item_path):
                file_hierarchy += f"{prefix}{str(item)}/\n"
                file_hierarchy += list_files_recursive(item_path, prefix + '    ', include_files)
        return file_hierarchy

    path = absolute_directory_path

    if path is not None:
        path_str = str(path)
        basename = os.path.basename(absolute_directory_path)
        path_to_directory_from_root = f'{basename}\\{os.path.relpath(path_str, absolute_directory_path)}'
        content_hierarchy = list_files_recursive(path_str, include_files=include_files)
        return f'Path: {path_to_directory_from_root}\n\nContent Hierarchy:\n{content_hierarchy}'
    else:
        return None