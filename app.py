from flask import Flask, render_template, request, send_file, redirect, url_for
import yt_dlp
import os

app = Flask(__name__)

# Define download directory
DOWNLOAD_DIR = 'downloads'

# Ensure the download directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form['url']
    if video_url:
        try:
            # Prepare yt-dlp options
            ydl_opts = {
                'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
                'format': 'bestvideo+bestaudio/best',
            }

            # Download video using yt-dlp
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                video_title = ydl.prepare_filename(info)

            # Provide the video file for download
            return send_file(video_title, as_attachment=True)

        except Exception as e:
            return f"An error occurred: {str(e)}"
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
