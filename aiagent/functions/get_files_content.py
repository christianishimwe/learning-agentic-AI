
from config import settings
import os


def get_file_content(working_directory, file_path):
    # first find if this file is withing the working directoru
    # build the absolute path of the file
    working_directory_abs = os.path.abspath(working_directory)
    # join with the file path
    target_file = os.path.normpath(
        os.path.join(working_directory_abs, file_path))
    # check if the target file is a subdirectory of the working_directory_abs
    if not os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs:
        return (
            f"Error: cannot read {file_path} as it is outside the working directory.")

    # check if this is even an existng file
    if not os.path.isfile(target_file):
        return (f"Error: {file_path} is not a file.")
    # now let's try to read
    try:
        with open(target_file, "r") as f:
            content = f.read(settings.max_chars)
            # check if the content was too long
            if f.read(1):
                content += f"\n... File {file_path} content truncated as it exceeds the maximum return limit of {settings.max_chars} characters."
            return content
    except Exception as e:
        return f"Error {str(e)}"
