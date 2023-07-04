"""
Descrição:  
    Este código é responsável por estabelecer uma conexão com o banco de dados do Firebase e 
    monitorar os dados meteorológicos armazenados nele.
"""
import pyrebase
import datetime

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

def return_atual_day():
    # Obter a data atual
    data_atual = datetime.date.today()

    # Obter o número do dia da semana (segunda-feira = 0, domingo = 6)
    numero_dia_semana = data_atual.weekday()
    days = {
        '0':'1',
        '1':'2',
        '2':'3',
        '3':'4',
        '4':'5',
        '5':'6',
        '6':'0',
    }

    # return days[str(numero_dia_semana)]
    return '0'

path1 = "/Produtor/Cultura/Meteorologia/{}/{}"
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

dict_temp = db.child(path1.format('temperatura_dht', return_atual_day())).get()
print(path1.format('temperatura_dht', return_atual_day()))
valores_etc = db.child('/Produtor/Cultura/Meteorologia/etc').get()
dict_rad = db.child(path1.format('radiacao', return_atual_day())).get()
dict_umi = db.child(path1.format('umidade', return_atual_day())).get()
dict_vento = db.child(path1.format('vento', return_atual_day())).get()
dict_pressao = db.child(path1.format('pressao_bmp', return_atual_day())).get()


Rn = calc_media(dict_rad, values_rad) #Saldo de radiação em MJ/m2.dia
Temp = calc_media(dict_temp, values_temp) # Temperatura em graus Celsius
ur = calc_media(dict_umi, values_umi)   # Umidade Relativa em porcentagem
vv = calc_media(dict_vento, values_vento)    # Velocidade do vento à 2m de altura em m/s

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

esp_linhas = db.child('/Produtor/Cultura/esp_linhas').get()
esp_linhas = esp_linhas.val()

esp_plantas = db.child('/Produtor/Cultura/esp_plantas').get()
esp_plantas = esp_plantas.val()

vazao = db.child('/Produtor/Cultura/Irrigacao/vz_gotej').get()
vazao = vazao.val()

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
    print(ultimo_valor)


def setIdade(value):
    idd='idade'
    db.child(path2.format(idd)).set(value)


def registerCulture(dict_cultura, dict_irrigacao):
    for info in dict_cultura.keys():
        db.child(path2.format(info)).set(dict_cultura[info])
    for valor in dict_irrigacao:
        db.child(path3.format(valor)).set(dict_irrigacao[valor])
     



    

    
