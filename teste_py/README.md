# Documentação - Interface com Python e Firebase
Este exemplo mostra como usar Python para construir uma interface de usuário simples para exibir dados de uma estação meteorológica e como usar a biblioteca Pyrebase para se comunicar com o Firebase e atualizar os valores exibidos em tempo real.

## Instalação
Para usar este exemplo, é necessário instalar as seguintes bibliotecas:

* **flet**: Biblioteca para construção da interface, pode ser instalada com o comando `pip install flet`.
* **pyrebase**: Biblioteca para comunicação com o Firebase, pode ser instalada com o comando `pip install pyrebase`.

## Comunicação com Firebase
Antes de usar o exemplo, é necessário configurar as credenciais de comunicação com o Firebase. Essas credenciais podem ser encontradas [aqui](https://console.firebase.google.com/u/0/project/estacao-meteorologic/settings/general/web:MTZhYzBhNjMtY2JiNy00ZmM5LTlhYzgtMmEwOWM1MzJkOWZi?hl=pt)

E devem ser adicionadas no código no trecho:

```python
import pyrebase

config = {
    "apiKey": "apiKey",
    "authDomain": "projectId.firebaseapp.com",
    "databaseURL": "https://databaseName.firebaseio.com",
    "storageBucket": "projectId.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

```
Neste trecho, são importadas as bibliotecas necessárias e as credenciais são configuradas. O objeto "firebase" é usado para inicializar a comunicação com o banco de dados e o objeto "db" é usado para manipular os dados.

<br>

Em seguida, os valores são atualizados a partir do banco de dados, sempre que há uma atualização, usando funções como:

```python
def stream_pressão(message):
    pressao.value = message["data"] # altera o valor do elemento (pressao.value) e atualiza
    page.update()
```

<br>

E essas funções são chamadas e monitoradas através do stream, que é criado com o seguinte trecho de código:

```python
pressao_stream = db.child("InfoClima").child("Pressão").child("ultimo valor").stream(stream_pressão)
radiacao_stream = db.child("InfoClima").child("Radiacao").child("ultimo valor").stream(stream_radiac
```

O stream é uma função do Pyrebase que permite ouvir em tempo real os dados de uma determinada referência no banco de dados Firebase. No código acima, cada variável (pressão, radiação, temperatura, umidade e vento) tem uma função stream associada a ela, que é chamada quando há uma atualização no valor da respectiva referência no banco de dados. Essa função atualiza o valor exibido na interface, garantindo que os dados sempre estejam atualizados.

> Para mais informações sobre o uso do Pyrebase, consulte a documentação em https://github.com/thisbejim/Pyrebase.

<br>

## Estrutura da Interface
A lib [flet](https://flet.dev/) é uma biblioteca para construção de interfaces gráficas para aplicações web. Ela permite criar elementos de interface, como botões, caixas de texto e gráficos, de forma simples e intuitiva.

O código apresentado utiliza a estrutura básica de uma página criada com a lib flet, composta por:

* Uma função principal (main) que define o corpo da página
* Configurações da página, como título, alinhamento e modo de cor
* Variáveis de configuração, como cores de texto e fundo
* Elementos de interface, como caixas de texto para exibir valores do banco

Para criar a interface, é necessário inicialmente criar uma instância da classe **Page** e configurar suas propriedades, como título, alinhamento e modo de cor. Em seguida, os elementos da interface podem ser adicionados à página usando o método `add`. 

Exemplo:

```python
import flet as ft

# criação da página
page = ft.Page()

# configurações da página
page.title = "Estacao Meteorologica"
page.vertical_alignment = ft.MainAxisAlignment.CENTER
page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
page.theme_mode = "dark"

# criação de elementos da interface
pressao = ft.TextField(label="Pressão", value=0)
radiacao = ft.TextField(label="Radiacao", value=0)
temperatura = ft.TextField(label="Temperatura", value=0)
umidade = ft.TextField(label="Umidade", value=0)
vento = ft.TextField(label="Vento", value=0)

# adição de elementos à página
page.add(pressao)
page.add(radiacao)
page.add(temperatura)
page.add(umidade)
page.add(vento)
```

Alguns elementos comuns da biblioteca flet incluem:

* **TextField**: campo de texto para exibir e editar informações. [Documentação](https://flet.dev/docs/controls/textfield)
* **Button**: botão para realizar ações. [Documentação](https://flet.dev/docs/controls/buttons)
* **Card**: componente para exibir conteúdo em formato de cartão. [Documentação](https://flet.dev/docs/controls/card)
* **Image**: componente para exibir imagens. [Documentação](https://flet.dev/docs/controls/image)
* **Row** e **Column**: componentes para organizar elementos em linhas e colunas. [Documentação](https://flet.dev/docs/controls/row) e [Documentação](https://flet.dev/docs/controls/column)

É possível encontrar a documentação completa dos elementos e propriedades da biblioteca flet em https://flet.dev/docs

#### Observação
Este exemplo foi escrito com Python v3.8.6 ou inferior
