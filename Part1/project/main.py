from DataExcel import ExcelFile
import SQLController

# get excel data
dataFile = ExcelFile()

# create sql tables schema. This only needs to be run once, but it's idempotent
SQLController.createTablesSchema()

# insert excel data to SQL database.
SQLController.insertPdTableToDB(dataFile)
