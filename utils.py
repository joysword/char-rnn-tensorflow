# -*- coding: UTF-8 -*-

import codecs
import os
import io
import collections
from six.moves import cPickle
import numpy as np

class TextLoader():
    def __init__(self, data_dir, batch_size, seq_length, encoding='utf-8'):
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.seq_length = seq_length
        self.encoding = encoding

        input_file = os.path.join(data_dir, "input.txt")
        vocab_file = os.path.join(data_dir, "vocab.pkl")
        tensor_file = os.path.join(data_dir, "data.npy")

        # if vocab file and tensor file exist, load from previous preprocess
        # otherwise do preprocess
        if not (os.path.exists(vocab_file) and os.path.exists(tensor_file)):
            print("reading text file")
            self.preprocess(input_file, vocab_file, tensor_file)
        else:
            print("loading preprocessed files")
            self.load_preprocessed(vocab_file, tensor_file)

        self.create_batches()
        self.reset_batch_pointer()

    def preprocess(self, input_file, vocab_file, tensor_file):

        # read training set
        poetries = []

        with io.open(input_file, "r", encoding=self.encoding) as f:
            for line in f:
                try:
                    title, content = line.strip().split(':')
                    content = content.replace(' ', '')
                    if '_' in content or '(' in content or u'（' in content or u'《' in content or '[' in content:
                        continue
                    if len(content) < 5:# or len(content) > 79:
                        continue
                    content = '[' + content + ']'
                    poetries.append(content)
                except Exception as e:
                    pass

        # sort by number of characters in each poem
        poetries = sorted(poetries, key = lambda line: len(line))
        print 'number of poems: ', len(poetries)

        # get all characters
        all_chars = []
        for poetry in poetries:
            all_chars += [word for word in poetry]

        # count characters
        counter = collections.Counter(all_chars)

        # sort characters by number of appearance
        # from most frequent to least
        count_pairs = sorted(counter.items(), key=lambda x: -x[1])

        # get a lit of all characters, sorted
        self.chars, _ = zip(*count_pairs)

        # take the frequent words
        self.chars = self.chars[:len(self.chars)] + (' ',)

        # get size of vocab
        self.vocab_size = len(self.chars)

        # get indexed vocab
        self.vocab = dict(zip(self.chars, range(len(self.chars))))

        # dump characters to vocab_file
        with open(vocab_file, 'wb') as f:
            cPickle.dump(self.chars, f)

        # get tensor by converting each character in training set to index of each character
        self.tensor = np.array(list(map(self.vocab.get, all_chars)))

        # save tensor
        np.save(tensor_file, self.tensor)

    def load_preprocessed(self, vocab_file, tensor_file):
        with open(vocab_file, 'rb') as f:
            self.chars = cPickle.load(f)
        self.vocab_size = len(self.chars)
        self.vocab = dict(zip(self.chars, range(len(self.chars))))
        self.tensor = np.load(tensor_file)
        self.num_batches = int(self.tensor.size / (self.batch_size *
                                                   self.seq_length))

    def create_batches(self):
        self.num_batches = int(self.tensor.size / (self.batch_size *
                                                   self.seq_length))

        # When the data (tensor) is too small, let's give them a better error message
        if self.num_batches==0:
            assert False, "No enough data. Make seq_length and batch_size smaller."

        # get rid of the leftover at the end of the tensor
        self.tensor = self.tensor[:self.num_batches * self.batch_size * self.seq_length]

        # set xdata and ydata
        # ydata = [xdata[1:], xdata[0]]
        xdata = self.tensor
        ydata = np.copy(self.tensor)
        ydata[:-1] = xdata[1:]
        ydata[-1] = xdata[0]

        # get x_batches and y_batches by making xdata and ydata into num_batches batch_size by seq_length matrices
        # for example, if num_batches = 100, batch_size = 50 and seq_length = 50,
        # each of x_batches and y_batches consists of 100 50*50 matrices
        self.x_batches = np.split(xdata.reshape(self.batch_size, -1), self.num_batches, 1)
        self.y_batches = np.split(ydata.reshape(self.batch_size, -1), self.num_batches, 1)


    def next_batch(self):
        x, y = self.x_batches[self.pointer], self.y_batches[self.pointer]
        self.pointer += 1
        return x, y

    def reset_batch_pointer(self):
        self.pointer = 0
