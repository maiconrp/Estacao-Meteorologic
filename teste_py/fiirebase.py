"""
Pra testar:
1. pip install virtualenv
2. virtualenv nome_do_ambiente
3. nome_do_ambiente/Scripts/activate.bat
4. pip install pyrebase

obs: python v3.8.6 ou inferior
Docs:
https://jualabs.files.wordpress.com/2017/11/curso-pyrebase-mc3b3dulo-pyrebase-e-database.pdf
https://github.com/thisbejim/Pyrebase
"""

# pip install pyrebase
import pyrebase

# Credenciais de comunicação
config = {
    "apiKey": "apiKey",
    "authDomain": "projectId.firebaseapp.com",
    "databaseURL": "https://databaseName.firebaseio.com",
    "storageBucket": "projectId.appspot.com"
}

# iniciar app
firebase = pyrebase.initialize_app(config)

# pegar banco de dados
db = firebase.database()

# atualiza o valor de temperatura ou cria se não existir: https://github.com/thisbejim/Pyrebase#set
data = {'temperatura': 10}
db.set(data)

# atualiza o valor de temperatura: https://github.com/thisbejim/Pyrebase#update
data = {'temperatura': 10}
db.update(data)

# pegar o 'ramo' "temperatura" do banco de dados
temperatura = db.child("temperatura").get()

# imprimir o valor: https://github.com/thisbejim/Pyrebase#val
print(temperatura.val())

# Imprime o valor sempre que ele atualiza
def stream_temp(message):
    print("Temperatura: ", message["data"])

def stream_umid(message):
    print("Umidade: ", message["data"])
    
temperatura_stream = db.child("temperatura").stream(stream_temp)
umidade_stream = db.child("umidade").stream(stream_umid)

