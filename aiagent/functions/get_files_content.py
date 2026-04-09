from functions.get_files_info import get_files_info
from config import settings
import os


def get_file_content(working_directory, file_path):
    # first find if this file is withing the working directoru
