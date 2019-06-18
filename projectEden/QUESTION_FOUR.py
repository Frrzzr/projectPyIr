import sys

files = list()
eden = dict()
try:
    n = int(input("enter n: "))
except ValueError:
    print("INTEGER.")


class ClassFinder:

    def __init__(self):
        pass

    @staticmethod
    def add_list(text_list, file_name, tx_line):
        for word in text_list:
            if word not in eden.keys():
                eden[word] = {}
                if file_name not in eden[word].keys():
                    eden[word][file_name] = []
                    eden[word][file_name].append(tx_line)
                else:
                    if tx_line in eden[word][file_name]:
                        continue
                    eden[word][file_name].append(tx_line)
            elif word in eden.keys():
                if file_name not in eden[word].keys():
                    eden[word][file_name] = []
                    eden[word][file_name].append(tx_line)
                else:
                    if tx_line in eden[word][file_name]:
                        continue
                    eden[word][file_name].append(tx_line)
        return None


# C:\Python34\LICENSE.txt
# C:\Python34\NEWS.txt
# C:\Python34\README.txt


def main():
    try:
        import re
        for _ in range(n): files.append(input("enter full path: "))
        print('indexing....')
        for index in range(len(files)):
            with open(files[index]) as file:
                text_line = 1
                text_list = file.readline().upper()
                while text_list != '':
                    ClassFinder.add_list(sorted(text_list.split()), files[index], text_line)
                    text_list = re.sub("[^a-zA-Z]", " ", file.readline().upper())
                    text_line += 1
    except IndexError as Msg:
        print(str(Msg))
    except FileNotFoundError as Msg:
        print('{}'.format(str(Msg)))
        files.clear()
        main()
    except KeyboardInterrupt:
        print("terminating...")
        sys.exit(0)
    return None


main()

try:
    while True:
        query = input("\nenter you query: ").split()
        print('\nquery result\n\t', end='')
        for word in query:
            try:
                print("\n\t" + word)
                for file_name, line in eden[word.upper()].items():
                    print("\n\t\t" + file_name, end="\n\t\t\t")
                    for ln in line:
                        print(str(ln) + ", ", end="")
            except KeyError as Msg:
                print("not found")
        YesNo = input('\ndo you want to continue: ')
        if len(YesNo) > 0:
            if YesNo != 'yes' and YesNo != 'y' and YesNo != 'Y' \
                    and YesNo != 'YES':
                print("terminating...")
                sys.exit(0)
except KeyboardInterrupt:
    print("terminating...")
    sys.exit(0)
