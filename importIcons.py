# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import pyodbc
import yaml
import pprint
from sqlalchemy import create_engine, Column, MetaData, Table, Index
from sqlalchemy import Integer, String, Text, Float, Boolean, BigInteger, Numeric, SmallInteger

import ConfigParser, os
fileLocation = os.path.dirname(os.path.realpath(__file__))
inifile=fileLocation+'/sdeloader.cfg'
config = ConfigParser.ConfigParser()
config.read(inifile)
destination=config.get('Database','destination')
sourcePath=config.get('Files','sourcePath')

print "connecting to DB"
engine = create_engine('destination')
connection = engine.connect()



metadata = MetaData()

print "Setting up Tables"

eveIcons = Table('eveIcons',metadata,
                Column('iconID',Integer,primary_key=True, autoincrement=False),
                Column('iconFile',String(500)),
                Column('description',Text)
                )


metadata.create_all(engine,checkfirst=True)

print "opening Yaml"
with open(sourcePath+'iconIDs.yaml','r') as yamlstream:
    print "importing"
    trans = connection.begin()
    icons=yaml.load(yamlstream,Loader=yaml.CSafeLoader)
    print "Yaml Processed into memory"
    for icon in icons:
        connection.execute(eveIcons.insert(),
                           iconID=icon,
                           iconFile=icons[icon].get('iconFile',''),
                           description=icons[icon].get('description',''))
trans.commit()
