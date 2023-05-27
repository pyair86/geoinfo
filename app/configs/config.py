import os


postgres = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DATABASE_NAME", "postgres"),
    "user": os.getenv("DB_USERNAME", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "port": os.getenv("DB_PORT", 5433),
}
