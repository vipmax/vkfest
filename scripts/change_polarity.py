import pickle
import tarfile
import sys
import io
import tarfile

reload(sys)
sys.setdefaultencoding('UTF8')

# extract dictionary package
tar = tarfile.open("/home/maxpetrov/polyglot_data/sentiment2/ru/ru.sent.pkl.tar.bz2")
tar.extractall('/home/maxpetrov/polyglot_data/')
tar.close()

# read all new words
new_words = []
new_words_values = []

new_data_file = io.open('/home/maxpetrov/PycharmProjects/vkfest/data/full_vocabulary.csv', 'r', encoding='utf8')
for line in new_data_file.readlines():
    l = line.split(',')
    new_words.append(l[0])
    # new_words_values.append([int(l[1].replace('\n', ''))])
    new_words_values.append([int(l[1].replace('\n', '').replace(']', '').replace('[', ''))])

dictionary_words = list()
dictionary_words_values = list()

# add new words to dictionary
for i in range(len(new_words)):
    if new_words[i] not in dictionary_words:
        print 'adding ', new_words[i], new_words_values[i]
        dictionary_words.extend([new_words[i]])
        dictionary_words_values.extend([new_words_values[i]])
    else:
        print 'already exist word =', new_words[i]

# write new dictionary to pickle file
result = (dictionary_words, dictionary_words_values)
with open('/home/maxpetrov/polyglot_data/data/tmp/sentiment/ru/ru.sent.pkl', 'w+') as f:
    pickle.dump(result, f)

# add dictionary to package

tar = tarfile.open("/home/maxpetrov/polyglot_data/sentiment2/ru/ru.sent.pkl.tar.bz2", "w")
tar.add("/home/maxpetrov/polyglot_data/data/tmp/sentiment/ru/ru.sent.pkl")
tar.close()
