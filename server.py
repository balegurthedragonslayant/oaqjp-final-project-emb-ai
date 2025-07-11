"""
Flask web server for emotion detection using Watson NLP API.
"""

import requests
from flask import Flask, request, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route('/')
def index():
    """
    Renders the home page with the input form.
    """
    return render_template('index.html')


@app.route('/emotionDetector', methods=['GET'])
def detect_emotion():
    """
    Endpoint for detecting emotions from user text input.

    Returns:
        str: A formatted string of detected emotion scores and dominant emotion,
             or an error message if input is invalid.
    """
    try:
        text_to_analyze = request.args.get('textToAnalyze', '')

        if not text_to_analyze.strip():
            return (
                "Invalid text! Please try again!",
                400,
                {"Content-Type": "text/plain"}
            )

        emotion_response = emotion_detector(text_to_analyze)

        if (
            emotion_response is None
            or emotion_response.get('dominant_emotion') is None
        ):
            return "Invalid text! Please try again!", 400

        response_message = (
            f"For the given statement, the system response is 'anger': "
            f"{emotion_response['anger']}, 'disgust': {emotion_response['disgust']}, "
            f"'fear': {emotion_response['fear']}, 'joy': {emotion_response['joy']} "
            f"and 'sadness': {emotion_response['sadness']}. "
            f"The dominant emotion is {emotion_response['dominant_emotion']}."
        )
        return response_message

    except requests.exceptions.RequestException as error:
        return f"Request failed: {str(error)}", 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002, debug=True)
