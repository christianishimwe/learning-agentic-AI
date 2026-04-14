from functions.get_files_info import get_files_info
import os


def main():
    print(get_files_info("omega_working_directory", "."))
    print(get_files_info("omega_working_directory", "pkg"))
    print(get_files_info("omega_working_directory", "/bin"))
    print(get_files_info("omega_working_directory", "../"))


main()
