import psycopg2
import json

from configs.config import postgres


def connect():

    try:
        conn = psycopg2.connect(
                host=postgres["host"],
                database=postgres["database"],
                user=postgres["user"],
                password=postgres["password"],
                port=postgres["port"]
        )
        return conn

    except Exception as e:
        raise f"Can not connect to DB, {e}"


def add_point(resp, sql, conn):
    name = resp['name']
    lat = resp['lat']
    long = resp['long']

    insert_query = sql.SQL(
        "INSERT INTO geoinfo.points (geom,name, geom_4326) VALUES (ST_SetSRID(ST_MakePoint({}, {}), 2056), {}, ST_MakePoint({}, {}));").format(
        sql.Literal(long),
        sql.Literal(lat),
        sql.Literal(name),
        sql.Literal(long),
        sql.Literal(lat)
    )

    with conn.cursor() as cursor:
        cursor.execute(insert_query)

    conn.commit()


def create_geojson(rows):
    features = []

    for row in rows:
        name = row[0]
        geom = row[1]
        geometry = json.loads(geom)
        feature = {
            "type": "Feature",
            "geometry": geometry,
            "properties": {"name":name}
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    return geojson


def query(conn):
    cur = conn.cursor()
    sql = "SELECT name, ST_AsGeoJSON(geom_4326) FROM geoinfo.points"
    cur.execute(sql)
    rows = cur.fetchall()
    geojson = create_geojson(rows)
    cur.close()
    return geojson


def disconnect(conn):
    conn.close()
