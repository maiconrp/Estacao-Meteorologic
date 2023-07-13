import flet as ft
from database import registerCulture
from flet import *

class DialogTemplateCadastro(ft.UserControl):
    def __init__(
        self,
        modal=False,
        content=None,
        content_padding=padding.only(bottom=-10, top=10, left=0, right=0),
        actions=None,
        actions_padding=None,
        actions_alignment="center",
        shape=RoundedRectangleBorder(radius=10),
        on_dismiss=None,
    ):
        def on_close(self, e):
            self.open = False
            self.page.update()
            print("close")

        def on_open(self, e):
            self.page.dialog = dlg_cadastro
            self.open = True
            self.page.update()
            print("open")

        super().__init__()
        self.page = page
        self.modal = modal
        self.content = content
        self.content_padding = content_padding
        self.actions = actions
        self.actions_padding = actions_padding
        self.actions_alignment = actions_alignment
        self.shape = shape
        self.on_dismiss = on_dismiss
        self.on_open = on_open
        self.on_close = on_close

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


data_de_plantio = TextFieldTemplate(
    width = 130,
    label='Data de plantio',
    hint_text='dd/mm/aa'
).build()

area = TextFieldTemplate(
    label='Área de cada setor',
    hint_text='Em ha'
).build()

vazao_gotejador = TextFieldTemplate(
    width=130, label='Vazão do gotejador',
    hint_text='Em litros/h'
).build()

espacamento_linhas = TextFieldTemplate(
    width=130, 
    label='Entre linhas',
    hint_text='Em cm²'
).build()

espacamento_plantas= TextFieldTemplate(
    width=130,
    label='Entre plantas',
    hint_text='Em cm²'
).build()

horas = TextFieldTemplate(
    width=130,
    label=None,
    hint_text='Horas'
).build()

minutos = TextFieldTemplate(
    width=130,
    label=None,
    hint_text='Minutos'
).build()

tipo = Dropdown(
    options=[
        dropdown.Option("Milho"),
        dropdown.Option("Melão"),
        dropdown.Option("Berinjela"),
    ],
    label='Tipo',
    width=130,
    height=40,
    content_padding=padding.only(left=10, right=12),
    text_style = TextStyle(size=11, color='#000000'),
    label_style = TextStyle(size=11, color='#1c2439'),
    border_radius=6,
    filled=True,
    border_color=colors.TRANSPARENT,
    bgcolor='#F1F4FA',
)

textura_solo = Dropdown(
    options=[
        dropdown.Option("Grossa"),
        dropdown.Option("Média"),
        dropdown.Option("Fina"),
    ],
    label='Textura do solo',
    width=130,
    height=40,
    content_padding=padding.only(left=10, right=12),
    text_style = TextStyle(size=11, color='#000000'),
    label_style = TextStyle(size=11, color='#1c2439'),
    border_radius=6,
    filled=True,
    border_color=colors.TRANSPARENT,
    bgcolor='#F1F4FA',
)

title_cadastrar = Text('Cadastro de cultura', color='#000000', size=17, weight=FontWeight.W_700)

text_cadastrar = Text('Preencha os campos abaixo para\ncadastrar sua cultura.', color='#000000', size=13)

text_espacamento = Text('Espaçamento:', color='#000000', weight=FontWeight.W_600, size=11)

text_tempo = Text('Tempo de irrigação atual por setor:', color='#000000', weight=FontWeight.W_600, size=11)

lista_inputs = [data_de_plantio,    vazao_gotejador,    espacamento_linhas,    
                espacamento_plantas,   horas,    minutos,   tipo, textura_solo, area]

info_cultura = {'data_plantio':0,   'esp_linhas': 0,    
                'esp_plantas': 0,   'cultura': 0, 'solo': 0} 

valores_irrigacao = {'vz_gotej': 0, 'tempo_ant': 0, 'Ai': 0}

def getValues(e):
    info_cultura['data_plantio'] = data_de_plantio.value
    info_cultura['esp_linhas'] = int(espacamento_linhas.value)
    info_cultura['esp_plantas'] = int(espacamento_plantas.value)
    info_cultura['cultura'] = tipo.value
    info_cultura['solo'] = textura_solo.value
    valores_irrigacao['Ai'] = area.value
    valores_irrigacao['tempo_ant'] = int(horas.value)*60 + int(minutos.value)
    valores_irrigacao['vz_gotej'] = int(vazao_gotejador.value)

    registerCulture(info_cultura, valores_irrigacao)

    for input in lista_inputs:
        input.value = ''

dlg_cadastro = DialogTemplateCadastro(
    content=Container(
        padding=padding.only(top=8, left=15, right=15, bottom=15),
        width=310,
        height=470,
        bgcolor='white',
        content = Column(alignment=MainAxisAlignment.CENTER,
            horizontal_alignment = CrossAxisAlignment.CENTER,
            controls = [
                Container(
                    alignment = alignment.top_left,
                    content = title_cadastrar,   
                ),
                    Container(
                    alignment = alignment.top_left,
                    margin=margin.only(bottom=10),
                    content = text_cadastrar,   
                ),
                Row(
                    controls = [
                        tipo,
                        data_de_plantio, 
                    ]
                ), 
                Container(
                    margin = margin.only(top=10),
                    alignment = alignment.top_left,
                    content = text_tempo,   
                ),                
                Row(
                    controls = [
                        horas,
                        minutos,
                    ]
                ), 
                    Row(
                    controls = [
                        vazao_gotejador,
                        textura_solo
                    ]
                ),                            
                Container(
                    margin = margin.only(top=10),
                    alignment = alignment.center_left,
                    content = text_espacamento,   
                ),
                Row(
                    controls = [
                        espacamento_linhas,
                        espacamento_plantas,
                    ]
                ),
                area,
            ]
        )
    ),
).build()

