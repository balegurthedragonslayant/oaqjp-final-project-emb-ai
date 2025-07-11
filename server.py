"""
This module contains a Flask application for emotion detection using Watson NLP API.
It provides a web interface and an API endpoint for analyzing emotions in text.
"""

import requests
from flask import Flask, request, jsonify, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/')
def index():
    """
    Render the main page with the interface for emotion detection.
    """
    return render_template('index.html')

@app.route('/emotionDetector', methods=['GET'])
def detect_emotion():
    """
    Detect emotions in a given text using the emotion_detector function.

    Accepts:
        textToAnalyze (str): The input text passed as a query parameter.

    Returns:
        str: A formatted message containing emotion scores and dominant emotion.
    """
    try:
        # Get text from query parameters
        text_to_analyze = request.args.get('textToAnalyze', '')

        if not text_to_analyze.strip():
            return (
            "Invalid text! Please try again!", 
            400, 
            {"Content-Type": "text/plain"}
        )

        emotion_response = emotion_detector(text_to_analyze)

        if (
            emotion_response is None or 
            emotion_response.get('dominant_emotion') is None
        ):
            return "Invalid text! Please try again!", 400

        # Build response string
        response_message = (
            f"For the given statement, the system response is 'anger': "
            f"{emotion_response['anger']}, 'disgust': {emotion_response['disgust']}, "
            f"'fear': {emotion_response['fear']}, 'joy': {emotion_response['joy']} "
            f"and 'sadness': {emotion_response['sadness']}. "
            f"The dominant emotion is {emotion_response['dominant_emotion']}."
        )
        return response_message

    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
