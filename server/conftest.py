import os

# Keep test runs off the real dev database file.
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
