'''from flet import (
    Container,
    FontWeight,
    Image,
    MainAxisAlignment,
    Row,
    Text,
    border,
    colors,
    icons,
    padding,
    UserControl,
    alignment,
    BoxShape
)

import assets.colors


class ClimaTemplate(UserControl):
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
        content=None,
        width=300,
        height=47,
        padding=padding.only(left=20, right=20),
        margin=0,
        border_radius=10,
    ):
        def att_valor(self, e):
            self.page.update()
            print("valor atualizado")

        super().__init__()
        self.bgcolor = bgcolor
        self.content = content
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
            border_radius=self.border_radius,
        )


# icons.AIR


def clima_template(titulo: str, valor: str, icone: str, atualizar):
    # Cria os controles filhos para a linha do título
    imagem_titulo = Container(
        Image(src=f"assets/icons/clima/{titulo}.svg", width=18, height=18),
        shape=BoxShape.CIRCLE, 
        bgcolor=assets.colors.PRIMARY_GREEN, 
        padding=5
    )

    texto_titulo = Text(titulo.title(), color="#000000", size=15, weight=FontWeight.W_600)
    controles_titulo = [imagem_titulo, texto_titulo]

    # Cria os controles filhos para a linha do valor
    texto_valor = Text(valor, color="#000000", size=11, weight=FontWeight.W_700)
    container_valor = Container(
        content=texto_valor,
        alignment=alignment.center,
        border_radius=12,
        bgcolor=assets.colors.WIDGET,
        width=70,
        height=22,
    )
    imagem_valor = Image(src=f"assets/icons/{icone}.svg", height=13)
    controles_valor = [container_valor, imagem_valor]

    # Cria a linha principal de conteúdo com as linhas de título e valor
    linha_titulo = Row(controls=controles_titulo)
    linha_valor = Row(controls=controles_valor)
    conteudo = Row(
        controls=[linha_titulo, linha_valor],
        alignment=MainAxisAlignment.SPACE_BETWEEN,
    )

    # Retorna o objeto ClimaTemplate com o conteúdo e a cor de fundo

    return ClimaTemplate(content=conteudo)


temperatura = clima_template("temperatura",  (dict_temp)+' °C', "setaBaixo", atualizar='nao')
vento = clima_template("vento", get_value(dict_vento)+' Km/h', "setaCima")
umidade = clima_template("umidade", get_value(dict_umi)+' %', "setaBaixo")
pressao = clima_template("pressão", get_value(dict_pressao)+' hpa', "setaCima")
radiacao = clima_template("radiação", get_value(dict_rad)+' W/m²', "setaCima")'''