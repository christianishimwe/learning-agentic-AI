import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(working_directory_abs, file_path))

        if os.path.commonpath([working_directory_abs, target_file]) != working_directory_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python3", target_file]
        if args:
            command.extend(args)

        result = subprocess.run(
            command, capture_output=True, text=True, cwd=working_directory_abs, timeout=30)

        output_str = ""
        if result.returncode != 0:
            output_str += f"Process exited with code {result.returncode}\n"

        if not result.stdout and not result.stderr:
            output_str += "No output produced"
        else:
            if result.stdout:
                output_str += f"STDOUT:\n{result.stdout}"
            if result.stderr:
                output_str += f"STDERR:\n{result.stderr}"

        return output_str

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file relative to the working directory, with optional command-line arguments, and returns the combined standard output and error produced by the execution.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command-line arguments to pass to the Python file during execution",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
        required=["file_path"],
    ),
)
