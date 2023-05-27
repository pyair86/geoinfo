from geoinfo.app.app import app
from geoinfo.app import db


def test_status():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b'<div id="map"></div>' in response.data


def test_db():
    conn = db.connect()
    db.truncate_table(conn)
    assert db.count_rows(conn) == 0

    db.add_initial_points(conn)
    assert db.count_rows(conn) == 2

    db.disconnect(conn)


