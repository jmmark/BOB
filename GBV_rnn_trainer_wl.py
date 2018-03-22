'''based on: https://github.com/keras-team/keras/blob/master/examples/lstm_text_generation.py'''

from __future__ import print_function
from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
#from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
import io
import pre_processing as pp
import h5py

path = "all_gbv_lyrics.txt"
text = pp.load_n_scrub(path)
verses = pp.overlapping_verses(text, 4)


words = sorted(list(set(' '.join(verses).split(' '))))
print('total lines:', len(text))
print('total created verses:', len(verses))
print('total words:', len(words))
word_indices = dict((c, i) for i, c in enumerate(words))
indices_word = dict((i, c) for i, c in enumerate(words))

# find the longest verse
def num_words(inp_text):
    ''' count the words in an input string, by space '''
    return(len(inp_text.split(' ')))

maxlen = max([num_words(verse) for verse in verses])
# step = 3
# sentences = []
# next_chars = []
# for i in range(0, len(text) - maxlen, step):
#     sentences.append(text[i: i + maxlen])
#     next_chars.append(text[i + maxlen])
# print('nb sequences:', len(sentences))
print('longest verse:', maxlen)

window = 10
step = 1
# chop input up into window word bits for training the model
full_verse = ' '.join(verses).split(' ')
total_words = len(full_verse)
train_words = []
next_word = []
for i in range(0, total_words - window, step):
    train_words += [full_verse[i:i + window]]
    next_word += [full_verse[i + window]]



print('Vectorization...')
x = np.zeros((len(train_words), window, len(words)), dtype=np.bool)
y = np.zeros((len(train_words), len(words)), dtype=np.bool)
for i, verse in enumerate(train_words):
    for t, word in enumerate(verse):
        x[i, t, word_indices[word]] = 1
    y[i, word_indices[next_word[i]]] = 1


# build the model: a single LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(128, input_shape=(window, len(words))))
model.add(Dense(len(words)))
model.add(Activation('softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def on_epoch_end(epoch, logs):
    # Function invoked at end of each epoch. Prints generated text.
    print()
    print('----- Generating text after Epoch: %d' % epoch)

    start_index = random.randint(0, total_words - window - 1)
    for diversity in [0.2, 0.5, 1.0, 1.2]:
        print('----- diversity:', diversity)

        generated = ''
        sentence = full_verse[start_index: start_index + window]
        generated += ' '.join(sentence)
        print('----- Generating with seed: "' + generated + '"')
        sys.stdout.write(generated)

        for i in range(400):
            x_pred = np.zeros((1, window, len(words)))
            for t, word in enumerate(sentence):
                x_pred[0, t, word_indices[word]] = 1.

            preds = model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_word[next_index]

            generated += ' ' + next_char
            sentence = sentence[1:] + [next_char]

            sys.stdout.write(' ' + next_char)
            sys.stdout.flush()
            if next_char == '<eov>' :
                break
        print()

print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

model.fit(x, y,
          batch_size=128,
          epochs=20,
          callbacks=[print_callback])

model.save("GBV_rnn_wl.h5")