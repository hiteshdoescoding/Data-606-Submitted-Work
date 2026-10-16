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

# cursor.execute("SELECT COUNT (*) FROM Customers")
# row = cursor.fetchone()
# print(row[0])

# rows = cursor.execute(
#     "SELECT * FROM Customers"
# ).fetchall()
# print(len(rows))

# rows = cursor.execute(
#     "SELECT ProductName, UnitPrice FROM Products"
# ).fetchall()
#
# for row in rows:
#     print(row.ProductName, row.UnitPrice)



# results = cursor.execute(
#     "SELECT * FROM Products"
# )
#
# while True:
#     row = results.fetchone()
#
#     if row is None:
#         break
#
#     print(row.ProductName)



# results = cursor.execute(
#     "SELECT * FROM Products"
# )
#
# while True:
#     batch = results.fetchmany(10)
#
#     if not batch:
#         break
#     for row in batch:
#         print(row.ProductName)



# rows = cursor.execute(
#     "SELECT * FROM Customers WHERE City = ?",                  # helps to avoid sql injection
#     city
# ).fetchall()
#
# for row in rows:
#     print(row.CompanyName, row.City)


cursor.close()
connection.close()     #these are for good practice, remember to close db connection and cursor before ending your file
