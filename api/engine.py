from sqlalchemy import create_engine

# Define the URI in a single location

uri = 'mysql+pymysql://root:1234@localhost/sigma_security'
#uri = 'mysql+pymysql://sauvageduck24:sigmasecurity@sauvageduck24.mysql.pythonanywhere-services.com/sauvageduck24$sigmasecurity'

# Create the shared engine
engine = create_engine(uri,pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800)