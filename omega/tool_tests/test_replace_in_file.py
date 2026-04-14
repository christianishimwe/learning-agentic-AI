from functions.replace_in_file import replace_in_file


def main():
    print(
        f"test 1: {replace_in_file("calculator", "pkg/dummy_calculator.py", "# just a silly", 1, 1)}")
    print(f"test 2: {replace_in_file("calculator", "pkg/dummy_calculator.py", """        self.operators = {\n              "+": lambda a, b: a + b,\n""", 4, 5)}")
    print(
        f"test 3: {replace_in_file("calculator", "pkg/dummy_calculator.py", "class Calculator:", 2, 2)}")


main()
