import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from flet.plotly_chart import PlotlyChart
from flet import UserControl
import assets.colors
from database import valores_etc, dict_temp, dict_rad, dict_umi, dict_vento

class GraficoLinhas(UserControl):
    def __init__(
        self,
        dicio = None,
        title_graph = None,
        titley = None,
    ):
        super().__init__()
        self.dicio = dicio
        self.title_graph = title_graph
        self.titley = titley

    def build(self):
        green = [assets.colors.PRIMARY_GREEN,]*100
        cinza_claro = [assets.colors.CINZA_AZULADO,]*100
        
        fig = go.Figure()

        try:
            dias = [v.key() for v in self.dicio.each() if type(v) != 'NoneType']
        except:
            dias = [i for i in range(10)]
            
        fig.add_trace(go.Scatter(x=dias, 
            y=[v.val() for v in self.dicio.each()], 
            line=dict(color='#00D154', 
            width=6)))

       
        fig.update_layout(
            title=self.title_graph,
            titlefont_size=28,
            yaxis=dict(
                title=self.titley,
                titlefont_size=22,
                tickfont_size=14,
            ),
            xaxis=dict(
                title='Dia',
                titlefont_size=22,
                tickfont_size=18,
            ),
            legend=dict(
                x=1.0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            barmode='group',
            bargap=0.1, # gap between bars of adjacent location coordinates.
            bargroupgap=0.1 # gap between bars of the same location coordinate.
        )
        return PlotlyChart(fig, expand=True)

grafico_temperatura = GraficoLinhas(dicio = dict_temp, title_graph = 'Temperatura', titley='Valor em °C')
grafico_radiacao = GraficoLinhas(dicio = dict_rad, title_graph = 'Radiação solar', titley='Valor em W/m²')
grafico_vento = GraficoLinhas(dicio = dict_vento, title_graph = 'Velocidade do vento', titley='Valor em m/s')
grafico_umidade = GraficoLinhas(dicio = dict_umi, title_graph = 'Umidade', titley='Valor em %')

