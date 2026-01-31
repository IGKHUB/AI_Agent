import os
import subprocess
from dotenv import load_dotenv
from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file relative to the working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_abs = os.path.abspath(os.path.join(working_directory, file_path))

        # Ensure file is inside working directory
        if not file_abs.startswith(working_dir_abs + os.sep):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Ensure file exists and is a regular file
        if not os.path.isfile(file_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Ensure it's a Python file
        if not file_abs.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build command
        command = ["python", file_abs]
        if args:
            command.extend(args)

        # Run subprocess
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )

        output_parts = []

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"