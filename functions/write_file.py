import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file relative to the working directory, creating it if necessary",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)


def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_abs = os.path.abspath(os.path.join(working_directory, file_path))

        # Ensure path is inside working directory
        if not file_abs.startswith(working_dir_abs + os.sep):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Reject existing directories
        if os.path.isdir(file_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Ensure parent directories exist
        parent_dir = os.path.dirname(file_abs)
        os.makedirs(parent_dir, exist_ok=True)

        # Write file
        with open(file_abs, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"