def clientes_por_ciudad(df):
    """
    Cuenta la cantidad de clientes por ciudad.
    """
    return df.groupby("City").size().reset_index(name="Cantidad")


def productos_caros(df, precio=50):
    """
    Devuelve los productos cuyo precio sea mayor al indicado.
    """
    return df[df["UnitPrice"] > precio]


def promedio_precio(df):
    """
    Calcula el precio promedio de los productos.
    """
    return df["UnitPrice"].mean()


def top_productos_caros(df, cantidad=10):
    """
    Devuelve los productos más caros.
    """
    return df.sort_values(
        by="UnitPrice",
        ascending=False
    ).head(cantidad)


def estadisticas_precios(df):
    """
    Devuelve estadísticas básicas de los precios.
    """
    return df["UnitPrice"].describe()


def productos_sin_stock(df):
    """
    Devuelve los productos sin existencias.
    """
    return df[df["UnitsInStock"] == 0]


def productos_por_categoria(df):
    """
    Cuenta la cantidad de productos por categoría.
    Requiere el DataFrame de obtener_productos_completos().
    """
    return (
        df.groupby("CategoryName")
          .size()
          .reset_index(name="Cantidad")
          .sort_values("Cantidad", ascending=False)
    )