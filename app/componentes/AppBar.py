import flet as ft
from datetime import datetime
import locale
from flet import (
    alignment,
    AppBar,
    FilledTonalButton,
    FontWeight,
    Icon,
    Row,
    Text,
    UserControl,
    Column,
    Container,
    MainAxisAlignment,
    margin,
    Page,
)
import assets.colors
from .Estacao import dlg_estacao


locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')    
data_de_hoje = datetime.today()

# Obtenha o dia da semana, o dia do mês e o mês em formato de string
dia_da_semana = data_de_hoje.strftime('%A')
dia_do_mes = data_de_hoje.strftime('%d')
mes = data_de_hoje.strftime('%B')

# Formate a string no formato desejado
string_data = f"{dia_da_semana.title()}, {dia_do_mes} de {mes.lower()}"

class Estacao(UserControl):
    def build(self):
        def close_dlg(e):
            dlg_estacao.open = False
            self.page.update()
            
        def open_dlg_modal(e):
            self.page.dialog = dlg_estacao
            dlg_estacao.open = True
            self.page.update()

        return Container(
                width=70,
                height=29,
                margin=ft.margin.only(right=25.0, left=-50),
                on_click=open_dlg_modal,
                content=Container(
                    bgcolor=assets.colors.WIDGET,
                    padding=ft.padding.symmetric(horizontal=10),
                    border_radius=100,
                    content=Row(
                        spacing=3,
                        controls=[
                            Text(
                                value="Estação", color="#000000", size=10, weight=FontWeight.W_600
                            ),
                            Icon("settings", color=assets.colors.PRIMARY_GREEN, size=10),
                        ],
                    ),
                ),
        )
estacao = Estacao()

class AppBarTemplate(AppBar):
    """
    Classe para criar uma barra de aplicativo com configurações comuns

    Atributos:
        ATRIBUTO       TIPO        DEFINIÇÃO                                                             DEFAULT
        title          (Any):      Título da barra de aplicativo                                           (None)
        bgcolor        (Color):    Cor de fundo da barra de aplicativo                                     (colors.PRIMARY)
        actions        (list):     Lista de elementos a serem exibidos à direita da barra de aplicativo     (None)
    """

    def __init__(
        self,
        title=Container(
            content=Row(alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls = [
                    Column(
                        controls=[
                            Text(
                                value="Olá, Victor",
                                color="#000000",
                                size=20,
                                weight=FontWeight.W_700,
                                font_family="Poppins Bold",
                            ),
                            Text(
                                value=string_data,
                                color="#000000",
                                size=10,
                                font_family="Poppins Regular",
                            ),
                        ],
                        spacing=3,
                    ),
                    estacao,
                ]
            ),
            margin=margin.only(left=20, bottom=10),    
        ),
        bgcolor="transparent",
    ):
        """
        Construtor da classe AppBarTemplate. Define os atributos title, bgcolor e actions da AppBar.

        Atributos:
        ATRIBUTO       TIPO        DEFINIÇÃO                                                             DEFAULT
        title          (Any):      Título da barra de aplicativo                                           (None)
        bgcolor        (Color):    Cor de fundo da barra de aplicativo                                     (colors.PRIMARY)
        actions        (list):     Lista de elementos a serem exibidos à direita da barra de aplicativo     (None)

        Returns:
            Nenhum retorno.
        """
        super().__init__()
        self.title = title
        self.bgcolor = bgcolor


appbar = AppBarTemplate()
