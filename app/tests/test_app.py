from app import app
from app import db


def test_status_200():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b'<div id="map"></div>' in response.data


def test_status_404():
    client = app.test_client()
    response = client.get('/doesntExist')
    assert response.status_code == 404
    assert b'<p> :/ content not found.</p>' in response.data


def test_db():
    conn = db.connect()
    db.truncate_table(conn)
    assert db.count_rows(conn) == 0

    db.add_initial_points(conn)
    assert db.count_rows(conn) == 2

    db.disconnect(conn)


