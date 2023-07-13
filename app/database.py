import flet as ft
from flet import (
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
import pyrebase


config = {
  'apiKey': "AIzaSyDRgO8OH2ctVG-d6D-bH3qD1cOqeeCXl_k",
  'authDomain': "estacao-meteorologic.firebaseapp.com",
  'databaseURL': "https://estacao-meteorologic-default-rtdb.firebaseio.com",
  'projectId': "estacao-meteorologic",
  'storageBucket': "estacao-meteorologic.appspot.com",
  'messagingSenderId': "483337827811",
  'appId': "1:483337827811:web:80b8b243ae10e899775cd6"
}

FIREBASE = pyrebase.initialize_app(config)

db = FIREBASE.database()

path1 = "/Produtor/Cultura/Meteorologia/{}/valor_atual"
path2 = "/Produtor/Cultura/{}"
path3 = "/Produtor/Cultura/Irrigacao/{}"


def calc_media(dicio, lista):
    length = 0
    soma = 0
    for valor in dicio.each():
       lista.append(valor.val()) 

    for valor in lista:
        soma = soma + valor

    media = soma/len(lista)

    return media
    

values_rad = []
values_temp = []
values_umi = []
values_vento = []
values_etc = []


dict_temp = db.child('/Produtor/Cultura/Meteorologia/temperatura_dht/3').get()
valores_etc = db.child('/Produtor/Cultura/Meteorologia/etc').get()
dict_rad = db.child('/Produtor/Cultura/Meteorologia/radiacao/3').get()
dict_umi = db.child('/Produtor/Cultura/Meteorologia/umidade/3').get()
dict_vento = db.child('/Produtor/Cultura/Meteorologia/vento/5').get()
dict_pressao = db.child('/Produtor/Cultura/Meteorologia/pressao_bmp/3').get()


Etc = calc_media(valores_etc, values_etc) #Saldo de radiação em MJ/m2.dia


Rn = calc_media(dict_rad, values_rad) #Saldo de radiação em MJ/m2.dia

Temp = calc_media(dict_temp, values_temp) # Temperatura em graus Celsius
print(Temp)
ur = calc_media(dict_umi, values_umi)   # Umidade Relativa em porcentagem
print(ur)
vv = calc_media(dict_vento, values_vento)    # Velocidade do vento à 2m de altura em m/s
print(vv)

cultura = db.child('/Produtor/Cultura/cultura').get()
cultura = cultura.val()

data_plantio = db.child('/Produtor/Cultura/data_plantio').get()
data_plantio = data_plantio.val()

estagio = db.child('/Produtor/Cultura/estagio').get()
estagio = estagio.val()

Am = db.child('/Produtor/Cultura/Irrigacao/Am').get()
Am = Am.val()

TR = db.child('/Produtor/Cultura/Irrigacao/TR').get()
TR = TR.val()

Ai = db.child('/Produtor/Cultura/Irrigacao/Ai').get()
Ai = Ai.val()
Ai = float(Ai)


esp_linhas = db.child('/Produtor/Cultura/esp_linhas').get()
esp_linhas = esp_linhas.val()
esp_linhas = float(esp_linhas)

esp_plantas = db.child('/Produtor/Cultura/esp_plantas').get()
esp_plantas = esp_plantas.val()
esp_plantas = float(esp_plantas)


vazao = db.child('/Produtor/Cultura/Irrigacao/vz_gotej').get()
vazao = vazao.val()
vazao = float(vazao)

tempo_ant = db.child('/Produtor/Cultura/Irrigacao/tempo_ant').get()
tempo_ant = tempo_ant.val()

data_plantio = db.child('/Produtor/Cultura/data_plantio').get()
data_plantio = data_plantio.val()


#print(cultura)
#print(Rn)
#print(Temp)
#print(ur)
#print(vv)


def get_value(dicio):
    dic = dicio.val()
    ultimo_valor = list(dic.values())[-1]

    return str(ultimo_valor)


def setIdade(value):
    idd='idade'
    db.child(path2.format(idd)).set(value)


def registerCulture(dict_cultura, dict_irrigacao):
    for info in dict_cultura.keys():
        db.child(path2.format(info)).set(dict_cultura[info])
    for valor in dict_irrigacao:
        db.child(path3.format(valor)).set(dict_irrigacao[valor])
     
class StreamValor(ft.UserControl): 
    def __init__(
        self,
        titulo=None,
        valor=None,
        icone=None,
    ):
        
        super().__init__()
        self.titulo = titulo
        self.valor = valor
        self.icone = icone

    def build(self):
        def atualizar(e):
            self.page.update()
            print("atualizado")
        return Container(
            content = Container(
                bgcolor="white",
                width=300,
                height=47,
                padding=padding.only(left=20, right=20),
                margin=0,
                border_radius=10,
                content=Row(alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Container(
                            Image(src=f"assets/icons/clima/{self.titulo}.svg", width=18, height=18),
                            shape=BoxShape.CIRCLE, 
                            bgcolor=assets.colors.PRIMARY_GREEN, 
                            padding=5
                        ),
                        Text(self.titulo, color="#000000", size=15, weight=FontWeight.W_600),
                        
                        Container(
                            content=Text(self.valor, color="#000000", size=11, weight=FontWeight.W_700),
                            alignment=alignment.center,
                            border_radius=12,
                            bgcolor=assets.colors.WIDGET,
                            width=40,
                            height=22,
                        ),
                        Image(src=f"assets/icons/{self.icone}.svg", height=13),

                    ],
                ),
        ))




temperatura = StreamValor(titulo="temperatura",  valor=get_value(dict_temp)+' °C', icone="setaBaixo")
vento = StreamValor(titulo="vento", valor=get_value(dict_vento)+' Km/h', icone="setaCima")
umidade = StreamValor(titulo="umidade", valor=get_value(dict_umi)+' %', icone="setaBaixo")
pressao = StreamValor(titulo="pressão", valor=get_value(dict_pressao)+' hpa', icone="setaCima")
radiacao = StreamValor(titulo="radiação", valor=get_value(dict_rad)+' W/m²', icone="setaCima")


def stream_handler_temp(message):
    print(message['data'])
    dict_value = message["data"]
    valor = list(dict_value.values())[-1]
    print(valor)
    temperatura.valor = valor
    print(umidade.valor)
    temperatura.build()
    
stream_temp = db.child('/Produtor/Cultura/Meteorologia/temperatura_dht/vila').stream(stream_handler_temp)


def stream_handler_umidade(message):
    print(message['data'])
    dict_value = message["data"]
    valor = list(dict_value.values())[-1]
    print(valor)
    umidade.valor = valor
    print(umidade.valor)
    umidade.build()
    
stream_umidade = db.child('/Produtor/Cultura/Meteorologia/umidade/vila').stream(stream_handler_umidade)


def stream_handler_radiacao(message):
    print(message['data'])
    dict_value = message["data"]
    valor = list(dict_value.values())[-1]
    print(valor)
    radiacao.valor = valor
    print(radiacao.valor)
    radiacao.build()
    
stream_radiacao = db.child('/Produtor/Cultura/Meteorologia/radiacao/vila').stream(stream_handler_radiacao)


def stream_handler_vento(message):
    print(message['data'])
    dict_value = message["data"]
    valor = list(dict_value.values())[-1]
    print(valor)
    vento.valor = valor
    print(vento.valor)
    vento.build()
    
stream_vento = db.child('/Produtor/Cultura/Meteorologia/vento/vila').stream(stream_handler_vento)



def stream_handler_pressao(message):
    print(message['data'])
    dict_value = message["data"]
    valor = list(dict_value.values())[-1]
    print(valor)
    pressao.valor = valor
    print(pressao.valor)
    pressao.build()
    
stream_pressao = db.child('/Produtor/Cultura/Meteorologia/pressao_bmp/vila').stream(stream_handler_pressao)
