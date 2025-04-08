from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL is missing"}), 400
    return jsonify({"message": f"Получил ссылку: {url}"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
