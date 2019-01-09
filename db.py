#!flask/bin/python
import pyodbc 

server = 'kms-db.database.windows.net'
database = 'kms_dev'
username = 'kmsadmin@kms-db'
password = 'Dotvik@98765'
driver= '{SQL Server}'
connectionString = 'DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password
print(connectionString)
cnxn = pyodbc.connect(connectionString)