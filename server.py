from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/emotionDetector", methods=["POST"])
def emotion_detector_route():
    # Get the text from the HTML form input
    text_to_analyze = request.form['textToAnalyze']

    # Get emotion analysis result
    result = emotion_detector(text_to_analyze)

    # Check for errors
    if "error" in result:
        return result["error"]

    # Format the output as requested
    output = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )

    return output

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
