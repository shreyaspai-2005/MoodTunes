from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS
import traceback # Import traceback to get full error details
import sys # To exit if model fails to load
import os # For environment variables, if you decide to externalize paths/configs

# --- CONFIGURATION ---
# It's good practice to put configurations at the top or in a separate config file.
# We'll use a specific model version to ensure consistency.
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment"

# Define the mood-to-music mapping with your actual Spotify playlist URLs
MOOD_MUSIC_MAP = {
    'LABEL_0': { # Negative / Down
        'mood': 'Negative / Reflective',
        'music_description': 'Calming Ambient, Reflective Classical, Blues, Melancholy Indie',
        'spotify_playlist_url': 'https://open.spotify.com/playlist/2sOMIgioNPngXojcOuR4tn'
    },
    'LABEL_1': { # Neutral / Calm
        'mood': 'Neutral / Calm',
        'music_description': 'Relaxing Lo-Fi, Smooth Jazz, Acoustic Folk, Instrumental',
        'spotify_playlist_url': 'https://open.spotify.com/playlist/5jYQ4O9Ii3tQcSbJMtVrk8'
    },
    'LABEL_2': { # Positive / Upbeat
        'mood': 'Positive / Upbeat',
        'music_description': 'Energetic Pop, Upbeat Electronic, Funky Disco, Happy Rock',
        'spotify_playlist_url': 'https://open.spotify.com/playlist/37i9dQZF1EIeEZPgsd7pko'
    }
}
# --- END CONFIGURATION ---


# --- APP INITIALIZATION ---
app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Global variable to store the sentiment analyzer, initialized once
sentiment_analyzer = None

# Function to load the model, ensuring it's done only once and handling potential errors
def load_sentiment_model():
    global sentiment_analyzer
    if sentiment_analyzer is None:
        print(f"Attempting to load sentiment model: {MODEL_NAME}...")
        try:
            # The pipeline automatically handles downloading and caching the model
            sentiment_analyzer = pipeline("sentiment-analysis", model=MODEL_NAME)
            print("Sentiment model loaded successfully!")
        except Exception as e:
            print(f"CRITICAL ERROR: Failed to load sentiment model {MODEL_NAME}. Please check internet connection or model name.")
            print(f"Details: {e}")
            # If the model can't be loaded, the app can't function. Exit or set a flag.
            # For a production app, you might want a more graceful retry mechanism.
            # For a mini-project, exiting is acceptable if it's a critical dependency.
            sys.exit(1) # Exit the application if model loading fails
    else:
        print("Sentiment model already loaded.")

# Call this function when the app starts
# This ensures the model is ready before any requests come in
with app.app_context():
    load_sentiment_model()

# --- END APP INITIALIZATION ---


@app.route('/')
def home():
    """
    Basic home route to confirm the server is running.
    """
    return "MoodTunes Backend is running! Send POST requests to /analyze_journal"

@app.route('/analyze_journal', methods=['POST'])
def analyze_journal():
    """
    API endpoint to analyze journal entry sentiment and recommend music.
    Expects a JSON payload with a 'journal_entry' key.
    """
    # Check if the sentiment model is actually loaded before processing
    if sentiment_analyzer is None:
        print("Error: Sentiment model is not loaded. Cannot process request.")
        return jsonify({"error": "Backend not ready: Sentiment model failed to load."}), 503 # Service Unavailable

    try:
        data = request.get_json()
        journal_entry = data.get('journal_entry')

        if not journal_entry:
            # Log the request and error for debugging.
            print(f"Received empty journal_entry from {request.remote_addr}")
            return jsonify({"error": "No journal_entry provided"}), 400

        # Perform sentiment analysis
        # The sentiment_analyzer returns a list of dictionaries, e.g.,
        # [{'label': 'LABEL_2', 'score': 0.998}]
        sentiment_result = sentiment_analyzer(journal_entry)[0]
        sentiment_label = sentiment_result['label']
        
        # Log the sentiment analysis result for debugging
        print(f"Journal entry analyzed: '{journal_entry[:50]}...' -> Label: {sentiment_label}, Score: {sentiment_result['score']:.4f}")

        # Get the corresponding mood and music recommendation from our map
        # This 'recommendation' dictionary already contains 'spotify_playlist_url'
        recommendation = MOOD_MUSIC_MAP.get(sentiment_label, {
            'mood': 'Undetermined',
            'music_description': 'Explore various genres!',
            'spotify_playlist_url': '#' # Fallback URL if label not found
        })
        
        # Log the final recommendation
        print(f"Recommended Mood: {recommendation['mood']}, Music: {recommendation['music_description']}")

        # Return the results as a JSON response
        # The spotify_playlist_url is directly from the 'recommendation' dictionary
        return jsonify({
            "detected_mood": recommendation['mood'],
            "recommended_music": recommendation['music_description'],
            "spotify_playlist_url": recommendation['spotify_playlist_url'], # This is now directly from the map
            "raw_sentiment_label": sentiment_label,
            "raw_sentiment_score": sentiment_result['score']
        })

    except Exception as e:
        # Log the error for debugging purposes
        # traceback.format_exc() provides a detailed stack trace
        error_details = traceback.format_exc()
        print(f"An unhandled error occurred during /analyze_journal request: {e}\n{error_details}")
        return jsonify({"error": "Internal server error", "details": error_details}), 500

if __name__ == '__main__':
    # Ensure the model is loaded before starting the server
    # load_sentiment_model()

    # Run the Flask app on localhost:5000
    # debug=True allows for automatic reloading on code changes and provides a debugger
    app.run(debug=True, host='127.0.0.1', port=5000)

