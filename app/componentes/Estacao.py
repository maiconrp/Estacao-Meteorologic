import flet as ft
from flet import *

class DialogTemplateEstacao(ft.UserControl):
        def __init__(
            self,
            modal=False,
            content=None,
            content_padding=10,
            actions=None,
            actions_alignment=ft.MainAxisAlignment.END,
            actions_padding=None,
            shape=RoundedRectangleBorder(radius=10),
            on_dismiss=None,
        ):
            

            super().__init__()
            self.modal = modal
            self.content = content
            self.content_padding = content_padding
            self.actions = actions
            self.actions_padding = actions_padding
            self.actions_alignment = actions_alignment
            self.shape = shape
            self.on_dismiss = on_dismiss

        def build(self):

            actions = []
            """for action in self.actions:
                if isinstance(action, str):
                    actions.append(ft.TextButton(action, on_click=close))
                else:
                    actions.append(action)
            self.page.add(
                ft.ElevatedButton("Open modal dialog", on_click=open),
            )"""
            return ft.AlertDialog(
                modal=self.modal,
                content=self.content,
                content_padding=self.content_padding,
                actions=actions,
                actions_padding=self.actions_padding,
                actions_alignment=self.actions_alignment,
                shape=self.shape,
                on_dismiss=self.on_dismiss,
            )

class StatusTemplate(UserControl):
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
        bgcolor='white',
        content=None,
        width=250,
        height=37,
        padding=padding.only(left=15, right=21),
        margin=0,
        border_radius=10,
    ):
        super().__init__()
        self.bgcolor = bgcolor
        self.content= content
        self.width = width
        self.height = height
        self.padding = padding
        self.margin = margin
        self.border_radius = border_radius

    def build(self):
        """
        Cria um objeto TextField com as configurações especificadas no construtor

        Retorna: TextField: campo de texto criado
        """
        return Container(
            bgcolor=self.bgcolor,
            content=self.content,
            width=self.width,
            height=self.height,
            padding=self.padding,
            margin=self.margin,
            border_radius = self.border_radius
        )

def status_template(titulo: str, unidade: str, status: str):
    # Cria os controles filhos para a linha do título
    texto_titulo = Text(titulo.title(), color="#000000", size=13, weight=FontWeight.W_600)

    # Cria os controles filhos para a linha do valor
    texto_unidade = Text(unidade, color="#000000", size=9, weight=FontWeight.W_700)
    container_unidade = Container(
        content=texto_unidade,
        alignment=alignment.center,
        border_radius=12,
        bgcolor='#EBEBF0',
        width=50,
        height=22,
    )

    if status == 'on':
        controles_status = [container_unidade, Icon(ft.icons.CIRCLE, color='#00D154', size=9)]
    elif status == 'off':
        controles_status = [container_unidade, Icon(ft.icons.CIRCLE, color='red', size=9)]

    # Cria a linha principal de conteúdo com as linhas de título e valor

    linha_status = Row(controls=controles_status)
    conteudo = Row(
        controls=[texto_titulo, linha_status],
        alignment=MainAxisAlignment.SPACE_BETWEEN,
    )

    # Retorna o objeto ClimaTemplate com o conteúdo e a cor de fundo
    return StatusTemplate(content=conteudo)


temperatura = status_template("temperatura", "°C", "on")

vento = status_template("vento", "km/h", "on")

umidade = status_template("umidade", "%", "on")

pressao = status_template("pressão", "hpa", "on")

radiacao = status_template("radiação", "W/m²", "off")


dlg_estacao = DialogTemplateEstacao(
    content=Container(
        width=270,
        height=310,
        bgcolor=None,
        content=Column(
            controls = [
                Container(
                    height=37,
                    width=270,
                    
                    content=Row(#vertical_alignment = CrossAxisAlignment.CENTER,
                        controls = [
                            Container(
                                margin=margin.only(right=-95, bottom=-140, top=-40, left=-20),
                                content = Image(
                                        src=f"assets/icons/settings.svg",                                          
                                    )
                            ),
                            Text(
                                "Estação",
                                color="#000000",
                                size=22,
                                weight=FontWeight.W_800,
                            ),

                            
                        ]
                    ) 
                ),
            
                Card(temperatura, elevation=9),
                Card(umidade, elevation=12),
                Card(vento, elevation=12),
                Card(pressao, elevation=12),
                Card(radiacao, elevation=8),
            ]
        )
    )
).build()
