import pickle

#function to run for prediction
def detecting_fake_news(var, model):    
#retrieving the best model for prediction call
    if model == 'SVM':
        load_model = pickle.load(open('./models/svm_pipeline_ngram.sav', 'rb'))
    elif model == 'SGD':
        load_model = pickle.load(open('./models/sgd_pipeline_ngram.sav', 'rb'))
    elif model == 'Logistic':
        load_model = pickle.load(open('./models/final_model.sav', 'rb'))
    elif model == 'Naive-bayes':
        load_model = pickle.load(open('./models/nb_pipeline_ngram.sav', 'rb'))
    else:
        load_model = pickle.load(open('./models/random_forest_final.sav', 'rb'))
    
    prediction = load_model.predict([var]) 
    if model == 'SVM':
        prob = load_model.predict_proba([var])
    else:
        prob = load_model.predict_proba([var])

    return prediction[0], prob[0][1]
