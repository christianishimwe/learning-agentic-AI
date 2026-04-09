from functions.get_files_content import get_file_content


def main():
    print(f"test 1: {get_file_content("calculator", "functions")}\n")
    print(f"test 2: {get_file_content("calculator", "pkg")}\n")
    print(f"test 3: {get_file_content("calculator", "pkg/calculator.py")}\n")


main()
