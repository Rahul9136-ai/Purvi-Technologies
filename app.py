from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    if not name:
        return jsonify({"success": False, "message": "Name is required."}), 400
    return jsonify({
        "success": True,
        "message": f"Thanks {name}! We'll get back to you within 24 hours.",
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
