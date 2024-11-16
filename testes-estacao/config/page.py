import flet as ft
from flet import UserControl, Theme, Page


class PageConfig:
    """
    Configura as propriedades da página.
    """

    def __init__(self, page: Page):
        self.page = page

        # Define o título da página
        self.page.title = "Estacao Meteorologica"

        # Define a largura e altura da janela
        self.page.window_width = 980.0
        self.page.window_height = 704.0

        # Habilita a barra de rolagem da página
        self.page.scroll = "auto"
        # Define que a janela deve ficar sempre no topo
        self.page.window_always_on_top = True
        # Define a posição horizontal do conteúdo na janela
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Define o modo e o tema da página
        self.page.theme_mode = "light"
    
        # Atualiza a página
        self.page.update()
