import os
import pandas as pd

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
import plotly.graph_objects as go

import numpy as np



def affiche(recherche, ville, category=None, mode=1):

    # Chargement des données
    csv_file_name = os.path.join("data_search", f"{recherche}-{ville}-search-LBC.csv")
    data = pd.read_csv(csv_file_name)

    data['first_publication_date'] = pd.to_datetime(data['first_publication_date'], format="%Y-%m-%d %H:%M:%S")



    if category in [8,9,10,11,12,13]:
        x_name = "surface_hab"
    elif category in [1,2,3,4,5]:
        x_name = "kilometrage"
    else:
        x_name = "first_publication_date"


    if mode == 1: #option pas trop mal

        fig = px.scatter(data, x=x_name, y='price', color='distance',
                         labels={'surface_hab': 'Surface habitable', 'price': 'Prix', 'first_publication_date':'Date de publication', "kilometrage": 'Kilometrage'},
                         hover_data={'subject': True, 'url': True},
                         trendline="ols", trendline_scope="overall", trendline_color_override="black")
        # Affichage du graphique
        fig.show()



    elif mode ==2 : #fonctionne pas
        plt.figure()
        sc = plt.scatter(data[x_name], data['price'], c=data['distance'])
        plt.xlabel(x_name)
        plt.ylabel('Prix')
        plt.colorbar(sc)
        
        def on_pick(self, event):
            artist = event.artist
            xmouse, ymouse = event.mouseevent.xdata, event.mouseevent.ydata
            x, y = artist.get_xdata(), artist.get_ydata()
            ind = event.ind
            print('Artist picked:', event.artist)
            print('{} vertices picked'.format(len(ind)))
            print('Pick between vertices {} and {}'.format(min(ind), max(ind)+1))
            print('x, y of mouse: {:.2f},{:.2f}'.format(xmouse, ymouse))
            print('Data point:', x[ind[0]], y[ind[0]])
            print()

        plt.gcf().canvas.mpl_connect('pick_event', on_pick)
        plt.show()



    elif mode ==3:
        from plotly.callbacks import Points, InputDeviceState
        points, state = Points(), InputDeviceState()

        fig = go.FigureWidget([go.Scatter(x= data[x_name], y=data['price'], mode='markers')])

        n = len(data)
        scatter = fig.data[0]  
        colors = ['#a3a7e4'] * n
        scatter.marker.color = colors
        scatter.marker.size = [10] * n
        fig.layout.hovermode = 'closest'   
        
        
        
        # create our callback function
        def update_point(trace, points, selector):

            print('caca')
            c = list(scatter.marker.color)
            s = list(scatter.marker.size)
            for i in points.point_inds:
                c[i] = '#bae2be'
                s[i] = 20
                with fig.batch_update():
                    scatter.marker.color = c
                    scatter.marker.size = s

        scatter.on_click(update_point)

        from dash import Dash, dcc, html

        app = Dash()
        app.layout = html.Div([
            dcc.Graph(figure=fig)
        ])

        app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter


    if mode ==4: 
        def on_pick(self, event):
            artist = event.artist
            xmouse, ymouse = event.mouseevent.xdata, event.mouseevent.ydata
            x, y = artist.get_xdata(), artist.get_ydata()
            ind = event.ind
            print('Artist picked:', event.artist)
            print('{} vertices picked'.format(len(ind)))
            print('Pick between vertices {} and {}'.format(min(ind), max(ind)+1))
            print('x, y of mouse: {:.2f},{:.2f}'.format(xmouse, ymouse))
            print('Data point:', x[ind[0]], y[ind[0]])
            print()


        # Génération de fausses données pour la démonstration
        np.random.seed(0)
        superficie = np.random.randint(50, 200, 100)
        prix = 50 + 2.5 * superficie + np.random.normal(0, 20, 100)

        # Calcul de la régression linéaire
        coef = np.polyfit(superficie, prix, 1)
        poly1d_fn = np.poly1d(coef)

        # Tracé de la régression linéaire
        fig = plt.figure(figsize=(6, 4), dpi=100)
        plt.plot(superficie, prix, 'bo', label='Données', picker=5)  # Activer la sélection des points avec un rayon de 5 pixels
        plt.plot(superficie, poly1d_fn(superficie), 'r-', label='Régression linéaire')
        plt.xlabel('Superficie')
        plt.ylabel('Prix')
        plt.title('Régression linéaire : Prix en fonction de la superficie')
        plt.legend()
        plt.grid(True)
        

        # Connexion de la fonction on_pick à l'événement de sélection de point
        fig.canvas.mpl_connect('pick_event', on_pick)
        plt.show()

    if mode ==5: 
        # Import libraries

        import json
        import ipywidgets as widgets

        x=np.random.uniform(-10,10,size=50)
        y=np.sin(x)

        fig=go.FigureWidget([go.Scatter(x=x, y=y, mode='markers'), go.Scatter(x=[], y=[], mode="lines")])

        fig.update_layout(template='simple_white')

        scatter=fig.data[0]
        line = fig.data[1]
        colors=['#a3a7e4']*100
        scatter.marker.color=colors
        scatter.marker.size=[10]*100
        fig.layout.hovermode='closest'

        fig.update_traces(marker=dict(line=dict(color='DarkSlateGrey')))

        out = widgets.Output(layout={'border': '1px solid black'})
        out.append_stdout('Output appended with append_stdout\n')

        # create our callback function
        @out.capture()
        def update_point(trace, points, selector):
            x = list(line.x) + points.xs
            y = list(line.y) + points.ys
            line.update(x=x, y=y)
        scatter.on_click(update_point)

        reset = widgets.Button(description="Reset")
        export = widgets.Button(description="Export")

        @out.capture()
        def on_reset_clicked(b):
            line.update(x=[], y=[])
            out.clear_output()
        @out.capture()
        def on_export_clicked(b):
            print(fig.to_dict()["data"][1])

        reset.on_click(on_reset_clicked)
        export.on_click(on_export_clicked)

        widgets.VBox([widgets.HBox([reset, export]), widgets.VBox([fig, out])])
        # https://stackoverflow.com/questions/70628787/python-interactive-plotting-with-click-events


if __name__ == "__main__":
    # affiche('maison', 'rennes', category= "logement",mode=4)    

    affiche('z650', 'rennes', category= "véhicule",mode=1)    