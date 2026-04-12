from functions.write_file import write_file


def main():
    '''
    creates a new file dummy.txt in the calculator directory with the content "This is a dummy file."
    '''
    print(write_file("calculator", "dummy.txt", "This is a dummy file."))
    '''
    creates a missing directory "functions" and a new file dummy.txt in the functions directory with the content "This is a dummy file in the functions directory."
    '''
    print(write_file("calculator", "dummy/dummy.txt",
          "This is a dummy file in the functions directory."))
    '''
    restrictes access outside the working directory, should return an error message
    '''
    print(write_file("calculator", "/dummy/dummy.txt",
          "This is a dummy file in the functions directory."))


main()
