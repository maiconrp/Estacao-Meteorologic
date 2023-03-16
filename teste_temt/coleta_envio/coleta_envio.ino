/*
Board: Esp32 Dev Module
ArduinoID v2.0.4

Sensor: TEMT6000
Pinout: 
  S - 12
  V - 3V3
  G - GND

*/

//importando bibliotecas
#include <WiFi.h>                  //Biblioteca para conectar o ESP32 com WiFi
#include <IOXhop_FirebaseESP32.h>  //Biblioteca para esp32 se comunicar com firebase

// Credenciais do firebase: Link e Senha
#define FIREBASE_HOST "link"
#define FIREBASE_AUTH "senha"
// senha em https://console.firebase.google.com/u/0/project/NOME-DO-PROJETO/settings/serviceaccounts/databasesecrets?hl=pt>

// Credenciais de wifi: Nome e Senha
#define WIFI_SSID "nome"
#define WIFI_PASSWORD "senha"

#define TEMT6000_PIN 13

// VARIAVEIS
float radiacao;
float leitura;
int i;

int delay_de_tentativas = 500;
int tentativas = 20;


void conect_wifi() {
  /*
    Função para conectar o ESP32 ao WiFi.

    * Esta função utiliza as credenciais de WiFi 
    * definidas nas constantes WIFI_SSID e WIFI_PASSWORD 
    * para conectar o ESP32 à rede WiFi. 
    * A função imprime na saída serial o andamento da conexão.
    * Retorna caso não seja possível se conectar
  */
  Serial.println();
  Serial.print("[WiFi] Conectando à: ");
  Serial.print(WIFI_SSID);

  // Inicia comunicação com wifi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  // Espera pelo evento de WiFi
  while (true) {

    switch (WiFi.status()) {

      case WL_DISCONNECTED:
        Serial.print(".");
        break;

      case WL_NO_SSID_AVAIL:
        Serial.println("[WiFi] SSID não encontrado");
        break;

      case WL_CONNECT_FAILED:
        Serial.print("\n[WiFi] Falha - Não foi possivel conectar! Motivo: ");
        return;
        break;

      case WL_CONNECTION_LOST:
        Serial.println("\n[WiFi] A conexão foi perdida");
        break;

      case WL_SCAN_COMPLETED:
        Serial.println("\n[WiFi] A digitalização está concluída");
        break;

      case WL_CONNECTED:

        Serial.println();
        Serial.println("[WiFi] WiFi conectado!");
        Serial.print("[WiFi] Endereço IP: ");
        Serial.println(WiFi.localIP());
        return;
        break;

      default:
        Serial.print("\n[WiFi] WiFi Status: ");
        Serial.println(WiFi.status());
        break;
    }

    delay(delay_de_tentativas);

    // Verifica se excedeu o tempo máximo de tentativas de conexão
    if (tentativas <= 0) {
      Serial.print("[WiFi] Falha: Tempo de conexão excedeu o limite esperado");
      // Use a função de desconexão para forçar a interrupção da tentativa de conexão
      WiFi.disconnect();
      return;
    } else {
      tentativas--;
    }
  }
}


void setup() {
  /* 
    Função de inicialização do programa.

    * Esta função é executada uma vez ao iniciar o programa. 
    * Ela configura a comunicação serial, conecta o ESP32 ao WiFi 
    * e inicia a comunicação com o Firebase.
  */

  // Inicia comunicação serial
  Serial.begin(9600);
  conect_wifi();

  // Inicia comunicação com firebase
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  delay(5000);
};

void loop() {
  i++;
  leitura = analogRead(TEMT6000_PIN);  //Lê o valor da entrada analógica
  radiacao = leitura * 0.0079;         //Converte o valor lido em W/m²

  Serial.println();
  Serial.print("Leitura: ");
  Serial.print(leitura);
  Serial.println(" lux");

  Serial.print("Irradiance: ");
  Serial.print(radiacao);
  Serial.println(" W/m²");

  // Envia os dados de radiação em MJ para o Firebase;
  Firebase.set("Produtor/Cultura/Meteorologia/radiacao/valor_atual", radiacao);
  Firebase.set("Produtor/Cultura/Meteorologia/radiacao/index", i);

  delay(5000);  //Aguarda 5 segundos antes de realizar a próxima leitura
};
