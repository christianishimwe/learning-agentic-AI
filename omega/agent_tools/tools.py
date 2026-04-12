from google.genai import types
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.search_in_files import schema_search_in_files
available_functions = types.Tool(
    function_declarations=[schema_get_files_info,
                           schema_get_file_content,
                           schema_write_file,
                           schema_run_python_file,
                           schema_search_in_files],
)
