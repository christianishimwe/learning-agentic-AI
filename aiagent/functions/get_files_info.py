import os


def get_files_info(working_directory, directory="."):
    abs_working_directory = os.path.abspath(working_directory)
    if directory == None:
        directory = "."
    abs_directory = os.path.abspath(
        os.path.join(abs_working_directory, directory))

    if not abs_directory.startswith(abs_working_directory):
        return f"Error: Directory '{directory}' is outside the working directory."

    contents = os.listdir(abs_directory)
    result = []
    for content in contents:
        full_path = os.path.join(abs_directory, content)
        is_dir = os.path.isdir(full_path)
        size = os.path.getsize(full_path)
        result.append(
            f"{'dir' if is_dir else 'file'}: {content}, size: {size} bytes"
        )
    return "\n".join(result)
