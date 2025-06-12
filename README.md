# MoodTunes

### Project Overview
'MoodTunes' is an AI-powered mini-project designed to personalize music recommendations by analyzing a user's real-time emotional state extracted from journal entries. This system innovatively detects underlying moods and curates tailored music playlists, directly linking them to Spotify.

### Features
-   **Mood Detection:** Utilizes Natural Language Processing (NLP) with the Hugging Face Transformers library (specifically the `cardiffnlp/twitter-roberta-base-sentiment` model) for advanced sentiment analysis of unstructured text. [Learn more about the model used](https://huggingface.co/blog/sentiment-analysis-twitter)
-   **Music Recommendation:** Dynamically maps detected moods to pre-selected Spotify playlists.
-   **Interactive Web UI:** Features a responsive user interface built with HTML, CSS (Tailwind CSS), and JavaScript for seamless user interaction.

### Technologies Used
-   Python (Flask, Transformers library)
-   HTML, CSS (Tailwind CSS)
-   JavaScript

### Installation and Setup
To set up and run MoodTunes on your local machine, follow these steps:

1.  **Download the Project Files:**
    * Manually download `app.py` and `index.html` into a new folder on your computer.

2.  **Set up the Python Backend (`app.py`):**
    * **Prerequisites:** Ensure you have Python 3.10 or more installed.
    * **Install Dependencies:** Open your terminal or command prompt, navigate to the folder where you saved `app.py`, and install the required Python libraries:
        ```bash
        pip install Flask transformers torch
        # If 'torch' installation causes issues, you can try:
        # pip install Flask transformers tensorflow
        ```
    * **Update Spotify Playlists:** Open `app.py` in a text editor. In the `MOOD_MUSIC_MAP` section, **replace the placeholder Spotify playlist URLs** (for eg: `https://open.spotify.com/playlist/YOUR_NEGATIVE_PLAYLIST_ID_HERE` etc.) with the actual "Share link to playlist" URLs from your chosen Spotify playlists.
    * **Run the Backend Server:** In the same terminal, execute `app.py`:
        ```bash
        python app.py
        ```
        Keep this terminal window open and running. You should see output indicating the Flask server is active (e.g., `Running on http://127.0.0.1:5000`).

3.  **Access the Web Frontend (`index.html`):**
    * **Open the HTML File:** Navigate to the folder where you saved `index.html` on your computer. Double-click `index.html` to open it in your preferred web browser (e.g., Chrome, Edge, Firefox).
    * **Interact with MoodTunes:**
        * Type a journal entry into the provided text area.
        * Click the "Get My MoodTunes" button.
        * The system will analyze your entry, display the detected mood and recommended music, and provide a clickable link to the corresponding Spotify playlist.

---

### Contributors
This project was developed as a 2nd year mini-project for AI-ML by the following team members:

* **Sharvesh R** - USN: 1NH23AI147 (Role: Project Report handling)
* **Shreyas Pai** - USN: 1NH23AI151 (Role: Lead Backend Developer, Sentiment Analysis Integration)
* **Sumanth Kalyan K** - USN: 1NH23AI159 (Role: Frontend Developer, Webpage Design)


### License
[MIT License](LICENSE.md)

### Acknowledgements
Special Thanks to :
* Dr. N.V. Uma Reddy (HoD of AIML (NHCE)) & Prof. Syam Dev R.S. (Senior Assistant Professor of AIML (NHCE), and our project guide) & Prof. Ramesh Prasad (Senior Assistant Professor of AIML (NHCE), and our project coordinator).
* `2024-2025, AIML Department, New Horizon College of Engineering, Bengaluru, Karnataka, India`
    
