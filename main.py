from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL is missing"}), 400

    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "forcejson": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return jsonify({
            "video_url": info.get("url"),
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
