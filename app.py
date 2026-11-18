import os
from datetime import date

from flask import Flask, Response, render_template, request, jsonify

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Public address of the live site, used for canonical links, the sitemap and
# structured data. Set SITE_URL on Render (e.g. https://www.purvitech.com) once
# you have a custom domain.
SITE_URL = os.environ.get("SITE_URL", "https://purvi-technologies.onrender.com").rstrip("/")

# Code from Google Search Console's "HTML tag" verification method
# (only the content="..." value).
GOOGLE_VERIFICATION = os.environ.get("GOOGLE_SITE_VERIFICATION", "")


@app.context_processor
def inject_seo():
    return {"site_url": SITE_URL, "google_verification": GOOGLE_VERIFICATION}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/robots.txt")
def robots():
    body = f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"
    return Response(body, mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{SITE_URL}/</loc><lastmod>{date.today().isoformat()}</lastmod>"
        "<changefreq>weekly</changefreq><priority>1.0</priority></url>\n"
        "</urlset>\n"
    )
    return Response(xml, mimetype="application/xml")


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
