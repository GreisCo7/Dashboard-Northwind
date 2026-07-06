# Tarea N°3 - Dashboards en Python
# Integrantes: Greisy Coronado (8-1031-491), Alejandro Gonzáles ( )


from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px


from consulta import (
    obtener_clientes,
    obtener_productos,
    obtener_productos_completos
)

from procesamientos import (
    promedio_precio,
    clientes_por_ciudad,
    top_productos_caros,
    productos_por_categoria,
    productos_sin_stock
)


# Cargar datos ---------------------------------

clientes = obtener_clientes()
productos = obtener_productos()

productos_completos = obtener_productos_completos()

categorias_lista = sorted(
    productos_completos["CategoryName"].unique()
)


clientes_ciudad = clientes_por_ciudad(clientes)

productos_top = top_productos_caros(productos)

categorias = productos_por_categoria(productos_completos)

sin_stock = productos_sin_stock(productos)
# Cantidad de productos
cantidad_sin_stock = len(sin_stock)

cantidad_con_stock = len(productos) - cantidad_sin_stock

estado_stock = {
    "Estado": ["Con stock", "Sin stock"],
    "Cantidad": [cantidad_con_stock, cantidad_sin_stock]
}



# Colores del Dashboard ------------------------

COLOR_FONDO = "#0B1F3A"
COLOR_TARJETA = "#162C4E"
COLOR_TEXTO = "white"
COLOR_TITULO = "#4FC3F7"

# Crear gráficas -------------------------------

grafica_clientes = px.bar(
    clientes_ciudad,
    x="City",
    y="Cantidad",
    title="Clientes por ciudad",
    template="plotly_dark",
    color_discrete_sequence=["#4FC3F7"]
)

grafica_clientes.update_layout(
    paper_bgcolor=COLOR_TARJETA,
    plot_bgcolor=COLOR_TARJETA
)

grafica_productos = px.bar(
    productos_top,
    x="UnitPrice",
    y="ProductName",
    orientation="h",
    title="Top 10 productos más caros",
    template="plotly_dark",
    color_discrete_sequence=["#4FC3F7"]
)

grafica_productos.update_layout(
    paper_bgcolor=COLOR_TARJETA,
    plot_bgcolor=COLOR_TARJETA
)

grafica_categorias = px.pie(
    categorias,
    names="CategoryName",
    values="Cantidad",
    title="Productos por categoría",
    template="plotly_dark",
    color_discrete_sequence=["#4FC3F7"]
)

grafica_categorias.update_layout(
    paper_bgcolor=COLOR_TARJETA
)

grafica_stock = px.pie(
    estado_stock,
    names="Estado",
    values="Cantidad",
    title="Estado del inventario",
    hole=0.55,
    template="plotly_dark",
    color="Estado",
    color_discrete_map={
        "Con stock": "#4FC3F7",
        "Sin stock": "#FF6B6B"
    }
)

grafica_stock.update_layout(
    paper_bgcolor=COLOR_TARJETA,
    plot_bgcolor=COLOR_TARJETA,
    font_color="white",
    legend_bgcolor="rgba(0,0,0,0)",
    title_x=0.5
)

grafica_stock.update_layout(
    paper_bgcolor=COLOR_TARJETA,
    plot_bgcolor=COLOR_TARJETA
)

# Crear aplicación -----------------------------

app = Dash(__name__)


# Layout ---------------------------------------

def tarjeta(titulo, valor):

    return html.Div(

        children=[

            html.H4(
                titulo,
                style={
                    "color": COLOR_TITULO,
                    "marginBottom": "10px"
                }
            ),

            html.H2(
                valor,
                style={
                    "color": COLOR_TEXTO
                }
            )

        ],

        style={
            "backgroundColor": COLOR_TARJETA,
            "padding": "20px",
            "borderRadius": "10px",
            "textAlign": "center",
            "width": "22%",
            "boxShadow": "2px 2px 10px rgba(0,0,0,0.3)"
        }
    )


def caja_grafica(grafica, id=None):

    if id:
        graph = dcc.Graph(
            id=id,
            figure=grafica,
            config={"displayModeBar": False}
        )
    else:
        graph = dcc.Graph(
            figure=grafica,
            config={"displayModeBar": False}
        )

    return html.Div(

        graph,

        style={
            "backgroundColor": COLOR_TARJETA,
            "padding": "15px",
            "borderRadius": "10px",
            "width": "49%",
            "boxShadow": "2px 2px 10px rgba(0,0,0,0.3)"
        }

    )

app.layout = html.Div(

    style={
        "fontFamily": "Arial",
        "padding": "25px",
        "backgroundColor": COLOR_FONDO,
        "minHeight": "100vh"
    },

    children=[

        html.H1(
            
            "Dashboard Northwind",
            style={
                "textAlign": "center",
                "color": COLOR_TEXTO,
                "marginBottom": "30px"
            }
        ),

        html.Hr(),

    
        # Métricas -------------------------

        html.Div(
            
            children=[
                
                tarjeta("Clientes", len(clientes)),
                
                tarjeta("Productos", len(productos)),
                
                tarjeta(
                    
                    "Categorías",
                    productos_completos["CategoryName"].nunique()
                ),
                
                tarjeta(
                    "Precio Promedio",
                    f"{promedio_precio(productos):.2f}"
                )
            ],
            
            style={
                
                "display": "flex",
                "justifyContent": "space-between",
                "marginBottom": "40px"
            }
        ),
        
        html.Div(
            
            [
                
                html.Div(
                    
                    [
                        html.Label(
                            "Categoría",
                            style={"color":"white"}
                        ),
                        
                        dcc.Dropdown(
                            id="dropdown-categoria",
                            options=[
                                {"label":"Todas","value":"Todas"}
                                ] + [
                                    {"label":c,"value":c}
                                    for c in categorias_lista
                                    ],
                                value="Todas",
                                clearable=False
                            )
                    ],
                    
                    style={"width":"45%"}
                    ),
                
                html.Div(
                    
                    [
                        html.Label(
                            "Precio mínimo",
                            style={"color":"white"}
                            ),
                        
                        dcc.Slider(
                            id="slider-precio",
                            min=0,
                            max=100,
                            step=5,
                            value=0,
                            marks={
                                i: {
                                    "label": str(i),
                                    "style": {"color": "white"}
                                    }
                                for i in range(0, 101, 20)
                            }
                        )
                    ],
                    
                    style={"width":"45%"}
                )
            ],
            
            style={
                
                "display":"flex",
                "justifyContent":"space-between",
                "marginBottom":"30px"
            }
        ),

        # Gráficas -------------------------

        html.Div(

            children=[

                # Primera fila
                html.Div(

                    [

                        caja_grafica(grafica_clientes),

                        caja_grafica(grafica_categorias)

                    ],

                    style={

                        "display": "flex",
                        "gap": "20px",
                        "marginTop": "30px"

                    }

                ),

                # Segunda fila
                html.Div(

                    [

                        caja_grafica(
                            grafica_productos,
                            id="grafica-productos"
                        ),

                        caja_grafica(grafica_stock)

                    ],

                    style={

                        "display": "flex",
                        "gap": "20px",
                        "marginTop": "20px"

                    }
                )
            ]
        ),
    ]
)

# Tablas de datos ---------------------------

html.Hr(),

html.H2(
    "Datos originales",
    style={"marginTop": "30px"}
),

html.H3("Clientes"),

dash_table.DataTable(

    data=clientes.to_dict("records"),

    columns=[
        {"name": i, "id": i}
        for i in clientes.columns
    ],

    page_size=10,

    style_table={
        "overflowX": "auto"
    },

    style_cell={
        "textAlign": "left"
    }

),

html.Br(),

html.H3("Productos"),

dash_table.DataTable(

    data=productos.to_dict("records"),

    columns=[
        {"name": i, "id": i}
        for i in productos.columns
    ],

    page_size=10,

    style_table={
        "overflowX": "auto"
    },

    style_cell={
        "textAlign": "left"
    }

)


# Callback ---------------------------------

@app.callback(

    Output("grafica-productos", "figure"),

    Input("dropdown-categoria", "value"),

    Input("slider-precio", "value")

)

def actualizar_grafica(categoria, precio):

    df = productos_completos.copy()

    if categoria != "Todas":
        df = df[df["CategoryName"] == categoria]

    df = df[df["UnitPrice"] >= precio]

    figura = px.bar(
        
    df,
    x="UnitPrice",
    y="ProductName",
    orientation="h",
    title="Productos",
    template="plotly_dark",
    color_discrete_sequence=["#4FC3F7"]
    )
    
    figura.update_layout(
    paper_bgcolor=COLOR_TARJETA,
    plot_bgcolor=COLOR_TARJETA,
    font_color="white"
    )

    return figura

# Ejecutar servidor ------------------------

if __name__ == "__main__":
    app.run(debug=True)
    