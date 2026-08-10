from functions.get_file_content import get_file_content


def main():
    print(
        f"test 1: {get_file_content("omega_working_directory", "functions")}\n")
    print(
        f"test 2: {get_file_content("omega_working_directory", "functions/get_files_info.py")}\n")
    print(
        f"test 3: {get_file_content("omega_working_directory", "pkg/dummy.txt")}\n")
    print(f"test 4: {get_file_content("omega_working_directory", "main.py")}")


main()
