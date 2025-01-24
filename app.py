from flask import Flask, request, jsonify
from flask_cors import CORS
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests from the extension

# IBM Watson NLU credentials
IBM_WATSON_API_KEY = "Enter Your IBM Api key"
IBM_WATSON_API_URL = "nter Your IBM Api url"

# YouTube API key
YOUTUBE_API_KEY = "Anter Your YouTube Api key"

# Initialize IBM Watson NLU
authenticator = IAMAuthenticator(IBM_WATSON_API_KEY)
nlu_client = NaturalLanguageUnderstandingV1(
    version="2022-04-07",
    authenticator=authenticator
)
nlu_client.set_service_url(IBM_WATSON_API_URL)

@app.route("/analyze", methods=["POST"])
def analyze_sentiment():
    data = request.json
    video_id = data.get("video_id")

    if not video_id:
        return jsonify({"error": "No video ID provided!"}), 400

    # Fetch YouTube comments
    comments = fetch_youtube_comments(video_id)
    if not comments:
        return jsonify({"error": "No comments found or an error occurred!"}), 400

    # Perform sentiment analysis
    sentiment_results = analyze_comments(comments)

    # Return the results
    return jsonify(sentiment_results)

def fetch_youtube_comments(video_id):
    url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return None

    data = response.json()
    comments = [item["snippet"]["topLevelComment"]["snippet"]["textOriginal"] for item in data.get("items", [])]
    return comments

def analyze_comments(comments):
    positive = neutral = negative = 0

    for comment in comments:
        try:
            response = nlu_client.analyze(
                text=comment,
                features={"sentiment": {}}
            ).get_result()
            sentiment = response["sentiment"]["document"]["label"]
            if sentiment == "positive":
                positive += 1
            elif sentiment == "neutral":
                neutral += 1
            else:
                negative += 1
        except Exception as e:
            print(f"Error analyzing comment: {e}")
            continue

    return {"positive": positive, "neutral": neutral, "negative": negative}

if __name__ == "__main__":
    app.run(debug=True)
