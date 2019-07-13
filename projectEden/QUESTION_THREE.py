try:
    import os
    import sys
    import re
    import readConcurrently
    import doc2txt
except ImportError as Msg:
    import os
    import sys
    import re
    import readConcurrently
    pass

# file = r"C:\Python34\README.txt"
# words = sorted(set(re.sub("[^a-zA-Z]", " ", open(file, 'r').read()).upper().split()))

try:
    file_obj = open("affixes\\suffixes", 'r')
    file_str = re.sub('[^a-zA-Z]', " ", file_obj.read())
    file_str = file_str.upper().split()
    suffixes = sorted(set(file_str))
    del file_obj
    del file_str
    file_obj = open('affixes\\preffixes', 'r')
    file_str = re.sub('[^a-zA-Z]', " ", file_obj.read())
    file_str = file_str.upper().split()
    prefixes = sorted(set(file_str))
    del file_obj
    del file_str
    file_obj = open('affixes\\stopwords')
    file_str = re.sub('[^a-zA-Z]', " ", file_obj.read())
    file_str = file_str.upper().split()
    stopwords = sorted(set(file_str))
except FileNotFoundError as Msg:
    print('please include the folder (affixes) from the project directory'.upper())

stemmed = []
temp = []
irregular = dict()


class Stemmiser:
    def __init__(self, full_file_path):
        # print('initializing ' + full_file_path)
        self.FullFilePath = full_file_path
        size = full_file_path.find('.') + 1
        self.FileType = full_file_path[size:]
        self.file_name = full_file_path[full_file_path.rfind("\\") + 1: full_file_path.rfind('.txt')]
        self.List = list()
        # load the dict (irregular) from irregular verb text file
        # print('loading...')
        load_irregular_verb()

    def stem(self):
        # print('stemming...')
        if self.FileType == 'txt':
            self.List = self.remove_verb_to_be(self.reader())
            write_to_file(self.List, self.file_name, 'original')
            # keep verb to be in the list
            # print('removing vrb to be from the stop word lists')
            remove_to_be()
            self.remove_stop_word()
            self.remove_suffixes()

    def remove_stop_word(self):
        # print('removing stop word from the file list')
        for word in stopwords:
            for w in self.List:
                if word == w or len(w) == 1:
                    self.List.remove(w)
        # print('writing to file removed_stop')
        write_to_file(self.List, self.file_name, 'removed_stop')

    def remove_suffixes(self):
        # print('removing suffixes....')
        for word in self.List:
            if word == 'be'.upper():
                stemmed.append('BE')
                continue
            for (key, value) in irregular.items():
                if word == key or word in value:
                    if word == key:
                        # print('word found in the irregular dict key verb list ' + word)
                        stemmed.append(word)
                        break
                    elif word in value:
                        # print('word found in the irregular verb lists' + word)
                        stemmed.append(key)
                        break
                else:
                    # print('word not found in both key and value pairs ' + word)
                    for suf in suffixes:
                        if word.endswith(suf) and len(word) > len(suf):
                            temp.append(suf)
                    break
            if len(temp) != 0:
                try:
                    tx = max([len(c) for c in temp])
                    for t in temp:
                        if len(t) == tx:
                            i, ti = 0, 0
                            while i != -1:
                                ti = i
                                i = word.find(t, (word.find(t) + i + 1))
                            stemmed.append(self.remove_prefixes(word[:word.find(t, ti)], t))
                            # print('suffixes ', word, "\t\t\t\t", temp, "\t\t\t\t", t, "\t\t\t\t", word[:word.find(t, ti)])
                    temp.clear()
                except ValueError as Msg:
                    pass
        return None

    @staticmethod
    def remove_prefixes(word, s):
        # print('starting prefix cutter ...')
        tmp = []
        tmp.clear()
        for pre in prefixes:
            if word.startswith(pre):
                if len(pre) >= len(word):
                    continue
                tmp.append(pre)
        ptx = 0
        if len(tmp) != 0:
            try:
                ptx = max([len(c) for c in tmp])
                for t in tmp:
                    if len(t) == ptx:
                        word = word[word.find(t):]
                        # print('prefixes ', word, "\t\t\t\t", tmp, "\t\t\t\t", t, "\t\t\t\t", word[ptx:])
                        return add_necessary_affixes(t, word[ptx:], s)
                tmp.clear()
            except ValueError as Msg:
                pass
        return add_necessary_affixes(word[ptx:], s)

    def reader(self):
        file_string_list = ''
        try:
            file_string = open(self.FullFilePath, 'r').read()
            file_string = file_string.upper()
            file_string_list = re.sub("[^a-zA-Z]", " ", file_string)
            file_string_list = file_string_list.split()
        except FileNotFoundError as Msg:
            # print("{}".format(str(Msg)))
            pass
        return sorted(set(file_string_list))

    @staticmethod
    def remove_verb_to_be(lst):
        _List = []
        for word in lst:
            if word == 'be'.upper() or word == 'am'.upper() or word == 'is'.upper() or word == 'are'.upper() \
                    or word == 'was'.upper() or word == 'were'.upper() or word == 'been'.upper() or word == 'i'.upper():
                _List.append('BE')
            else:
                _List.append(word)
        return _List


def remove_to_be():
    # print('removing the verb to be from the stop word list')
    for wd in stopwords:
        if wd == 'be'.upper() or wd == 'am'.upper() or wd == 'is'.upper() or wd == 'are'.upper() \
                or wd == 'was'.upper() or wd == 'were'.upper() or wd == 'been'.upper() or wd == 'i'.upper():
            # print('removing ' + wd)
            stopwords.remove(wd)


def load_irregular_verb():
    # print('loading irregular verbs from the irregular.txt..')
    with open('affixes/irregular', 'r') as f:
        # print('reading...')
        line = f.readline()
        while line != '':
            # do the dict
            key = line[:line.find(' ')].upper()
            irregular[key] = []
            # !! no need to add key to the dict list since we can make decision on the key
            irregular[key].append(key)
            for wd in line[line.find(' '):].split():
                irregular[key].append(wd.upper())
            line = f.readline()
    return None


# TODO
# @abstractmethod
def determine_prefixes(pr):
    return ''


def add_necessary_affixes(pre='', wd='', suf=''):
    try:
        if suf == 'ABLE' or suf == 'IBLE':
            if wd[-1] == 'L':
                return determine_prefixes(pre) + wd + 'ATE'
        if suf == 'ABILITY ' or suf == 'IBILITY':
            if wd[-1] == 'S':
                return determine_prefixes(pre) + wd + 'E'
        if suf == 'ANCE' or suf == 'ENCE':
            if wd[-1] == 'D':
                return determine_prefixes(pre) + wd + 'ENT'
        if suf == 'ANCY' or suf == 'ENCY':
            if wd[-1] == 'L':
                return determine_prefixes(pre) + wd + 'ENT'
        if suf == 'ANCY' or suf == 'ENCY':
            if wd[-1] == 'L':
                return determine_prefixes(pre) + wd + 'ENT'
        if suf == 'ANT' or suf == 'ENT':
            if wd[-1] == 'T' or wd[-1] == 'R':
                return determine_prefixes(pre) + wd + 'E'
        if suf == 'ARIAN':
            if wd[-1] == 'N':
                return determine_prefixes(pre) +  wd + 'E'
        if suf == 'ATIVE':
            if wd[-1] == 'R':
                return determine_prefixes(pre) + wd + 'ATE'
        if suf == 'ATIVELY':
            if wd[-1] == 'E':
                return determine_prefixes(pre) + wd + 'ATE'
        if suf == 'CIDE':
            if wd[-1] == 'N':
                return determine_prefixes(pre) + wd + 'E'
        if suf == 'CIDAL':
            if wd[-1] == 'M':
                return determine_prefixes(pre) + wd + 'E'
        if suf == 'CY':
            if wd[-1] == 'N':
                return determine_prefixes(pre) + wd + 'T'
            if wd[-1] == 'A':
                return determine_prefixes(pre) + wd + 'TE'
        if suf == 'ED' or suf == 'D':
            if wd[-1] == 'S' or wd[-1] == 'V' or wd[-1] == 'T':
                return determine_prefixes(pre) + wd + 'E'
        if suf == 'EE':
            if wd[-1] == 'G' or wd[-1] == 'T' or wd[-1] == 'Y':
                return determine_prefixes(pre) + wd + 'E'
        if suf == 'ER':
            if wd[-1] == 'D' or wd[-1] == 'T' or wd[-1] == 'V':
                return determine_prefixes(pre) + wd + 'E'
            if wd[-1] == 'M' or wd[-1] == 'P' or wd[-1] == 'H':
                return determine_prefixes(pre) + wd + 'Y'
        if suf == 'ERY' or suf == 'RY':
            if wd[-1] == 'V' or wd[-1] == 'K' or wd[-1] == 'G':
                return determine_prefixes(pre) + wd + 'E'
        if suf == 'IANE' or suf == 'ANA':
            if wd[-1] == 'C':
                return determine_prefixes(pre) + wd + 'A'
            if wd[-1] == 'R':
                return determine_prefixes(pre) + wd + 'Y'
        if suf == 'IC':
            if wd[-1] == 'N':
                return determine_prefixes(pre) + wd + 'E'
            if wd[-1] == 'M' or wd[-1] == 'T':
                return determine_prefixes(pre) + wd + 'Y'
        if suf == 'ICAL':
            if wd[-1] == 'M':
                return determine_prefixes(pre) + wd + 'E'
        if suf == 'ICALLY':
            if wd[-1] == 'S':
                return determine_prefixes(pre) + wd + 'ICS'
        if suf == 'ICS':
            if wd[-1] == 'S':
                return determine_prefixes(pre) + wd + 'IC'
        if suf == 'ITY' or suf == 'TY':
            if wd[-1] == 'R':
                return determine_prefixes(pre) + wd + 'E'
        if suf == 'ING':
            if wd[-1] == 'T':
                return determine_prefixes(pre) + wd + 'E'
        if suf == 'ION':
            if wd[-1] == 'T':
                return determine_prefixes(pre) + wd + 'E'
        if suf == 'ISM':
            if wd[-1] == 'C':
                return determine_prefixes(pre) + wd + 'E'
        if suf == 'ISM':
            if wd[-1] == 'C':
                return determine_prefixes(pre) + wd + 'E'
        if suf == 'IST':
            if wd[-1] == 'R':
                return determine_prefixes(pre) + wd + 'Y'
        if suf == 'ITY':
            if wd[-1] == 'T':
                return determine_prefixes(pre) + wd + 'E'
        if suf == 'IVE':
            if wd[-1] == 'S' or wd[-1] == 'P':
                return determine_prefixes(pre) + wd + 'E'
        if suf == 'IZATION':
            if wd[-1] == 'N':
                return determine_prefixes(pre) + wd + 'IZE'
        if suf == 'IZATIONALLY':
            if wd[-1] == 'N':
                return determine_prefixes(pre) + wd + 'E'
        if suf == 'OLOGY' or suf == 'GY':
            if wd[-1] == 'I':
                return determine_prefixes(pre) + wd + 'TY'
        if suf == 'IZATIONALLY':
            if wd[-1] == 'N':
                return determine_prefixes(pre) + wd + 'E'
        if suf == 'ORY':
            if wd[-1] == 'V':
                return determine_prefixes(pre) + wd + 'E'
        if suf == 'OUS':
            if wd[-1] == 'I':
                return determine_prefixes(pre) + wd + 'ES'
            if wd[-1] == 'O':
                return determine_prefixes(pre) + wd + 'Y'
        if suf == 'Y' or suf == 'EY' or suf == 'IE':
            if wd.endswith('DD'):
                return determine_prefixes(pre) + word[:-2]
            if wd.endswith('GG'):
                return determine_prefixes(pre) + word[:-2]
    except UnboundLocalError as Msg:
        print(str(Msg))
    return wd


def write_to_file(lists, fn, name):
    # print(fn)
    if not os.path.exists('affixes/'):
        os.mkdir('affixes/')
    if not os.path.exists('affixes/output/'):
        os.mkdir('affixes/output/')
    if not os.path.exists('affixes/output/' + fn):
        # print(os.path.exists('affixes/output/' + fn + '/'))
        os.mkdir('affixes/output/' + fn + '/')
    with open('affixes/output/' + fn + '/' + name + '.txt', 'w') as f:
        for word in sorted(set(lists)):
            f.write(word + '\n')


def print_word_list(to_list):
    for ls in to_list:
        print(ls)
    return None


while True:
    try:
        pd_name = input("\nENTER FULL FILE NAME: ")
        # what if thye provide ys none txt format file type
        # save me here
        
        # what  if they provide us folder containing multiple file instead of single file 
        if os.path.isdir(pd_name):
        	# save me integrating this
        	rd = ReadConcurrently(pd_name, 8)
        	rd.feed().items()
        else:
	        open(pd_name, 'r')
	        stem = Stemmiser(pd_name)
	        stem.stem()
	        write_to_file(sorted(set(stemmed)), pd_name[pd_name.rfind('\\') + 1: pd_name.rfind('.txt')], 'stemmed')
	        print('browse affixes/' + pd_name[pd_name.rfind('\\') + 1: pd_name.rfind('.txt')] + ' folder')
        YesNo = input('\ndo you want to continue [YES/NO]: ')
        if len(YesNo) > 0:
            if YesNo != 'yes' and YesNo != 'y' and YesNo != 'Y' \
                    and YesNo != 'YES':
                print("terminating...")
                sys.exit(0)
    except FileNotFoundError as Msg:
        print(str(Msg))
    except PermissionError as Msg:
        print(str(Msg))
