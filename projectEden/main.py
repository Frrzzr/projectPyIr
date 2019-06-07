import os
import sys
import nltk
import re


file = r"C:\Python34\README.txt"
words = sorted(set(open(file, 'r').read().split()))
suffixes = sorted(set(open("affix\\suffixes", 'r').read().upper().split()))
prefixes = sorted(set(open('affix\\prefixes', 'r').read().upper().split()))
stopwords = sorted(set(open('affix\\stopwords').read().upper().split()))
stemmed = []

# keep verb to be in the list


class Stemmiser:
    def __init__(self, full_file_path):
        self.FullFilePath = full_file_path
        size = full_file_path.find('.') + 1
        self.FileType = full_file_path[size:]
        self.List = list()

    def stem(self):
        if self.FileType == 'txt':
            self.List = self.reader()
            write_to_file(self.List, 'original')
            self.remove_stop_word()
            self.remove_suffixes()

    def remove_stop_word(self):
        for word in sorted(set(stopwords)):
            for w in sorted(set(self.List)):
                if word == w or len(w) == 1:
                    self.List.remove(w)
        write_to_file(self.List, 'removed_stop')

    def remove_suffixes(self):
        for word in sorted(set(self.List)):
            for suffix in sorted(set(suffixes)):
                if len(word) <= len(suffix): continue
                if word.endswith(suffix):
                    word = word[:word.find(suffix)]
            stemmed.append(add_necessary_suffixes(word, suffix))

    def reader(self): return re.sub("[^a-zA-Z]", " ", open(self.FullFilePath, 'r').read().upper()).split()


def add_necessary_suffixes(wd, suf):
    if suf == 'ED' or suf == 'ES' or suf == 'IES':
        print(wd)
        wd = wd + 'Y'
    if suf == 'ING':
        print(wd)
        wd = wd + 'E'
    return wd


def write_to_file(lists, name):
    if not os.path.exists('affix/output/'): os.mkdir('affix/output/')
    with open('affix/' + 'output/' + name + '.txt', 'w') as f:
        for word in sorted(set(lists)):
            f.write(word + '\n')


def print_word_list():
    for ls in stemmed:
        print(ls, )


stem = Stemmiser("C:\Python34\LICENSE.txt")
stem.stem()
write_to_file(stemmed, 'stemmed')
# print_word_list()
