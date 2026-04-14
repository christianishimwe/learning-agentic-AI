
from config import settings
from google.genai import types
import os


def get_file_content(working_directory, file_path, first_line=1, num_lines=None):
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
    content = ""
    try:
        with open(target_file, "r") as f:
            '''
            content = f.read(settings.max_chars)
            # check if the content was too long
            if f.read(1):
                content += f"\n... File {file_path} content truncated as it exceeds the maximum return limit of {settings.max_chars} characters."
            return content
            '''
            count = 0
            for line_number, line in enumerate(f, start=1):
                if num_lines is not None and count >= num_lines:
                    break
                # if this line number is before start line, just skip
                if line_number < first_line:
                    continue
                content += f"line {line_number}:{line}"
                count += 1
                # if we hit more thatn max content we can read
                if len(content) > settings.max_chars:
                    content += f"\n\n ... File {file_path} content truncated as it exceeds the maximum return limit of {settings.max_chars} characters. You read exactly {len(content)} characters"
                    break
        return content
    except Exception as e:
        return f"Error {str(e)}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a specified file relative to the working directory. Will only read the contents from the first line reading a total of num_lines specified. The returned string includes all content with each line tagged with its line number in the file. By default first line is 1 and num_lines is None, so by default the function will read all lines in the file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read the content from, relative to the working directory",
            ),
            "first_line": types.Schema(
                type=types.Type.INTEGER,
                description="the first line to start reading from. the first one is always 1 by default"
            ),
            "num_lines": types.Schema(
                type=types.Type.INTEGER,
                description="number of lines to read from the first line included"
            )
        },
        required=["file_path"],
    ),
)
