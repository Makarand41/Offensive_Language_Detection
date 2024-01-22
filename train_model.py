import random
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import pandas as pd

nltk.download('punkt')
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

print('Opening data.csv...')
df = pd.read_csv('./data/book1.csv', encoding='latin-1')

intents = df['intents'].tolist()
patterns = df['patterns'].tolist()

print('Data.csv is read...')
words = []
classes = []
documents = []
punctuations = ['?', '!', ',', '.', ';', ':', '@', '#', '$', '&', '*', '(', ')']
tag = "Undefined"
i = 0
print('Processing the data to build a model....')
while True:
    if i == len(intents):
        break
    elif str(patterns[i]) == '0':
        tag = 'Negative'
    elif str(patterns[i]) == '2':
        tag = 'Neutral'
    elif str(patterns[i]) == '4':
        tag = 'Positive'
    word_list = nltk.word_tokenize(intents[i])
    words.extend(word_list)
    documents.append((word_list, tag))
    if tag not in classes:
        classes.append(tag)
    i += 1

print('Preparing the data for processing....')
words = [lemmatizer.lemmatize(word) for word in words if word not in punctuations]
words = sorted(set(words))
classes = sorted(set(classes))

print('Dumping the data....')
pickle.dump(words, open("./data/words.pkl", 'wb'))
pickle.dump(classes, open("./data/classes.pkl", 'wb'))

training = []
output = [0] * len(classes)

print('Processing the comments...')
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output)
    output_row[classes.index(document[1])] = 1
    training.append((np.array(bag), np.array(output_row)))

random.shuffle(training)

train_x = np.array([bag for bag, _ in training])
train_y = np.array([output_row for _, output_row in training])

print('Building the model...')
model = Sequential()
model.add(Dense(256, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

print('Training the model....')
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(train_x, train_y, epochs=115, batch_size=700, verbose=1)

print('Saving the model....')
model.save("./data/comment_model.h5", hist)

print('Model has graduated and is now ready for the job :)')
