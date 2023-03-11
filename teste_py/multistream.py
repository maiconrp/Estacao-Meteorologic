"""
obs: python v3.8.6 ou inferior
# DOCS
https://flet.dev/docs
https://jualabs.files.wordpress.com/2017/11/curso-pyrebase-mc3b3dulo-pyrebase-e-database.pdf
https://github.com/thisbejim/Pyrebase
"""


# pip install flet
import flet as ft # biblioteca pra construção da interface

# pip install pyrebase
import pyrebase # biblioteca pra comunicação com firebase

# Credenciais de comunicação, disponíveis em: 
# https://console.firebase.google.com/u/0/project/estacao-meteorologic/settings/general/web:MTZhYzBhNjMtY2JiNy00ZmM5LTlhYzgtMmEwOWM1MzJkOWZi?hl=pt
config = {
    "apiKey": "apiKey",
    "authDomain": "projectId.firebaseapp.com",
    "databaseURL": "https://databaseName.firebaseio.com",
    "storageBucket": "projectId.appspot.com"
}

# configura comunicação com firebase
firebase = pyrebase.initialize_app(config)

# pegar banco de dados
db = firebase.database()


# <body> corpo da pagina
def main(page: ft.Page):
    # CONFIGURAÇÕES DA PÁGINA
    # título
    page.title = "Estacao Meteorologica"

    # alinhamento
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    #modo de cor
    page.theme_mode = "dark"

    # VARIÁVEIS
    textColor = ft.colors.WHITE
    bgCor = ft.colors.GREEN_900

    # EXIBIÇÃO DE VALORES DO BANCO
    # <input type='text'>
    pressao = ft.TextField(
        label="Pressão",                # Descrição
        value=0,                        # valor (será pego do firebase)
        text_align=ft.TextAlign.CENTER, # alinhamento
        width=175,                      # largura
        suffix_text="hPa"               # texto atras do valor, complemento
    )

    radiacao = ft.TextField(
        label="Radiacao",
        value=0,
        text_align=ft.TextAlign.CENTER,
        width=175,
        suffix_text="W/m²"
    )

    temperatura = ft.TextField(
        label="Temperatura",
        value=0,
        text_align=ft.TextAlign.CENTER,
        width=175,
        suffix_text="°C"
    )

    umidade = ft.TextField(
        label="Umidade",
        value=0,
        text_align=ft.TextAlign.CENTER,
        width=175,
        suffix_text="%"
    )
    vento = ft.TextField(
        label="Vento",
        value=0,
        text_align=ft.TextAlign.CENTER,
        width=175,
        suffix_text="km/h"
    )


    # uma unica função verifica qual variavel foi alterada
    # no firebase e atualiza o valor do componente associado
    def stream(message):
        componentes = {
            "pressao":pressao,
            "radiacao": radiacao,
            "temperatura": temperatura,
            "umidade": umidade,
            "vento": vento,
        }
        componente = componentes.get(message["stream_id"])
        componente.value = message["data"]
        page.update()
        return print(message["stream_id"], message["data"])
    
    
    # caminho base para variáveis
    path = "/Produtor/Cultura/Meteorologia/{}/valor_atual"
    
    # variaveis do firebase, que são monitoradas pela funçãO STREAM, sendo diferenciadas pelo stream_id 
    pressao_stream = db.child(path.format("pressao")).stream(stream, stream_id="pressao")

    radiacao_stream = db.child(path.format("radiacao")).stream(stream, stream_id="radiacao")

    temperatura_stream = db.child(path.format("temperatura")).stream(stream, stream_id="temperatura")

    umidade_stream = db.child(path.format("umidade")).stream(stream, stream_id="umidade")

    vento_stream = db.child(path.format("vento")).stream(stream, stream_id="vento")



    # adiciona, em coluna, os componentes criados la em cima 
    page.add(
        ft.Column(
            [
                pressao,
                radiacao,
                temperatura,
                umidade,
                vento
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

# inicia a página
ft.app(target=main)
