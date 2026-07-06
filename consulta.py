import pandas as pd
from conexion import conectar


def ejecutar_consulta(query):
    """
    Ejecuta una consulta SQL y devuelve los resultados
    en un DataFrame de Pandas.
    """
    conn = conectar()

    if conn is None:
        return pd.DataFrame()

    try:
        df = pd.read_sql(query, conn)
        return df

    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return pd.DataFrame()

    finally:
        conn.close()



# Clientes --------------------------------

def obtener_clientes():
    query = """
        SELECT CustomerID, CompanyName, City
        FROM Customers
    """
    return ejecutar_consulta(query)



# Productos --------------------------------

def obtener_productos():
    query = """
        SELECT ProductName, UnitPrice, UnitsInStock
        FROM Products
    """
    return ejecutar_consulta(query)


def obtener_productos_completos():
    query = """
        SELECT
            p.ProductID,
            p.ProductName,
            c.CategoryName,
            s.CompanyName AS Supplier,
            p.UnitPrice,
            p.UnitsInStock,
            p.UnitsOnOrder,
            p.Discontinued
        FROM Products p
        INNER JOIN Categories c
            ON p.CategoryID = c.CategoryID
        INNER JOIN Suppliers s
            ON p.SupplierID = s.SupplierID
    """
    return ejecutar_consulta(query)



# Categorías --------------------------------

def obtener_categorias():
    query = """
        SELECT CategoryID, CategoryName
        FROM Categories
    """
    return ejecutar_consulta(query)



# Empleados --------------------------------

def obtener_empleados():
    query = """
        SELECT EmployeeID,
               FirstName,
               LastName,
               City
        FROM Employees
    """
    return ejecutar_consulta(query)



# Proveedores --------------------------------

def obtener_proveedores():
    query = """
        SELECT SupplierID,
               CompanyName,
               Country
        FROM Suppliers
    """
    return ejecutar_consulta(query)



# Pedidos --------------------------------

def obtener_pedidos():
    query = """
        SELECT OrderID,
               CustomerID,
               EmployeeID,
               OrderDate,
               ShipCountry
        FROM Orders
    """
    return ejecutar_consulta(query)


def obtener_pedidos_completos():
    query = """
        SELECT
            o.OrderID,
            o.OrderDate,
            o.ShipCountry,
            c.CompanyName AS Cliente,
            e.FirstName + ' ' + e.LastName AS Empleado
        FROM Orders o
        INNER JOIN Customers c
            ON o.CustomerID = c.CustomerID
        INNER JOIN Employees e
            ON o.EmployeeID = e.EmployeeID
    """
    return ejecutar_consulta(query)



# Prueba del módulo --------------------------------

if __name__ == "__main__":
    print("Clientes")
    print(obtener_clientes().head())

    print("\nProductos")
    print(obtener_productos().head())

    print("\nProductos completos")
    print(obtener_productos_completos().head())

    print("\nPedidos")
    print(obtener_pedidos().head())