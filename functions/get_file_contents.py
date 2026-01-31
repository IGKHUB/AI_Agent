import os
from config import MAX_CHARS
from dotenv import load_dotenv
from google import genai
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the contents of a file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_abs = os.path.abspath(os.path.join(working_directory, file_path))

        if not file_abs.startswith(working_dir_abs + os.sep):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Ensure it exists and is a regular file
        if not os.path.isfile(file_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read file safely
        with open(file_abs, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {e}"