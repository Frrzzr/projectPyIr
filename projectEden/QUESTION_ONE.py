import re
import sys


class QuestionOne:

    def __init__(self):
        self.word_list = list()
        self.count = {}
        self.tp = []
        self.checked = []
        try:
            file = input("enter file name: ")
            file_open = open(file, 'r').read()
            filter_word = re.sub('[^A-Za-z0-9]', ' ', file_open)
            self.word_list = filter_word.split()
        except FileNotFoundError as Msg:
            print(str(Msg))
        self.indexer()
        self.sort_index()
        # return self.word_list

    def indexer(self):
        for w in self.word_list:
            if w not in self.count.keys():
                self.count[w] = 1
            else:
                self.count[w] += 1

    # simple bubble sort
    def sort_index(self):
        tp = [(w, c) for w, c in self.count.items()]
        for index in range(len(self.count.items())):
            for idx in range((len(self.count.items()) + 1) - index):
                try:
                    if tp[idx][1] < tp[idx + 1][1]:
                        temp = tp[idx]
                        tp[idx] = tp[idx + 1]
                        tp[idx + 1] = temp
                except IndexError as _:
                    pass
            self.tp = tp
        return None

    def print_tp(self):
        for ls in self.tp:
            print(ls[0], ls[1], sep='\t\t')
        return None


while True:
    indexer = QuestionOne()
    indexer.print_tp()
    YesNo = input('\ndo you want to continue: ')
    if len(YesNo) > 0:
        if YesNo != 'yes' and YesNo != 'y' and YesNo != 'Y' \
                and YesNo != 'YES':
            print("terminating...")
            sys.exit(0)
