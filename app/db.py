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
            port=postgres["port"],
        )
        return conn

    except Exception as e:
        raise f"Can not connect to DB, {e}"


def add_point(resp, sql, conn):
    name = resp["name"]
    lat = resp["lat"]
    long = resp["long"]

    insert_query = sql.SQL(
        "INSERT INTO geoinfo.points (geom_2056,name, geom_4326) VALUES (ST_SetSRID(ST_MakePoint({}, {}), 2056), {}, ST_MakePoint({}, {}));"
    ).format(
        sql.Literal(long),
        sql.Literal(lat),
        sql.Literal(name),
        sql.Literal(long),
        sql.Literal(lat),
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
            "properties": {"name": name},
        }
        features.append(feature)

    geojson = {"type": "FeatureCollection", "features": features}
    return geojson


def query(conn):
    with conn.cursor() as cur:
        sql = "SELECT name, ST_AsGeoJSON(geom_4326) FROM geoinfo.points"
        cur.execute(sql)
        rows = cur.fetchall()
        geojson = create_geojson(rows)
        return geojson


def set_postgis(conn):
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION postgis;")
        conn.commit()


def truncate_table(conn):
    with conn.cursor() as cur:
        sql = "TRUNCATE geoinfo.points;"
        cur.execute(sql)
        conn.commit()


def count_rows(conn):
    with conn.cursor() as cur:
        sql = "SELECT COUNT(*) FROM geoinfo.points"
        cur.execute(sql)
        count = cur.fetchone()[0]
        return count


def create_table(conn):
    with conn.cursor() as cur:
        sql = """  CREATE TABLE geoinfo.points
                                (
                                    id serial PRIMARY KEY,
                                    name text CONSTRAINT nameCheck CHECK (char_length(name) <= 30) DEFAULT GEOINFO NOT NULL,
                                    geom_4326 geometry(Point, 4326) NOT NULL,
                                    geom_2056 geometry(Point, 2056) NOT NULL
                                );
                                """
        cur.execute(sql)
        conn.commit()


def create_index(conn):
    with conn.cursor() as cur:
        sql = """
            CREATE INDEX geoinfo_points_geom_idx
              ON geoinfo.points
              USING gist
              (geom_2056);
            """
        cur.execute(sql)
        conn.commit()


def add_constraints(conn):
    with conn.cursor() as cur:
        sql = """
            ALTER TABLE geoinfo.points
        
            ADD CONSTRAINT
                check_dims_geom
            CHECK (st_ndims(geom) = 0)
            ;
        """
        cur.execute(sql)


def add_initial_points(conn):
    with conn.cursor() as cur:
        sql = """
            INSERT INTO geoinfo.points (geom_2056, name, geom_4326) VALUES
            (
            ST_SetSRID(ST_MakePoint(10.4674, 45.653), 2056), 
             'geoinfo_city',
            ST_MakePoint(10.4674, 45.653)
            );"""

        cur.execute(sql)
        sql = """
            INSERT INTO geoinfo.points (geom_2056, name, geom_4326) VALUES
            (
            ST_SetSRID(ST_MakePoint(10.3574, 45.653), 2056), 
            'geoinfo_city',
            ST_MakePoint(10.3574, 45.653)
            );"""

        cur.execute(sql)
        conn.commit()


def disconnect(conn):
    conn.close()
