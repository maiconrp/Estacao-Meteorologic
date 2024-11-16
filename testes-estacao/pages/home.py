import flet as ft
from flet import*
from components.Graficos import GraficoRadiacao1
from components.Container import data, dados_analise


class HomePage:
    def build():
        return ft.View(
            "/",
            [
                Column(
                    controls = [
                        data,
                        GraficoRadiacao1,

                     ]   
                )
            ],
            scroll="auto",
            horizontal_alignment="center",
        )
