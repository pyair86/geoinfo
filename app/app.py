from psycopg2 import sql
from flask import Flask, render_template, jsonify, request, flash

import db as db

app = Flask(__name__)

app.secret_key = "geoinfo"


@app.route("/add_point", methods=["POST"])
def add_point():
    if request.method == "POST":
        try:
            resp = request.json
            conn = db.connect()
            db.add_point(resp, sql, conn)
            db.disconnect(conn)
            return jsonify(resp)
        except:
            flash("There was a problem while adding the point", "error")
            return render_template("main.html")


@app.route("/")
def index():
    return render_template("main.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/points")
def get_points():
    conn = db.connect()
    geojson = db.query(conn)
    db.disconnect(conn)
    if geojson:
        return jsonify(geojson)
    return render_template("main.html")


if __name__ == "__main__":
    app.run(debug=True)
