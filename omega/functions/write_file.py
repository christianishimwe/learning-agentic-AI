import os
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        # first create an abolsute working direcotyr
        working_directory_abs = os.path.abspath(working_directory)
        # now join with the file path
        target_file = os.path.normpath(
            os.path.join(working_directory_abs, file_path))
        # check if the target file is a subdirectory of the working_directory_abs
        if not os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs:
            return (
                f"Error: cannot write to {file_path} as it is outside the working directory.")
        # may this is an esisting direcotry

        if os.path.isdir(target_file):
            return f"Error: cannot write to {file_path} as it is an existing directory."
        # first create the missing directories
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        # now write to the file
        with open(target_file, "w") as f:
            f.write(content)

        return f"Successfully wrote to {file_path} ({len(content)} characters)."
    except Exception as e:
        return f"Error: {str(e)}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the provided content to a specified file path relative to the working directory. If the file or its parent directories do not exist, they will be created. will return an error if the target file path is outside the working directory or if it points to an existing directory and not a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write the content to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the specified file",
            ),
        },
    ),
)
