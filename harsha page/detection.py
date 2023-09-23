import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filtered-data')
def filtered_data():
    df = pd.read_csv("tapusena\\harsha page\\cyberbullying_tweets.csv")
    x = df["tweet_text"]
    y = input("Enter your experience: ")

    y_words = y.split()

    vectorizer = TfidfVectorizer(lowercase=False, use_idf=True, max_features=2500)

    vectTrain = vectorizer.fit_transform(x)
    vectTest = vectorizer.transform([' '.join(y_words)])  # Join the words back into a string before transforming
    result = cosine_similarity(vectTrain, vectTest)
    top_indices = np.argsort(result[:, 0])[-5:][::-1]
    top_tweets = df.loc[top_indices, "cyberbullying_type"]

    reference_dict = {'gender':1,
    'ethnicity':2,
    'other_cyberbullying':3,
    'age':4,
    'religion':5,
    'not_cyberbullying': 6}
    result = {}
    res = []

    for i in top_tweets:
        res.append(i)

    for i in top_tweets:
        result[i] = res.count(i)
    result = sorted(result)
    type=result[:1][0]

    dhelp = pd.read_csv("tapusena\\harsha page\\help.csv")
    filtered_rows = dhelp[dhelp["target"] == type]

    matched_rows = filtered_rows.to_csv(index=False, sep=',', line_terminator='\n')
    return matched_rows

if __name__ == '__main__':
    app.run()
