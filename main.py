app = Flask(__name__)

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL is missing"}), 400
    return jsonify({"message": f"Получил ссылку: {url}"}), 200

# ЭТО — ключевая строчка 👇
# Это позволяет gunicorn видеть переменную `app`
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8000)
