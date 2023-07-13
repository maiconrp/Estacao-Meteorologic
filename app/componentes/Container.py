from flet import (
    ButtonStyle,
    CircleBorder,
    Card,
    Column,
    Container,
    ContainerTapEvent,
    CrossAxisAlignment,
    ElevatedButton,
    FontWeight,
    Icon,
    Image,
    MainAxisAlignment,
    Row,
    Text,
    alignment,
    border,
    colors,
    icons,
    IconButton,
    margin,
    padding,
    UserControl,
)

import assets.colors

class TextTemplate(UserControl):
    """
    Classe para criar campos de texto com configurações comuns

    Atributos:
        ATRIBUTO    TIPO        DEFINIÇÃO                               DEFAULT
        label       (str)       Descrição do campo de texto             ("Texto")
        value       (int)       Valor inicial do campo de texto         (0)
        text_align  (TextAlign) Alinhamento do texto dentro do campo    (TextAlign.CENTER)
        width       (int)       Largura do campo de texto               (175)
        suffix_text (str)       Texto que aparece após o valor          ("")
    """

    def __init__(
        self,
        bgcolor=assets.colors.BRANCO,
        value="Milho",
        width=200,
        height=20,
        margin=0,
        color="#000000",
        size=10,
        weight=FontWeight.W_600,
    ):
        super().__init__()
        self.bgcolor = bgcolor
        self.value = value
        self.width = width
        self.height = height
        self.margin = margin
        self.color = color
        self.size = size
        self.weight = weight

    def build(self):
        """
        Cria um objeto TextField com as configurações especificadas no construtor

        Retorna: TextField: campo de texto criado
        """
        return Text(
            bgcolor=self.bgcolor,
            value=self.value,
            width=self.width,
            height=self.height,
            color=self.color,
            size=self.size,
            weight=self.weight,
        )


def click(e: ContainerTapEvent):
    print("clck")



line = Container(width=290, height=1.6, bgcolor="#00D154", alignment=alignment.center)

# Criação de campos de texto com configurações comuns

relatorio = Container(
    margin=margin.only(top=20),
    content=Row(
        controls=[
            Icon(icons.SQUARE, color="#00D154", size=16),
            Text(value="Relatório", color="#000000", size=20, weight=FontWeight.W_600),
        ],
        vertical_alignment=CrossAxisAlignment.CENTER
        # expand=1,
    ),
    width=300,
)

dashboard = Container(
    margin=margin.only(top=20),
    content=Row(
        controls=[
            Icon(icons.SQUARE, color="#00D154", size=16),
            Text(value="Dashboard", color="#000000", size=20, weight=FontWeight.W_600),
        ],
        vertical_alignment=CrossAxisAlignment.CENTER
        # expand=1,
    ),
    width=300,
)

clima = Container(
    margin=margin.only(top=20),
    content=Row(
        controls=[
            Icon(icons.SQUARE, color="#00D154", size=16),
            Text(value="Clima", color="#000000", size=20, weight=FontWeight.W_600),
        ],
        vertical_alignment=CrossAxisAlignment.CENTER
        # expand=1,
    ),
    width=300,
)


