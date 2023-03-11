"""
Este código cria uma classe "Counter" que herda de "ft.UserControl". O objetivo é criar um contador de cliques. 
A classe possui dois métodos: "add_click" que aumenta o contador em 1 e atualiza o valor exibido pelo texto e "build" 
que inicializa o contador e cria um objeto de texto e um botão. Dois objetos "contador1" e "contador2" são criados 
a partir da classe "Counter". A função "main" adiciona esses dois objetos na página. 
A função "ft.app" é chamada com o alvo "main" para iniciar a aplicação.
"""
import flet as ft

# Define uma classe Counter que herda de ft.UserControl
class Counter(ft.UserControl):
    # Método add_click é chamado ao clicar no botão "Add"
    def add_click(self, e):
        # Incrementa o contador
        self.counter += 1
        # Atualiza o texto mostrado na tela
        self.text.value = str(self.counter)
        # Aplica as atualizações na tela
        self.update()

    # Método build constrói a interface do usuário
    def build(self):
        # Inicializa o contador com zero
        self.counter = 0
        # Cria um componente Text com o valor inicial do contador
        self.text = ft.Text(str(self.counter))
        # Retorna uma linha com o componente Text e um botão "Add"
        return ft.Row([self.text, ft.ElevatedButton("Add", on_click=self.add_click)])

# Cria duas instâncias da classe Counter
contador1 = Counter()
contador2 = Counter()

# Define a função principal que será executada pelo aplicativo
def main(page):
    # Adiciona as duas instâncias de Counter na página
    page.add(contador1, contador2)

# Inicia o aplicativo passando a função main como alvo
ft.app(target=main)
