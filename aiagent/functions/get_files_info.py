import os
from google.genai import types


def get_files_info(working_directory=".", directory="."):
    '''
    we are making an assumption that
    working_direcory: comes relative to the current directory
    directory: comes relative to the workoing_directory
    '''
    try:
        working_directory_abs = os.path.abspath(working_directory)
        # try to join the dicctory
        target_dir = os.path.normpath(
            os.path.join(working_directory_abs, directory))

        # check if the target_dir is a subdirectory of the working_directory_abs
        if not os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs:
            return (
                f"Error: cannot list {directory} as it is outside the working directory.")

        # check if this is even an existing direcotyr or an existing file
        if not os.path.isdir(target_dir):
            return (f"Error: {directory} is not a directory.")
        # list the files in the directory
        files = os.listdir(target_dir)
        output_str = ""
        for file in files:
            full_path = os.path.join(target_dir, file)
            output_str += f"- {file}: file_size={os.path.getsize(full_path)} bytes, is_dir=f{os.path.isdir(full_path)}\n"
        return output_str
    except Exception as e:
        return f"Error: {str(e)}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and direcotory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working drectory",
            ),
        },
        required=["directory"],
    ),
)
