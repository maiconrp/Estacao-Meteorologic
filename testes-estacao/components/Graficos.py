import plotly.express as px
import plotly.graph_objects as go
import os
from flet.plotly_chart import PlotlyChart
from flet import* 
from Utils.historicos import *

class GraficoLinhas(UserControl):
    def __init__(
        self,
        dicio_INMET = None,
        dicio_EST = None,
        title_graph = None,
        titley = None,
        medicoes=None,

    ):
        super().__init__()
        self.dicio_INMET = dicio_INMET
        self.dicio_EST = dicio_EST
        self.title_graph = title_graph
        self.titley = titley
        self.medicoes = medicoes

    def build(self):
        fig = go.Figure()

###         CRIANDO O GRÁFICO COM 2 LINHAS, CADA UMA REPRESENTANDO O HISTÓRICO DE UMA ESTAÇÃO      ###

        
        fig.add_trace(go.Scatter(x=[v for v in self.dicio_EST.keys()], 
            y=[v for v in self.dicio_EST.values()],
            name='AgroMet',
            mode='lines+markers',
            marker=dict(
                size=2, 
                color='#00D154',
                line=dict(
                    color='#00D154', 
                    width=1
                ),
            ),
            textfont=dict(size=1),
            ),
        )
     
        fig.update_layout(
            width=360,  
            height=150,
            title=self.title_graph,
            titlefont_size=8,
            margin=dict(t=20, b=20),
            font=dict(
                size=5,  # Defina o tamanho da fonte desejado
            ),
            yaxis=dict(
                title=self.titley,
                titlefont_size=5,
                tickfont_size=4,
                title_standoff=10, 
                #range=[15, 30],
            ),
            xaxis=dict(
                title='Hora (UTC-3)',
                titlefont_size=5,
                tickfont_size=5,
                title_standoff=5, 
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

        return PlotlyChart(fig, expand=False)


    
'''GraficoTemp30 = GraficoLinhas(dicio_EST = dictTempDia30, dicio_INMET = historico_temperatura_INMET_Dia30, 
                                medicoes =  medicoes_temperatura_Dia30, title_graph = 'Temperatura', titley='Valor em °C')

GraficoTemp2 = GraficoLinhas(dicio_EST = dictTempDia2, dicio_INMET = historico_temperatura_INMET_Dia2, 
                                medicoes =  medicoes_temperatura_Dia2, title_graph = 'Temperatura', titley='Valor em °C')

GraficoTemp5 = GraficoLinhas(dicio_EST = dictTempDia5, dicio_INMET = historico_temperatura_INMET_Dia5, 
                                medicoes =  medicoes_temperatura_Dia5, title_graph = 'Temperatura', titley='Valor em °C')'''

GraficoRadiacao1 = GraficoLinhas(dicio_EST = dictRadiacaoDia1,   title_graph = 'RAdiacao', titley='Valor em W/m²')

#GraficoVento30 = GraficoLinhas(dicio_EST = dictVentoDia30, title_graph = 'Vento', titley='Valor em m/s')








