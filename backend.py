import os
import requests
import configparser
from sqlalchemy import Column, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import argparse
import logging
import datetime
import time
import json
import traceback

logging.basicConfig(level=logging.DEBUG)
sqlaBase = declarative_base()


class SensorEntry(sqlaBase):
    __tablename__ = 'sensor_entries'
    dt = Column(DateTime, primary_key=True)
    data = Column(Float)


def db_open(dbfile, dbpath):
    if not os.path.isfile(dbpath):
        raise FileNotFoundError
    engine = create_engine(f'sqlite:///{dbfile}')
    sqlaBase.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()
    return session


def db_init(dbfile, dbpath):
    try:
        logging.info(f"Removing {dbfile}...")
        os.remove(dbpath)
    except FileNotFoundError:
        logging.info(f"{dbfile} didn't exist.")
    except:
        logging.error(f"Couldn't remove {dbfile} for some reason (file locked or read-only?)")
        logging.error(f"Exiting.")
        exit()
    else:
        logging.info(f"Successfully removed.")

    engine = create_engine(f'sqlite:///{dbfile}')
    logging.info(f"Created {dbfile}")
    sqlaBase.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


def log(session, dt, data):
    entry = SensorEntry(dt=dt, data=data)
    session.add(entry)
    session.commit()
    logging.debug(f"Committed to database.")


def polling_loop(session, api, label):
    """Poll the API endpoint and log results to database session."""
    logging.info("Starting polling.")
    while True:
        try:
            r = requests.get(api)
            sensor = json.loads(r.text)
            data = sensor[f'{label}']
            dt = datetime.datetime.now()
            print(f"Time: {dt}, sensor reading: {data}")
            log(session, dt, data)
        except Exception as ex:
            tb_lines = traceback.format_exception(ex.__class__, ex, ex.__traceback__)
            tb_text = ''.join(tb_lines)
            logging.error(f"{datetime.datetime.now()} Error in polling loop:")
            logging.error(tb_text)
            logging.error("Continuing...")

        time.sleep(30)

def main():
    parser = argparse.ArgumentParser(description='Run the polling backend.')
    parser.add_argument('--createdb', help='initialize the database (will delete wionode-graph.db if it exists)', action='store_true')
    args = parser.parse_args()


    # load the config
    config = configparser.ConfigParser()
    config.read('config.cfg')
    api = config['API']['endpoint']
    label = config['API']['label']
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = config['DB']['dbfile']
    dbpath = os.path.join(basedir, dbfile)

    # open or initialize the database?
    try:
        session = db_open(dbfile, dbpath)
        justcreated = False
    except FileNotFoundError:
        logging.warning(f"Database was not found, creating.")
        session = db_init(dbfile, dbpath)
        justcreated = True
    if args.createdb and not justcreated:
        session = db_init(dbfile, dbpath)

    polling_loop(session, api, label)


if __name__ == '__main__':
    main()
