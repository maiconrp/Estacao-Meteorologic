import flet as ft


class ElevatedButtonTemplate:
    """Classe para criar botões elevados com configurações comuns

    Atributos:
        ATRIBUTO    TIPO        DEFINIÇÃO                       DEFAULT
        autofocus   (bool):     Se o botão tem autofoco         (False)
        bgcolor     (Color):    Cor de fundo do botão           (ft.colors.PRIMARY)
        color       (Color):    Cor do texto do botão           (ft.colors.WHITE)
        content     (Any):      Conteúdo do botão               (None)
        elevation   (int):      Altura do sombreamento do botão (2)
        icon        (str):      Icone do botão                  (None)
        icon_color  (Color):    Cor do icone                    (ft.colors.PRIMARY)
        style       (str):      Estilo css do botão             (None)
        text        (str):      Texto do botão                  ("Button")
        tooltip     (str):      Texto de dica                   (None)
    """

    def __init__(
        self,
        autofocus=False,
        bgcolor="white",
        color=ft.colors.WHITE,
        content=None,
        elevation=2,
        icon=None,
        icon_color=ft.colors.PRIMARY,
        style=None,
        text="Button",
        tooltip=None,
    ):

        self.autofocus = autofocus
        self.bgcolor = bgcolor
        self.color = color
        self.content = content
        self.elevation = elevation
        self.icon = icon
        self.icon_color = icon_color
        self.style = style
        self.text = text
        self.tooltip = tooltip

    def build(self):
        """
        Cria um objeto <ElevatedButton> com as configurações especificadas no construtor

        Retorna: ElevatedButton: botão elevado criado
        """
        return ft.ElevatedButton(
            autofocus=self.autofocus,
            bgcolor=self.bgcolor,
            color=self.color,
            content=self.content,
            elevation=self.elevation,
            icon=self.icon,
            icon_color=self.icon_color,
            style=self.style,
            text=self.text,
            tooltip=self.tooltip,
        )


# Criação de botões elevados com configurações comuns
HomeButton = ElevatedButtonTemplate(text="Estou em home").build()
LoginButton = ElevatedButtonTemplate(
    text="Perfil",
    icon=(ft.Image(src=f"/icons/icon.png")),
).build()

ElevatedButton = ElevatedButtonTemplate(text="Go to Login").build()
ElevatedButton2 = ElevatedButtonTemplate(text="Go to HOME").build()
