from flask import Flask, render_template, request, redirect, url_for
from config import DevConfig
from sentiment import get_all_words, get_tweets_for_model, remove_noise,process
from datetime import timedelta
from word_cloud import process_cloud, cloud
from prediction import detecting_fake_news
import requests
import json


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/sentiment', methods=['GET','POST'])
def sentiment():
    if request.method == 'POST':
        userinput = request.form.get('result')
        abc = requests.post('http://text-processing.com/api/sentiment/', data={"text": str(userinput)})
        obj = abc.json()
        if obj["label"] == "pos":
            backimg = "static/img/pos.jpg"
            font = "font-family: 'Princess Sofia', cursive;"
        elif obj["label"] == "neg":
            backimg = "static/img/sad.jpg"
            font = "font-family: 'Special Elite', cursive;"
        else:
            backimg = "static/img/neutral.jpg"
            font = "font-family: 'Balthazar', serif;"

        return render_template('result.html', A= str(userinput), B1=str(obj["probability"]["pos"]),B2=str(obj["probability"]["neutral"]),B3=str(obj["probability"]["neg"]),B4=str(obj["label"]), backimg = backimg, font=font)
        
    return render_template('sentiment.html')

@app.route('/word_cloud', methods=['GET','POST'])
def word_cloud(): 
    if request.method == 'POST':
        global fig_name
        input_text = request.form.get('news')
        input_genre = request.form.get("selectgenre")
        #picname = request.form.get('genre')
        fig_name, font_path, back = process_cloud(input_text, str(input_genre))
        return render_template('word_cloud_result.html', fig_name = str(fig_name), font_path=str(font_path), back=str(back)) 
    return render_template('word_cloud.html', data=[{'name':'Business'}, {'name':'Education'},{'name':'Entertainment'}, {'name':'Health'},
                                                    {'name':'Medical'}, {'name':'Sports'}, {'name':'Technology'}, {'name':'Others'}])

@app.route('/return')
def back():
 	return redirect(url_for('index'))

@app.route('/return_cloud')
def back_1():
 	return redirect(url_for('word_cloud'))

@app.route('/return_sentiment')
def back_2():
 	return redirect(url_for('sentiment'))

@app.route('/predict', methods=['GET','POST'])
def predict(): 
    back = 'static/img/back.jpg'
    if request.method == 'POST':
        input_text = request.form.get('news')
        model = request.form.get('selectmodel')
        pred, prob = detecting_fake_news(input_text, model)
        return render_template('predict.html', back=back, pred=str(pred), prob=str(prob))
    return render_template('predict.html', back=back, 
    data=[{'name':'SVM'}, {'name':'Logistic'},{'name':'SGD'}, {'name':'Naive-bayes'}, {'name':'RandomForest'}])

@app.route('/return_predict')
def back_3():
 	return redirect(url_for('predict'))

if __name__ == '__main__':
    app.run()