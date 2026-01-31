import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        items=os.listdir(target_dir)
        result_lines = []
        for item in items:
            item_path = os.path.join(target_dir, item)
            is_dir = os.path.isdir(item_path)
            size = os.path.getsize(item_path) if not is_dir else 0
            result_lines.append(f'- {item}:, file_size={size} bytes, is_dir={is_dir}')

        dir_display = directory if directory != "." else "current directory"
        result_header = f"Result for '{directory}' directory:" if directory != "." else "Result for current directory:"
        return f"{result_header}\n  " + "\n  ".join(result_lines)

    except Exception as e:
        return f"Error: {str(e)}"