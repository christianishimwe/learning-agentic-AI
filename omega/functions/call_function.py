import os
from google.genai import types
from .get_files_info import get_files_info
from .get_file_content import get_file_content
from .run_python_file import run_python_file
from .write_file import write_file
from .search_in_files import search_in_files
from .think import think
from .replace_in_file import replace_in_file

# Anchored to the package location (not the caller's cwd) so the sandbox is
# found no matter which directory `omega` is launched from.
WORKING_DIRECTORY = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "..", "omega_working_directory")
)


def call_function(function_call):
    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file,
        "search_in_files": search_in_files,
        "think": think,
        "replace_in_file": replace_in_file
    }
    # let's check if the function is in the map
    function_name = function_call.name or ""  # will be "" if name is None
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response=f"Error" f"Unknown function: {function_name}"
                )
            ],
        )
    # let's make our copy of the args
    # this way if the args is NOne, the dict will be empty and not throw an error
    our_args = dict(function_call.args) if function_call.args else {}
    # let's now set the working directory (not needed for think)
    if function_name != "think":
        our_args["working_directory"] = WORKING_DIRECTORY
    # now let's call the function
    function_result = function_map[function_name](
        **our_args)  # this result will be a string
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result}
            )
        ]
    )
