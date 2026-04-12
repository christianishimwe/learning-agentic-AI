from functions.run_python_file import run_python_file


def main():
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "main.py", args=["3 + 5"]))
    print(run_python_file("calculator", "../main.py"))
    print(run_python_file("calculator", "non_existent.py"))
    print(run_python_file("calculator", "lorem.txt"))


main()
