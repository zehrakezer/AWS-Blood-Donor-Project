import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm

from sqlalchemy import create_engine

# Update the DATABASE_URL for MySQL on AWS RDS
# Replace <username>, <password>, <hostname>, <dbname> with your actual MySQL credentials and database details
DATABASE_URL = "mysql+pymysql://admin:password@kanbagisdb.clwamwmci9vk.eu-central-1.rds.amazonaws.com:63306/kanbagisdb"

# Create engine for connecting to MySQL
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=10, pool_timeout=30, pool_recycle=3600)


# SessionLocal is used to create a session for interacting with the database
SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = _declarative.declarative_base()




"""# SQLITE
DATABASE_URL = "sqlite:///./database.db"
engine = _sql.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = _declarative.declarative_base()
"""
