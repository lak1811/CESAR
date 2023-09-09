import mysql.connector
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output

# Connect to the MySQL database
mydatabase = mysql.connector.connect(
    host='sql10.freemysqlhosting.net',
    port=3306,
    user='sql10639123',
    passwd='VyKJuJnrrl',
    db='sql10639123',
    charset='utf8',
    use_unicode=True
)

# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    style={'scroll-behavior': 'smooth',
    'font-family': 'Times New Roman',
    'backgroundColor': 'White',
    'overflow-x': 'hidden'
    
    
           },
    children=[
        
        # Navigation Bar
        dbc.NavbarSimple(
            children=[
                
                dbc.NavItem(html.A("Professors", href="#professors", style={'margin-right': '30px', 'font-size': '13px', 'font-family': 'Courier New, Courier, monospace', 'font-weight': 'bold', 'color': 'black'})),
                dbc.NavItem(html.A("Publications", href="#publications", style={'margin-right': '30px', 'font-size': '13px', 'font-family': 'Courier New, Courier, monospace', 'font-weight': 'bold', 'color': 'black'})),
                dbc.NavItem(html.A("Education", href="#education", style={'margin-right': '30px', 'font-size': '13px', 'font-family': 'Courier New, Courier, monospace', 'font-weight': 'bold', 'color': 'black',})),
                dbc.NavItem(html.A("Capitulos De Livros", href="#capitulos", style={'margin-right': '30px', 'font-size': '13px', 'font-family': 'Courier New, Courier, monospace', 'font-weight': 'bold', 'color': 'black'})),
                dbc.NavItem(html.A("Projects", href="#projects", style={'margin-right': '30px', 'font-size': '13px', 'font-family': 'Courier New, Courier, monospace', 'font-weight': 'bold', 'color': 'black'})),
                dbc.NavItem(html.A("Producao Tecnica", href="#producao", style={'margin-right': '30px', 'font-size': '13px', 'font-family': 'Courier New, Courier, monospace', 'font-weight': 'bold', 'color': 'black'})),
                dbc.NavItem(html.A("Trabalhos", href="#trabalhos", style={'margin-right': '30px', 'font-size': '13px', 'font-family': 'Courier New, Courier, monospace', 'font-weight': 'bold', 'color': 'black',})),
                dbc.NavItem(html.A("Other Productions", href="#other", style={'font-size': '13px', 'font-family': 'Courier New, Courier, monospace', 'font-weight': 'bold', 'color': 'black'})),
                #dbc.NavItem(html.Img(src=app.get_asset_url('picproject.jpg'), style={'border-radius': '50%','box-shadow': '0px 0px 10px rgba(0, 0, 0, 0.2)','opacity': '0.9','width':'20px','height':'20px','position':'relative','top':'20px'})),






            ],
            
            brand=html.Div([
            html.Img(src=app.get_asset_url('picproject.jpg'), style={'border-radius': '50%','box-shadow': '0px 0px 10px rgba(0, 0, 0, 0.2)','opacity': '0.9','width':'50px','height':'50px','position':'relative','right':'100px','text-align':'left'}), # Replace 'logo.png' with your logo image path
            html.Span("Cesar MySQL System", style={'font-size': '20px', 'margin-left': '10px','position':'relative','right':'80px'}),
        ]),
            
            brand_href="#",
            
            color="Orange",
            dark=False,
            style={'font-size': '20px',  # Adjust font size as needed
           'font-family': 'Courier New, Courier, monospace',
           'font-weight': 'bold',
            'width': '100%',
            'position': 'fixed',
            'top': '0',    
            'color':'black',
            'z-index': '1000',
            'text-align':'left',
            'height':'60px'
            
           }
        ),
        dbc.Row(dbc.Col(html.H1("\n"))),
        dbc.Row(dbc.Col(html.H1("\n"))),
        dbc.Row(dbc.Col(html.H1("\n"))),
        dbc.Row(dbc.Col(html.H1("\n"))),
        dbc.Row(dbc.Col(html.H1("\n"))),
        dbc.Row(dbc.Col(html.H1("\n"))),
        dbc.Row(dbc.Col(html.H1("\n"))),
        dbc.Row(dbc.Col(html.H1("\n"))),
        dbc.Row(dbc.Col(html.H1("Hello! Welcome to the website!",style={'text-align':'center','color': '#333','font-family':'Brush Script MT, cursive'}))),
        html.Div(
        html.Img(src=app.get_asset_url('picproject.jpg'), style={'border-radius': '50%','box-shadow': '0px 0px 10px rgba(0, 0, 0, 0.2)','opacity': '0.9'}),
        style={'text-align': 'center'}
        ),
        dbc.Row(dbc.Col(html.H2("All the professors", id="professors"))),
        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    id="loading",
                    type="default",
                    children=html.Div(id="table-content")
                )
            )
        ),
    ],
    className="mt-4",
)


@app.callback(
    Output("table-content", "children"),
    [Input("loading", "type")]
)
# Define callback to fetch data and update the table content
def update_table(_):
    cursor = mydatabase.cursor(dictionary=True)
    
    # Fetch data from the 'testapp1_person' table
    cursor.execute("SELECT Full_name, City, State, Description, `Update`, ORCID, Workplace FROM testapp1_person ORDER BY Full_name")
    person_rows = cursor.fetchall()

    # Fetch data from the 'articles' table (change 'article_table_name' to the actual table name)
    cursor.execute("SELECT DISTINCT Fullname, TITLE, YEAR, LANG, ISSN, AUTHOR FROM testapp1_publications ORDER BY Fullname, YEAR")
    article_rows = cursor.fetchall()

    # Fetch data for table 3 from MySQL (replace 'YOUR_QUERY_FOR_TABLE3' with your actual query)
    cursor.execute("SELECT DISTINCT Nome,Year_INI,Year_FIN,Month_INI,Month_FIN,Course,Type,Discipline FROM testapp1_education order by Nome,Year_INI")
    table3_data = cursor.fetchall()

    # Fetch data for table 4 from MySQL (replace 'YOUR_QUERY_FOR_TABLE4' with your actual query)
    cursor.execute("SELECT DISTINCT Nome,Title,Year,Lang,Author FROM testapp1_capitulosdelivrospublicados ORDER BY Nome,Year")
    table4_data = cursor.fetchall()

    # Fetch data for table 5 from MySQL (replace 'YOUR_QUERY_FOR_TABLE5' with your actual query)
    cursor.execute("SELECT DISTINCT Fullname,Proj,YEAR_INI,YEAR_FIN,Natureza,Integrantes,Cordena FROM testapp1_project order by Fullname,YEAR_INI")
    table5_data = cursor.fetchall()

    # Fetch data for table 6 from MySQL (replace 'YOUR_QUERY_FOR_TABLE6' with your actual query)
    cursor.execute("SELECT DISTINCT Fullname,Course,Year,Integrantes from testapp1_producaotecnica order by Fullname,Year")
    table6_data = cursor.fetchall()

    # Fetch data for table 7 from MySQL (replace 'YOUR_QUERY_FOR_TABLE7' with your actual query)
    cursor.execute("SELECT DISTINCT `fullname`, `TITLE`, `YEAR`, `LANG`, `AUTHOR`, `ORDER`, `ORDER_OK` FROM `testapp1_trabalho` ORDER BY `fullname`,`YEAR`;")
    table7_data = cursor.fetchall()

    # Fetch data for table 8 from MySQL (replace 'YOUR_QUERY_FOR_TABLE8' with your actual query)
    cursor.execute("SELECT DISTINCT Fullname,YEAR,NATURE,INSTITUTION,COURSE,STUDENT,TYPE,SPONSOR from testapp1_otherproductions order by Fullname,YEAR")
    table8_data = cursor.fetchall()
    cursor.close()

    if not person_rows and not article_rows:
        return "No data available."

    person_table_rows = []
    for row in person_rows:
        row_html = html.Tr(
            [
                html.Td(row["Full_name"]),
                html.Td(row["City"]),
                html.Td(row["State"]),
                html.Td(row["Description"]),
                html.Td(row["Workplace"]),
                html.Td(row["Update"]),
                html.Td(row["ORCID"]),
            ]
        )
        person_table_rows.append(row_html)
    table1 = dbc.Table(
        [html.Thead(html.Tr([html.Th("Full_name"), html.Th("City"),html.Th("State"),html.Th("Description"),html.Th("Workplace"),html.Th("Update"),html.Th("ORCID")])), html.Tbody(person_table_rows)],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
    )

    article_table_rows = []
    for row in article_rows:
        row_html = html.Tr(
            [
                html.Td(row["Fullname"]),
                html.Td(row["TITLE"]),
                html.Td(row["YEAR"]),
                html.Td(row["LANG"]),
                html.Td(row["ISSN"]),
                html.Td(row["AUTHOR"]),
            ]
        )
        article_table_rows.append(row_html)
    table2 = dbc.Table(
        [html.Thead(html.Tr([html.Th("Fullname"), html.Th("TITLE"),html.Th("Year"),html.Th("Language"),html.Th("ISSN"),html.Th("AUTHOR")])), html.Tbody(article_table_rows)],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
    )

    # Create table 3
    table3_rows = []
    for row in table3_data:
        row_html = html.Tr(
            [
                html.Td(row["Nome"]),
                html.Td(row["Year_INI"]),
                html.Td(row["Year_FIN"]),
                html.Td(row["Month_INI"]),
                html.Td(row["Month_FIN"]),
                html.Td(row["Course"]),
                html.Td(row["Type"]),
                html.Td(row["Discipline"]),
                # Add more columns as needed
            ]
        )
        table3_rows.append(row_html)

    table3 = dbc.Table(
        [html.Thead(html.Tr([html.Th("Name"), html.Th("Year Start"),html.Th("Year End"),html.Th("Month Start"),html.Th("Month End"),html.Th("Course"),html.Th("Type"),html.Th("Discipline")])), html.Tbody(table3_rows)],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
    )

    # Create table 4
    table4_rows = []
    for row in table4_data:
        row_html = html.Tr(
            [
                html.Td(row["Nome"]),
                html.Td(row["Title"]),
                html.Td(row["Lang"]),
                
                html.Td(row["Author"]),
                html.Td(row["Year"]),
                # Add more columns as needed
            ]
        )
        table4_rows.append(row_html)

    table4 = dbc.Table(
        [html.Thead(html.Tr([ html.Th("Nome"),html.Th("Title"), html.Th("Language"),html.Th("Author"),html.Th("Year")])), html.Tbody(table4_rows)],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
    )

    # Create table 5
    table5_rows = []
    for row in table5_data:
        row_html = html.Tr(
            [
                html.Td(row["Fullname"]),
                html.Td(row["Proj"]),
                html.Td(row["YEAR_INI"]),
                html.Td(row["YEAR_FIN"]),
                html.Td(row["Natureza"]),
                html.Td(row["Integrantes"]),
                html.Td(row["Cordena"]),
                
                # Add more columns as needed
            ]
        )
        table5_rows.append(row_html)

    table5 = dbc.Table(
        [html.Thead(html.Tr([html.Th("Name"), html.Th("Project"),html.Th("Year Start"), html.Th("Year End"),html.Th("Natureza"), html.Th("Integrantes"),html.Th("Cordenas")])), html.Tbody(table5_rows)],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
    )

    # Create table 6
    table6_rows = []
    for row in table6_data:
        row_html = html.Tr(
            [
                html.Td(row["Fullname"]),
                html.Td(row["Course"]),
                html.Td(row["Year"]),
                html.Td(row["Integrantes"]),
                # Add more columns as needed
            ]
        )
        table6_rows.append(row_html)

    table6 = dbc.Table(
        [html.Thead(html.Tr([html.Th("Full name"), html.Th("Course"),html.Th("Year"), html.Th("Integrantes")])), html.Tbody(table6_rows)],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
    )


    # Create table 7
    table7_rows = []
    for row in table7_data:
        row_html = html.Tr(
            [
                html.Td(row["fullname"]),
                html.Td(row["TITLE"]),
                html.Td(row["YEAR"]),
                html.Td(row["LANG"]),
                html.Td(row["AUTHOR"]),
                html.Td(row["ORDER"]),
                html.Td(row["ORDER_OK"]),
                
                # Add more columns as needed
            ]
        )
        table7_rows.append(row_html)

    table7 = dbc.Table(
        [html.Thead(html.Tr([html.Th("Name"), html.Th("Title"),html.Th("Year"), html.Th("Language"),html.Th("Author"), html.Th("Order"),html.Th("Order_ok")])), html.Tbody(table7_rows)],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
    )

    # Create table 8
    table8_rows = []
    for row in table8_data:
        row_html = html.Tr(
            [
                html.Td(row["Fullname"]),
                html.Td(row["YEAR"]),
                html.Td(row["NATURE"]),
                html.Td(row["INSTITUTION"]),
                html.Td(row["COURSE"]),
                html.Td(row["STUDENT"]),
                html.Td(row["TYPE"]),
                html.Td(row["SPONSOR"]),
                # Add more columns as needed
            ]
        )
        table8_rows.append(row_html)

    table8 = dbc.Table(
        [html.Thead(html.Tr([html.Th("Full name"), html.Th("Year"),html.Th("Nature"), html.Th("Institution"),html.Th("Course"), html.Th("Student"),html.Th("Type"), html.Th("Sponsor")])), html.Tbody(table8_rows)],
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
    )

    
    headerperson=html.H1("All the Publications", id="publications")
    header3 = html.H1("All the Educations", id="education")
    header4 = html.H1("All the Capitulos De Livros Publicados", id="capitulos")
    header5 = html.H1("All the Projects", id="projects")
    header6 = html.H1("All the Producao tecnica", id="producao")
    header7 = html.H1("All the Trabalhos", id="trabalhos")
    header8 = html.H1("All the Other Productions", id="other")

    
    mydatabase.close()
    return [
        html.Hr(),table1, headerperson,table2,header3,
        table3, html.Hr(),header4, table4, html.Hr(),header5,
        table5, html.Hr(), header6, table6, html.Hr(),
        header7,table7, html.Hr(),header8, table8
    ]

if __name__ == "__main__":
    app.run_server(debug=True, port=8051)



