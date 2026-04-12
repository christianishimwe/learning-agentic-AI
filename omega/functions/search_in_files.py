import os
import re
from google.genai import types


def search_in_files(working_directory, pattern, directory="."):
    '''
    This function searches for a pattern. It scans through all files both nested and not nested in the directory,
    and finds which lines have the requested patterns of strings. When it finds the patterns
    it will return a list of
    '''
    try:
        # let's first validate if this directory is within the walking directory
        working_directory_abs = os.path.abspath(working_directory)
        # connect them
        target_dir = os.path.normpath(
            os.path.join(working_directory_abs, directory))
        # if this path is outside the working directory
        if not os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs:
            return f"Error: Cannot search files in this directry since this directory is outside the working directory"

        # if this is not even a directory
        if not os.path.isdir(target_dir):
            return f"Error: Cannnot serach files since this is not a valid directory"

        # let's find where it is contained
        output_string = ""
        # common files we may want to search from
        text_extensions = {".py", ".txt", ".json", ".html", ".css", ".js"}
        for dirpath, _, filenames in os.walk(target_dir):
            if any(forbid in dirpath for forbid in ['__pycache__', "env"]):
                continue  # skip the pycache
            # open each file
            for filename in filenames:
                # check if this is a file that we may want to search from
                if not any(filename.endswith(end_ext) for end_ext in text_extensions) or filename == ".env":
                    continue
                with open(os.path.join(dirpath, filename), 'r') as f:
                    for line_number, line in enumerate(f, start=1):
                        if re.search(pattern, line):
                            output_string += f"- file_path: {os.path.relpath(os.path.join(dirpath, filename), working_directory_abs)}, line_number: {line_number}, line_content: {line.strip()}"

        # if no matches were found
        if not output_string:
            return f"No lines match the pattern {pattern} in the all files nested in directory {directory}"
        return f"Matches were found:\n{output_string}"

    except Exception as e:
        return f"Error: {str(e)}"


schema_search_in_files = types.FunctionDeclaration(
    name="search_in_files",
    description="this function searches in all files (including those nested in directories) contained in the directory provided, relative to the working directory. finds the requested pattern line by line in each file, and returns line number, file_path, and line_content of where this pattern was found",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "pattern": types.Schema(
                type=types.Type.STRING,
                description="the regex pattern or a plain string being searched for"
            ),
            "directory": types.Schema(
                type=types.Type.STRING,
                description="the directory being searched from. default is the working directory"
            )
        },
        required=["pattern"]
    )
)
