from flask import Flask, render_template,jsonify
import db

# todo add to improvements linters, spatial constrains
#todo convert espg of coords
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/data')
def get_points():
    conn = db.connect()
    geojson = db.query(conn)
    db.disconnect(conn)
    return jsonify(geojson)


if __name__ == '__main__':
    app.run(debug=True)
