from flask import Flask, render_template, request
import os
import math
import joblib
import pandas as pd

app = Flask(__name__)

# File upload folder
UPLOAD_FOLDER = 'prediction_model/model'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to calculate topic weight sum
def topic_weight_sum(topics):
    topic_freq = {'Music': 1997, 'Pop music': 1855, 'Entertainment': 2023, 'Film': 1324, 'Action game': 2506, 'Video game culture': 3002, 'Fashion': 176, 'Lifestyle (sociology)': 3973, 'Association football': 708, 'Sport': 1743, 'Electronic music': 541, 'Music of Asia': 662, 'Motorsport': 392, 'Cricket': 286, 'Hip hop music': 834, 'Music of Latin America': 718, 'Food': 825, 'Technology': 204, 'Hobby': 657, 'Basketball': 156, 'Politics': 445, 'Society': 1266, 'Television program': 1311, 'Independent music': 176, 'Rock music': 155, 'Role-playing video game': 2061, 'Strategy video game': 1017, 'Vehicle': 658, 'Physical fitness': 386, 'Action-adventure game': 1983, 'Simulation video game': 90, 'American football': 450, 'Tourism': 100, 'Reggae': 50, 'Health': 372, 'Casual game': 50, 'Jazz': 35, 'Rhythm and blues': 48, 'Christian music': 33, 'Sports game': 38, 'Humour': 668, 'Performing arts': 73, 'Soul music': 95, 'Tennis': 7, 'Military': 153, 'Country music': 22, 'Pet': 69, 'Religion': 20, 'Knowledge': 90, 'Boxing': 11, 'Professional wrestling': 3, 'Baseball': 23, 'Mixed martial arts': 6, 'Golf': 12, 'Ice hockey': 4, 'Classical music': 4, 'Business': 30, 'Music video game': 1, 'Puzzle video game': 20, 'Racing video game': 10, 'Physical attractiveness': 1}

    return sum(topic_freq.get(topic, 0) for topic in topics)

# Function to parse ISO 8601 duration
def parse_duration(duration):
    hours, minutes, seconds = 0, 0, 0
    duration = duration.strip()
    try:
        hours = int(duration.split("PT")[0])
    except ValueError:
        hours = 0
    if "M" in duration:
        minutes = int(duration.split("PT")[1].split("M")[0])
        if "S" in duration:
            seconds = int(duration.split("M")[1].split("S")[0])
    else:
        seconds = int(duration.split("PT")[1].split("S")[0])
    if minutes >= 60 or seconds >= 60:
        raise ValueError("Not valid value!")
    return hours * 3600 + minutes * 60 + seconds

# Function to preprocess input data
def preprocess_input(data):
    input_df = pd.DataFrame({
        'log_viewCount': [math.log1p(float(data["viewCount"]))],
        'log_likeCount': [math.log1p(float(data["likeCount"]))],
        'log_commentCount': [math.log1p(float(data["commentCount"]))],
        'log_avgDailyViews': [math.log1p(float(data["avgDailyViews"]))],
        'engagementRate': [float(data["engagementRate"])],
        'topicWeightSum': [topic_weight_sum(data["topicCategories"])],
        'duration_seconds': [parse_duration(data["duration"])],
        'category': [data["category"]]
    })
    return input_df

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Retrieve input data from form
        viewCount = request.form.get("viewCount")
        likeCount = request.form.get("likeCount")
        commentCount = request.form.get("commentCount")
        avgDailyViews = request.form.get("avgDailyViews")
        engagementRate = request.form.get("engagementRate")
        topicCategories = request.form.get("topicCategories").split(",")  # Comma-separated topics
        duration = request.form.get("duration")
        category = request.form.get("category")  # Category selected from dropdown

        # Save uploaded files
        model_file = request.files['model']
        preprocessor_file = request.files['preprocessor']

        model_path = os.path.join(app.config['UPLOAD_FOLDER'], model_file.filename)
        preprocessor_path = os.path.join(app.config['UPLOAD_FOLDER'], preprocessor_file.filename)
        
        model_file.save(model_path)
        preprocessor_file.save(preprocessor_path)

        # Load the uploaded model and preprocessor
        model = joblib.load(model_path)
        preprocessor = joblib.load(preprocessor_path)

        # Preprocess input
        input_data = {
            "viewCount": viewCount,
            "likeCount": likeCount,
            "commentCount": commentCount,
            "avgDailyViews": avgDailyViews,
            "engagementRate": engagementRate,
            "topicCategories": topicCategories,
            "duration": duration,
            "category": category  # Pass the selected category
        }
        input_df = preprocess_input(input_data)

        # Predict
        preprocessed = preprocessor.transform(input_df)
        prediction = model.predict(preprocessed)[0]
        prediction_prob = model.predict_proba(preprocessed)[:, 1][0] * 100

        return render_template("result.html", prediction=prediction, prediction_prob=round(prediction_prob, 8))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=9879)
