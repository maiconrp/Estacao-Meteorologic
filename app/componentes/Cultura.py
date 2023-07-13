import flet as ft
from flet import *
from database import estagio, data_plantio, cultura, tempo_ant, vazao
from utils.equations import*





class DialogTemplateCultura(ft.UserControl):
    def __init__(
        self,
        modal=False,
        content=None,
        actions=[],
        actions_padding=None,
        actions_alignment="end",
        shape=RoundedRectangleBorder(radius=10),
        on_dismiss=None,
    ):
        def on_close(self, e):
            self.open = False
            self.page.update()
            print("close")

        def on_open(self, e):
            self.page.dialog = dlg_cultura
            self.open = True
            self.page.update()
            print("open")

        super().__init__()
        self.modal = modal
        self.content = content
        self.actions = actions
        self.actions_padding = actions_padding
        self.actions_alignment = actions_alignment
        self.shape = shape
        self.on_dismiss = on_dismiss
        self.on_open = on_open
        self.on_close = on_close

    def build(self):
        return ft.AlertDialog(
            modal=self.modal,
            content=self.content,
            actions=self.actions,
            actions_padding=self.actions_padding,
            actions_alignment=self.actions_alignment,
            shape=self.shape,
            content_padding = 0,
            on_dismiss=self.on_dismiss,
        )

class TextFieldTemplate(UserControl):
    def __init__(
        self,
        border_radius=6,
        filled=True,
        border_color=colors.TRANSPARENT,
        bgcolor='#F1F4FA',
        width=74,
        height=39,
        read_only=True,
        label='Field',
        label_style=TextStyle(size=13, color='#1c2439', weight=FontWeight.W_400),
        value='Info',
        text_style = TextStyle(size=13, color='#1c2439'),
        content_padding = padding.only(left=15, bottom=10),

    ):
        super().__init__()
        self.filled = filled
        self.border_color = border_color
        self.bgcolor = bgcolor
        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.read_only = read_only
        self.label = label
        self.label_style = label_style
        self.value = value
        self.text_style = text_style
        self.content_padding = content_padding
        

#top_view = self.page.views[-1]

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
            read_only=self.read_only,
            label=self.label,
            label_style=self.label_style,
            value=self.value,
            text_style = self.text_style,
            content_padding = self.content_padding,
            
        )

tipo = TextFieldTemplate(width=300, label='Tipo', value=cultura).build()

data = TextFieldTemplate(width=117, label='Data de plantio', value=data_plantio).build()

area = TextFieldTemplate(width=117, label='Área', value="{:.0f} m²".format(Area)).build()

vazao = TextFieldTemplate(width=300, label='Vazão', value=str(vazao)+' L/h').build()

tempo_ant = TextFieldTemplate(label='Anterior', value=str(tempo_ant)+' min').build()

tempo_atu = TextFieldTemplate(label='Atual', value=str(Ti)+' min').build()

economia = TextFieldTemplate(bgcolor='#00D154', label='Economia', label_style=TextStyle(size=13, color='white', weight=FontWeight.W_400), value="{:.0f}%".format(economia)).build()

estagio = TextFieldTemplate(width=110, label='Estágio', value=estagio).build()

duracao = TextFieldTemplate(width=70, label='Duração', value='27 dias').build()

kc = TextFieldTemplate(width=45, label='Kc', value=Kc).build()

dlg_cultura = DialogTemplateCultura(
    content=Container(
        padding=13,
        margin=margin.only(bottom=-25),
        width=270,
        height=410,
        bgcolor='white',
        border_radius=10,
        content = Column(
            controls = [
                Row(vertical_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Container(
                            content=Image(
                                src=f"assets/icons/corn.png",
                                width=170,
                                height=170,
                            ),
                            margin=margin.only(right=-130, bottom=-60, top=-60),
                        ),
                        Text(
                            "Milho",
                            color="#000000",
                            size=22,
                            weight=FontWeight.W_800,
                        )
                    ]
                ),
                tipo,
                Row(spacing=13,
                    controls=[
                            data,
                            area,
                    ]
                ),
                vazao,
                Container(
                    margin=margin.only(top=8),
                    content=Text(
                        'Tempo de irrigação',
                        color="#1C2A50",
                        size=13,
                        weight=FontWeight.W_600,                          
                    )
                ),
                Row(spacing=13,
                    controls = [
                        tempo_ant,
                        tempo_atu,
                        economia,
                    ]
                ),
                Container(
                    margin=margin.only(top=8),
                    content=Text(
                        'Desenvolvimento',
                        color='#1C2A50',
                        size=13,
                        weight=FontWeight.W_600,
                    )
                ),
                Row(spacing=13,
                    controls = [
                        estagio,
                        duracao,
                        kc,
                    ]
                ),
            ]
        ),         
    )         
).build()
