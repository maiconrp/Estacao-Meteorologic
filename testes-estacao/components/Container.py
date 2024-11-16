from flet import* 
from components.Graficos import GraficoLinhas
from Utils.dados import *
import os
from datetime import datetime

class TextFieldTemplate(UserControl):
    def __init__(
        self,
        border_radius=6,
        filled=True,
        border_color=colors.TRANSPARENT,
        bgcolor="#F1F4FA",
        width=273,
        height=40,
        label="Field",
        label_style=TextStyle(size=12, color='#1c2439', weight=FontWeight.W_400),
        text_style = TextStyle(size=12, color='#1c2439'),
        hint_style=TextStyle(size=12, color='#525a64', weight=FontWeight.W_700),
        hint_text = '',
        on_focus = None,
        keyboard_type=KeyboardType.TEXT,
        content_padding=padding.only(top=8, left=8, right=8),
    ):
        super().__init__()
        self.filled = filled
        self.border_color = border_color
        self.bgcolor = bgcolor
        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.label = label
        self.label_style = label_style
        self.text_style = text_style
        self.hint_style = hint_style
        self.hint_text = hint_text
        self.on_focus = on_focus
        self.keyboard_type = keyboard_type
        self.content_padding = content_padding

    # top_view = self.page.views[-1]

    def build(self):
        """
        Cria um objeto TextField com as configurações especificadas no construtor

        Retorna: TextField: campo de texto criado
        """
        return TextField(
            filled = self.filled,
            border_color = self.border_color,
            bgcolor=self.bgcolor,
            width=self.width,
            height=self.height,
            border_radius=self.border_radius,
            label=self.label,
            label_style = self.label_style,
            text_style = self.text_style,
            hint_style = self.hint_style,
            hint_text = self.hint_text,
            on_focus = self.on_focus,
            keyboard_type=self.keyboard_type,
            content_padding = self.content_padding,
        )

data = path_json[-15:]

# Removendo a extensão .json
data = data.replace(".json", "")

# Substituindo o hífen por barra
data = data.replace("-", "/")

print("Data:", data)

data = Container(
    margin=margin.only(top=20, bottom=20, left=50),
    content=Row(
        controls=[
            Icon(icons.SQUARE, color="#00D154", size=16),
            Text(value="Data - " + str(data), color="#000000", size=20, weight=FontWeight.W_600),
        ],
    ),
)

dados_analise = Container(
    margin=margin.only(top=-20, bottom=20, left=30),
    content=Row(
        alignment=MainAxisAlignment.SPACE_AROUND,
        controls=[
            Container(
              
                content=Row(
                    controls=[
                        Icon(icons.SQUARE, color="#00D154", size=22),
                        Text(value = "Maior variância - " + maior_variancia_umidade, color="#000000", size=14, weight=FontWeight.W_500),
                    ],
                ),
            ),
            Container(
            
                content=Row(
                    controls=[
                        Icon(icons.SQUARE, color="#00D154", size=22),
                        Text(value=" Variância média - " + media_variancia_umidade, color="#000000", size=14, weight=FontWeight.W_500),
                    ],
                ),
            ),
            Container(
   
                content=Row(
                    controls=[
                        Icon(icons.SQUARE, color="#00D154", size=22),
                        Text(value=" Média de assertividade - " + str(assertividade_umidade) + "%", color="#000000", size=14, weight=FontWeight.W_500,),
                    ],
                ),
            ),

        ],
    ),
)

dados_umi = Container(
    margin=margin.only(top=-20, bottom=20, left=50),
    content=Row(
        controls=[
            Icon(icons.SQUARE, color="#00D154", size=16),
            Text(value="Maior variância - " + maior_variancia_umidade
            + "Variância média - " + media_variancia_umidade  
            + "Média de assertividade - " + str(assertividade_umidade), 
            color="#000000", size=14, weight=FontWeight.W_400),
        ],
    ),
)




