import os
from sqlalchemy import create_engine

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
DB_HOST = os.getenv("DB_HOST", "mysql")
DB_NAME = os.getenv("DB_NAME", "sigma_security")

uri = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
#uri = 'mysql+pymysql://sauvageduck24:sigmasecurity@sauvageduck24.mysql.pythonanywhere-services.com/sauvageduck24$sigmasecurity'

# Create the shared engine
engine = create_engine(uri, pool_size=10, max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800)