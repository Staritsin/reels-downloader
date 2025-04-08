from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL is missing"}), 400

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.70 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    html = response.text

    try:
        video_url = html.split('"video_url":"')[1].split('"')[0].replace("\\u0026", "&")
        thumbnail = html.split('"thumbnail_src":"')[1].split('"')[0].replace("\\u0026", "&")
        title = html.split('"title":"')[1].split('"')[0]
    except Exception as e:
        return jsonify({"error": f"Парсинг не удался: {str(e)}"}), 500

    return jsonify({
        "video_url": video_url,
        "thumbnail": thumbnail,
        "title": title
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
