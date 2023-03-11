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


    # Altera o valor sempre que ele atualiza no banco
    def stream_pressão(message):
        pressao.value = message["data"] # altera o valor do elemento (pressao.value) e atualiza
        page.update()

    def stream_radiacao(message):
        radiacao.value = message["data"]
        page.update()
    
    def stream_temp(message):
        temperatura.value = message["data"]
        page.update()

    def stream_umidade(message):
        umidade.value = message["data"]
        page.update()

    def stream_vento(message):
        vento.value = message["data"]
        page.update()

    
    # Pega cada valor de info clima e manda pra função monitorar ^
    pressao_stream = db.child("InfoClima").child(
        "Pressão").child("ultimo valor").stream(stream_pressão)
    radiacao_stream = db.child("InfoClima").child(
        "Radiacao").child("ultimo valor").stream(stream_radiacao)
    temperatura_stream = db.child("InfoClima").child(
        "Temperatura").child("ultimo valor").stream(stream_temp)
    umidade_stream = db.child("InfoClima").child(
        "Umidade").child("ultimo valor").stream(stream_umidade)
    vento_stream = db.child("InfoClima").child(
        "Vento").child("ultimo valor").stream(stream_vento)

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
