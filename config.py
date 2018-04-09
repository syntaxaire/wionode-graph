import os
import logging
import configparser

logging.basicConfig(level=logging.DEBUG)

basedir = os.path.abspath(os.path.dirname(__file__))
logging.debug(f"basedir is {basedir}")
pardir = os.path.abspath(os.path.join(basedir, os.pardir))
logging.debug(f"pardir is {pardir}")
config = configparser.ConfigParser()
configfile = 'config.cfg'
configpath = os.path.join(basedir, configfile)
logging.debug(f"Reading config from {configpath}")
config.read(configpath)
dbpath = os.path.join(basedir, config['DB']['dbfile'])
logging.debug(f"database is at {dbpath}")


class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + dbpath
    SQLALCHEMY_TRACK_MODIFICATIONS = False
