import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{target_dir}" is not a directory'
        
        files_info = ""

        for item in os.listdir(target_dir):
            item_full_path = os.path.join(target_dir, item)
            files_info += f"- {item}: file_size={os.path.getsize(item_full_path)} bytes, is_dir={os.path.isdir(item_full_path)} \n"

        return files_info

    except Exception as e:
        return f'Error: "{e}"' 