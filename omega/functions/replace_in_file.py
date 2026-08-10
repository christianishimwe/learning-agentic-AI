import os
from google.genai import types


def replace_in_file(working_directory, filepath, new_content, first_line=1, last_line=None):
    # make sure we are in the right working directory
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(
            os.path.join(working_directory_abs, filepath))
        if not os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs:
            return f"Error: Cannot replace content in this file since file {filepath} is not withing the working directory"
        if not os.path.isfile(target_dir):
            return f"Error: Cannot replace content in this file since file {filepath} doesn't exist"
        if not new_content.endswith("\n"):
            new_content += "\n"
        # now we are ready
        # let's open the file and read it line by line
        content = ""
        with open(target_dir, 'r') as f:
            # let's go line by line
            spotted = False  # check if we already spotted where we want to make the change at
            for line_number, line in enumerate(f, start=1):
                # if this line is within the first line and the last line
                if line_number >= first_line and (last_line is None or line_number <= last_line):
                    if not spotted:
                        content += new_content
                        spotted = True
                        continue
                    else:
                        continue
                content += line
        # write the new content to the file
        with open(target_dir, 'w') as f:
            f.write(content)
    except Exception as e:
        return f"Error: {str(e)}"
    return f"Success: successfuly edited file {filepath} by replacing all content from line {first_line} to including {last_line} with content:{new_content}"


schema_replace_in_file = types.FunctionDeclaration(
    name="replace_in_file",
    description="This function replaces a part of content in a file. it takes in a path to a file, the new content, first line and last line in the file. It will replace all content from (including) the first line to (including) the last line with the new content leaving all other content in the file as it was before",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "filepath": types.Schema(
                type=types.Type.STRING,
                description="the path to the file withing which to replace content",
            ),
            "new_content": types.Schema(
                type=types.Type.STRING,
                description="new content to write. Make sure each line ends with new line character \\n",
            ),
            "first_line": types.Schema(
                type=types.Type.INTEGER,
                description="the first line that represent where the old content to be replaced starts from. By default this will be the first line in the file, line 1"
            ),
            "last_line": types.Schema(
                type=types.Type.INTEGER,
                description="the last line that represents where the old content to be replaced ends at. By default this will be None ot represent that all content from first line specified to end of the file"
            )
        },
        required=["filepath", "new_content"]
    )
)
