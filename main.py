from flask import Flask, request, jsonify, send_from_directory, abort
import yt_dlp
import os
import tempfile
import requests
from openai import OpenAI
from dotenv import load_dotenv
import shutil

# Загрузка переменных окружения
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Константы
DOWNLOAD_PATH = "static"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# Flask приложение
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ ReelsDownloader API работает!"

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    try:
        # Создаем временную папку для скачивания
        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts = {
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'quiet': True,
                'noplaylist': True,
                'geo_bypass': True,
                'nocheckcertificate': True,
                'cookiefile': 'cookies.txt',
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            # Определяем реальное имя и расширение
            basename = os.path.basename(filename)
            target_path = os.path.join(DOWNLOAD_PATH, basename)

            # Перемещаем файл из временной папки в статическую
            shutil.move(filename, target_path)

        public_url = f"{request.host_url}static/{basename}"
        return jsonify({"url": public_url})

    except Exception as e:
        return jsonify({"error": f"Download failed: {str(e)}"}), 500

@app.route("/transcribe", methods=["POST"])
def transcribe():
    data = request.get_json()
    video_url = data.get("url")
    if not video_url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    try:
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
            r = requests.get(video_url, stream=True)
            for chunk in r.iter_content(chunk_size=8192):
                tmp_file.write(chunk)
            tmp_path = tmp_file.name

        with open(tmp_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="text"
            )
            transcribed_text = transcript.text if hasattr(transcript, 'text') else transcript

        os.remove(tmp_path)
        return jsonify({"transcription": transcribed_text})

    except Exception as e:
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500

@app.route("/static/<path:filename>")
def serve_file(filename):
    if os.path.exists(os.path.join(DOWNLOAD_PATH, filename)):
        return send_from_directory(DOWNLOAD_PATH, filename)
    else:
        abort(404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
