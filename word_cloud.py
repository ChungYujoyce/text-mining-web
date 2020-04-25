import sys, os, datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from glob import glob
import nltk
from nltk.corpus import stopwords
from nltk import PorterStemmer
from nltk.stem import WordNetLemmatizer
import pandas as pd
import numpy as np
import math, re, pickle
from sklearn import model_selection, preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
import sklearn
def process_cloud(input_text, ingenre):
    TRAINING_DATA_PATH = "./ProcessedNewsData/**/*.txt"
    RANDOM_FOREST_PKL = "./RandomForest.pkl"
    NUMBER_OF_GENRE = 8
    genres = ['Business', 'Education', 'Entertainment', 'Health', 'Medical', 'Sports', 'Technology', 'Others']
    fonts = [
        'Gloucester-MT-Extra-Condensed.ttf',
        'Cooper-Black.ttf',
        'Harlow-Solid-Italic.ttf',
        'Broadway.ttf',
        'Brush-Script-MT-Italic.ttf',
        'Gill-Sans-Ultra-Bold.ttf',
        'CopperplateGothicBold.ttf',
        'Wide-Latin.ttf',
    ] # genre[i] goes with fonts[i]

    txt_file = glob(TRAINING_DATA_PATH) ########## WARNING give path to the folder each folder at a time
    doc_all = {}
    for i in txt_file:
        text = open(i, encoding = "latin-1").read().lower()
        doc_all[i.split("\\")[2].split(".")[0]] = text ########## WARNING i.split("/")[idx] -> change the idx
        # i: the absolute path of abc.txt, i.split("/")[3]: abc.txt

    x = list(doc_all.values()) # x for training
    key = list(doc_all.keys()) # y for testing
    ###labels
    lab = []
    for i in range(len(key)):
        lab.append(key[i][10:13])

    train_x, valid_x, train_y, valid_y = model_selection.train_test_split(x, lab,test_size=0.2,random_state=42, shuffle=True)

    encoder = preprocessing.LabelEncoder()
    train_y_en = encoder.fit_transform(train_y)
    valid_y_en = encoder.fit_transform(valid_y)

    # word level tf-idf
    tfidf_vect = TfidfVectorizer(tokenizer = tokenize, stop_words = 'english', max_features = 5000)
    tfidf_vect.fit(train_x) #Learn vocabulary and idf from training data set. (in bad words)

    ## prediction for the new text using saved classification model
    with open(RANDOM_FOREST_PKL, 'rb') as f:
        clf = pickle.load(f) # load the model

    comment_tfidf =  tfidf_vect.transform([input_text])
    comment_predictions = clf.predict(comment_tfidf)
    # print(comment_predictions) # Weird
    # print(encoder.inverse_transform(comment_predictions)[0].lower()) # <class 'numpy.ndarray'>
    genre = encoder.inverse_transform(comment_predictions)[0].lower()
    fig_name = ingenre
    
    for i in range(NUMBER_OF_GENRE):
        if genre == genres[i][:3].lower():
            print(genres[i])
            idx = i
            break
        else: idx = NUMBER_OF_GENRE - 1 # Others as default
    
    for j in range(NUMBER_OF_GENRE):
        if ingenre == genres[j]:
            idx = j
            break
    
    font_path = os.getcwd() + "\\static\\assets\\" + fonts[j]
    background_image_path = os.getcwd() + "\\static\\assets\\" + genres[j] + ".JPG"
    background = "static/assets/" + genres[i] + ".JPG"

    nltk_stopwords = stopwords.words('english')
    customized_stopwords = ["the","and","i", "'s", "-", "--", "---", "n't", "'in", "``", "`", "'", "''", "'ll", "'ve"]
    Stopwords = customized_stopwords + nltk_stopwords + list(STOPWORDS)

    img = plt.imread(background_image_path)
    plt.figure('tmp', frameon = False, facecolor=(0, 0, 0, 0), edgecolor=(0, 0, 0, 0))
    plt.imshow(img)
    plt.margins(x = 0, y = 0)
    plt.xticks([])
    plt.yticks([])
    cloud(input_text, Stopwords, font_path)
    PATH = os.getcwd() + "\\static\\cloud_result\\"
    current_time = str(datetime.datetime.now()).split(" ")[1].replace(":", "-").replace(".", "-") # 2020-04-20 23:57:44.019598
    fig_name = fig_name + current_time
    plt.savefig(os.path.join(PATH, fig_name)) # Save to same folder as this python file
    fig_name = 'cloud_result/' + fig_name +'.png'

    return fig_name, font_path, background

def cloud(text, Stopwords, font_path):
    word = WordCloud(stopwords = Stopwords, width = 2000, height = 1500,\
                     font_path = font_path, min_font_size = 3, max_font_size = 400, max_words = 70,\
                     background_color = "rgba(255, 255, 255, 0)", mode = 'RGBA', colormap = plt.get_cmap('nipy_spectral') # nipy_spectral, tab10
           ).generate(text)
    plt.imshow( word, cmap = plt.get_cmap('jet'), alpha = 0.8)

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = []
    for item in tokens:
        stems.append(PorterStemmer().stem(item))
        #stems.append(WordNetLemmatizer().lemmatize(item))
    return stems


#process_cloud("A star is born in 2018 amerivan musical romantic drama film produced and directed by bradley cooper in his directorial debut and written by eric roth, cooperand will fetters."
#, "Others")