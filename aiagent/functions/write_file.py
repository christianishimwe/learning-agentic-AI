import os


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
