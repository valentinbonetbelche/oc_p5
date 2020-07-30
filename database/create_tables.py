# THIS FILE IS A SCRIPT THAT WILL CREATE THE TABLES IN OUR DATABASE
from sqlalchemy import create_engine

from models import Base


def create_tables(base, user, password, host, database_name):
    engine = create_engine("mysql+pymysql://" + user + ":" + password + "@" +
                           host + ":3306/" + database_name)
    base.metadata.create_all(engine)


create_tables(
    base=Base,
    host="localhost",
    user="root",
    password="admin",
    database_name="oc_p5")
