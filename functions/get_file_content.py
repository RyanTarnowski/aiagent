import os
from dotenv import load_dotenv

def get_file_content(working_directory, file_path):
    try:
        load_dotenv()
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        max_chars = int(os.environ.get("MAX_CHARS"))

        with open(target_file, 'r') as file:
            content = file.read(max_chars)

            if file.read(1):
                content += f'[...File "{file_path}" truncated at {max_chars} characters]'
                                
        return content

    except Exception as e:
        return f'Error: "{e}"'