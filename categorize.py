import pickle
import numpy as np 
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import pyttsx3 as spk
import os
from word2number import w2n
import pandas as pd

lemmatizer = WordNetLemmatizer()

df = pd.read_csv('./data/book1.csv', encoding='latin-1')

intents = df['intents'].tolist()
patterns = df['patterns'].tolist()

words = pickle.load(open("./data/words.pkl", 'rb'))
classes = pickle.load(open("./data/classes.pkl", 'rb'))
model = load_model("./data/comment_model.h5")

def clean_up(sentence):
	sen_words = nltk.word_tokenize(sentence)
	sen_words = [lemmatizer.lemmatize(word) for word in sen_words]
	return sen_words

def bag_of_words(sentence):
	sen_words = clean_up(sentence)
	bag = [0] * len(words)
	for w in sen_words:
		for i, word in enumerate(words):
			if word == w:
				bag[i] = 1
	return np.array(bag)

def predict_class(sentence):
	bow = bag_of_words(sentence)
	res = model.predict(np.array([bow]))[0]
	ERROR_THRESHOLD = 0.25
	result = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
	result.sort(key=lambda x: x[1], reverse=True)
	return_list = []
	for r in result:
		return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
	return return_list

def categorize(msg):
	ints = predict_class(msg)
	return ints[0]['intent']