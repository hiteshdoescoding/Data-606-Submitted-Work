import pyodbc

#pyodbc is py open database connectivity, print(pyodbc.drivers())


connection = pyodbc.connect(
    "DRIVER={ODBC DRIVER 18 for SQL Server};"
    "SERVER=localhost\\SQLSERVER2019;"
    "DATABASE=Northwind;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

cursor = connection.cursor()

cursor.execute("SELECT @@VERSION")

row = cursor.fetchone()

print(row[0])