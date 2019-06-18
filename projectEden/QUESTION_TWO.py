import os


def main():
    file_path = input("enter file path")
    file_type = input("enter file type")
    search_string = input("enter search string")

    if not (file_path.endswith("/") or file_path.endswith("\\")):
        file_path = file_path + "/"
    if not os.path.exists(file_path):
        file_path = "./"

    for files in os.listdir(path=file_path):
        if files.endswith(file_type):
            fop = open(file_path + files)
            line = fop.readline()
            count = 1
            while line != '':
                found_text = line.find(search_string)
                if found_text != -1:
                    print(files)
                count += 1
                line = fop.read()
            fop.close()
