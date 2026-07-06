import pyodbc

SERVER = "DESKTOP-D2QEQ63\\SQLEXPRESS01"
DATABASE = "Northwind"

CONNECTION_STRING = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
)


def conectar():
    """
    Establece una conexión con la base de datos Northwind.
    """
    try:
        return pyodbc.connect(CONNECTION_STRING)

    except pyodbc.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None