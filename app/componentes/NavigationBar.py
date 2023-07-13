from flet import (
    NavigationBar,
    NavigationBarLabelBehavior,
    NavigationDestination,
    Image,
    UserControl,
    border_radius,
    Container,
    Page,
)
import config.routes


class NavigationDestinationTemplate(NavigationDestination):
    def __init__(self, icon, label="Cultura", width=16):
        super().__init__()
        self.label = label
        self.icon_content = Image(src=f"assets/icons/navbar/{icon}.svg", width=width)


class NavigationBarTemplate(NavigationBar):
    """
    Classe para criar uma barra de navegação com configurações comuns

    Atributos:
        ATRIBUTO       TIPO                            DEFINIÇÃO
        destinations   (List[NavigationDestination])   lista de destinos de navegação
    """

    def __init__(
        self,
        destinations=[
            NavigationDestinationTemplate(label="Dashboard", icon="plant"),
            NavigationDestinationTemplate(label="Home", icon="home"),
            NavigationDestinationTemplate(label="Perfil", icon="user"),
        ],
        bgcolor="#FFFFFF",
        height=70,
        page: Page = None,
    ):
        super().__init__()
        self.destinations = destinations
        self.bgcolor = bgcolor
        self.height = height
        self.page = page
        self.on_change = self.change

    def change(self, e):
        self.page.go(e.control.selected_index)


navigation_bar = NavigationBarTemplate()
