import db


def setup_data():
    conn = db.connect()
    db.create_schema(conn)
    db.create_table(conn)
    db.create_index(conn)
    db.add_constraints(conn)
    db.add_initial_points(conn)
    db.disconnect(conn)


if __name__ == "__main__":
    setup_data()
