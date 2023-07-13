from flet import (
    alignment,
    Card,
    Column,
    Container,
    CrossAxisAlignment,
    FontWeight,
    icons,
    Icon,
    Image,
    MainAxisAlignment,
    Row,
    Text,
    margin,
    padding,
    UserControl,
)
import flet as ft
import assets.colors
from utils.equations import *
from .Cultura import dlg_cultura
from .CadastroCultura import dlg_cadastro, getValues
from database import cultura, estagio, data_plantio, vazao

class cadastrarCultura(UserControl): 
    def build(self):
        def close_dlg(e):
            dlg_cadastro.open = False
            self.page.update()

        def registerClose(e):
            getValues(e)
            dlg_cadastro.open = False
            card_cultura = Cultura()
            self.page.update()
            
        def open_dlg_modal(e):
            self.page.dialog = dlg_cadastro
            dlg_cadastro.open = True
            dlg_cadastro.actions = [
                Container(
                    width = 240,
                    height = 40,
                    bgcolor = '#00D154',
                    alignment=alignment.center,
                    border_radius=6,
                    on_click=registerClose,
                    content = Text('CADASTRAR', color='#1c2439', size=11, weight=FontWeight.W_600),
                )
            ]
            self.page.update()

        return Card(
            content=Container(
                bgcolor="white",
                height=95,
                width=300,
                border_radius=11,
                padding=padding.only(left=20, right=20),
                on_click=open_dlg_modal,
                content=Row(alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls = [
                        Text(
                            "Cadastre sua cultura",
                            color=assets.colors.PRETO,
                            size=19,
                            weight=FontWeight.W_700,
                        ),
                        Container(
                            bgcolor=assets.colors.PRIMARY_GREEN,
                            height=40,
                            width=40,
                            border_radius=30,
                            content = Icon(icons.ADD, size=24, color=assets.colors.BRANCO),
                        ),
                    ]
                )
            ),
            elevation=4,
        )

class Cultura(UserControl): 
    def build(self):
        def close_dlg(e):
            dlg_cultura.open = False
            self.page.update()
            
        def open_dlg_modal(e):
            self.page.dialog = dlg_cultura
            dlg_cultura.open = True
            self.page.update()

        return Card(
            elevation=6,
            content = Container(
                bgcolor="white",
                height=95,
                width=300,
                border_radius=11,
                padding=padding.only(left=20),
                on_click=open_dlg_modal,
                content=Row(
                    controls=[
                        Container(
                            Image(
                                src=f"assets/icons/corn.png",
                                width=300,
                                height=300,
                            ),
                            margin=margin.only(left=-60, right=-180),
                        ),
                        Column(
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Container(
                                    Text(
                                        "Milho",
                                        color="#000000",
                                        size=17,
                                        weight=FontWeight.W_600,
                                    ),
                                    margin=margin.only(bottom=-8),
                                ),
                                Text(
                                    "Plantio: {} \nEstágio: {} \nÁrea: {:.0f}m² \nVazão: {}L/h".format(data_plantio, estagio, Area, vazao),
                                    color="#000000",
                                    size=10,
                                    weight=FontWeight.W_600,
                                ),
                            ],
                        ),
                    ],
                ),
        ))
      
if cultura == 'none':
    card_cultura = cadastrarCultura()
else:
    card_cultura = Cultura()

card_irrigacao = Card(
    content = Container(
        bgcolor="white",
        height=140,
        width=140,
        border_radius=11,
        padding=padding.only(top=14, left=17, right=17, bottom=22),
        content=Column(
            controls=[
                Row(
                    controls=[
                        Container(
                            bgcolor="#EBEBF0",
                            height=24,
                            width=75,
                            border_radius=20,
                            margin=margin.only(right=7),
                            padding=padding.only(left=10),
                            content=ft.Text(
                                "Irrigação",
                                color="#000000",
                                size=12,
                                weight=FontWeight.W_700,
                            ),
                        ),
                        Image(
                            src=f"assets/icons/watch.svg",
                            width=20,
                            height=20,
                        ),
                    ]
                ),
                Container(
                    margin=margin.only(top=-7),
                    content= Text(
                                value=str(Ti)+'min',
                                color="#000000", size=33, weight=FontWeight.W_700
                            ),
                ),
                Container(
                    margin=margin.only(top=-4),
                    content = Text(
                        value="Tempo ideal de irrigação para hoje",
                        color="#000000",
                        size=11,
                        weight=FontWeight.W_400,
                    )
                ),
            ]
        ),
    ),
    elevation=8,
)

card_economia = Card(
    content = Container(
        bgcolor="white",
        height=140,
        width=140,
        border_radius=11,
        padding=padding.only(top=14, left=17, right=17, bottom=22),
        content=Column(
            controls=[
                Row(
                    controls=[
                        Container(
                            bgcolor="#EBEBF0",
                            height=24,
                            width=75,
                            border_radius=20,
                            margin=margin.only(right=7),
                            padding=padding.only(left=10),

                            content=ft.Text(
                                "Economia",
                                color="#000000",
                                size=12,
                                weight=FontWeight.W_700,
                            ),
                        ),
                        Image(
                            src=f"assets/icons/percentage.svg",
                            width=20,
                            height=20,
                        ),
                    ]
                ),
                Container(
                    Text(
                        value="{:.0f}%".format(economia), color="#000000", size=33, weight=FontWeight.W_700
                    ),
                    margin=margin.only(top=-7),
                ),
            ]
        ),
    ),
    elevation=8,
)

card_ET = Card(
    content = Container(
        bgcolor=assets.colors.BRANCO,
        # height=120,
        width=300,
        border_radius=11,
        padding=padding.only(top=14, left=20, right=10, bottom=25),
        content=Column(
            spacing=12,
            controls=[
                Container(
                    bgcolor=assets.colors.WIDGET,
                    height=22,
                    width=500,
                    border_radius=17,
                    alignment=alignment.center,
                    # margin=margin.only(top=-10, bottom=-22, left=-14, right=20),
                    content=Text(
                        "Evapotranspiração",
                        color="#000000",
                        size=12,
                        weight=FontWeight.W_700,
                    ),
                ),
                Row(
                    spacing=50,
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            spacing=1,
                            controls=[
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        Image(
                                            src=f"assets/icons/gotinha.svg",
                                            width=16,
                                            height=16,
                                        ),
                                        Container(
                                            content=Text(
                                                "Referencia",
                                                color="#000000",
                                                size=12,
                                                weight=FontWeight.W_700,
                                            ),
                                            alignment=alignment.center,
                                        ),
                                    ],
                                ),
                                Container(
                                    Column(
                                        [
                                            Text(
                                                value="{:.2f}".format(EToPMF),
                                                font_family="Montserrat",
                                                color="#000000",
                                                size=42,
                                                weight=FontWeight.W_700,
                                            ),
                                            Text(
                                                value="mm/dia",
                                                color="#808080",
                                                size=17,
                                                weight=FontWeight.W_700,
                                            ),
                                        ],
                                    )
                                ),
                            ],
                        ),
                        Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            spacing=1,
                            controls=[
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        Image(
                                            src=f"assets/icons/plantinha.svg",
                                            width=16,
                                            # height=16,
                                        ),
                                        Container(
                                            content=Text(
                                                "Cultura",
                                                color="#000000",
                                                size=12,
                                                weight=FontWeight.W_700,
                                            ),
                                            alignment=alignment.center,
                                        ),
                                    ],
                                ),
                                Container(
                                    Text(
                                        value="{:.2f}".format(Etc),
                                        font_family="Montserrat",
                                        color="#000000",
                                        size=42,
                                        weight=FontWeight.W_700,
                                    ),
                                ),
                                Container(
                                    Text(
                                        value="mm/dia",
                                        color="#808080",
                                        size=17,
                                        weight=FontWeight.W_700,
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ),
    elevation=8,
)
