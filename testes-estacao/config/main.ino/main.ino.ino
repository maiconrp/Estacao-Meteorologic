/*
Board: Esp32 Dev Module
ArduinoID v2.0.3
*/

/* BIBLIOTECAS */

// Gerais
#include <WiFi.h>                  //Biblioteca para conectar o ESP32 com WiFi
#include <IOXhop_FirebaseESP32.h>  //Biblioteca para esp32 se comunicar com firebase
#include <ArduinoJson.h>           //Biblioteca para colocar informação no formato json, utilizado no firebase (versão 5.13.3)
#include <Wire.h>

// Sensores
#include <DHT.h>  //Biblioteca para o sensor DHT22, v1.2.3
#include <Adafruit_Sensor.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

/* CONSTANTES */

// Credenciais do firebase: Link e Senha
#define FIREBASE_HOST "https://estacao-meteorologic-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "VoPrhGBDhJiuhvKt1Oo6ucuCNtGI2EZ9ojWHhLN6"
// senha em https://console.firebase.google.com/u/0/project/NOME-DO-PROJETO/settings/serviceaccounts/databasesecrets?hl=pt>

// Credenciais de wifi: Nome e Senha
#define WIFI_SSID "EST"
#define WIFI_PASSWORD "12345678"


// Pressão Atmosférica local


/* VARIÁVEIS */
// dht
float temperatura_dht = 0;
float umidade_dht = 0;
unsigned long lastExecutionTime = 0;

// --- Constantes ---
int period = 5000;               //Tempo de medida(miliseconds)
int delaytime = 2000;            //Invervalo entre as amostras (miliseconds)
unsigned long interval = 60000; // 1 hora em milissegundos


// --- Variáveis Globais ---
unsigned int Sample  = 0;        //Armazena o número de amostras
unsigned int counter = 0;        //Contador para o sensor
unsigned int RPM = 0;            //Rotações por minuto

/* OBJETOS */


// sensor dht
DHT dht(13, DHT22);  // Parametros: Pino para dados, Tipo do sensor (DHT11, 21 ou 22)

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP);

String date;

void conect_wifi() {
  // wifi
  int delay_de_tentativas = 500;
  int tentativas = 40;
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
  Serial.begin(115200);                                                              // Inicia a comunicação serial
  // Inicia comunicação com o sensor DHT22
  dht.begin();
  conect_wifi();

  timeClient.begin();

  timeClient.setTimeOffset(-10800); // UTC-3

  // Inicia comunicação com firebase
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);

  timeClient.begin();
  timeClient.setTimeOffset(0);
  timeClient.update();
}

void timeGet(){
  while(!timeClient.update()) {
    timeClient.forceUpdate();
  }
  // The data comes with the following format:
  // 2018-05-28T16:00:13Z
  // We need to extract date and time
  date = timeClient.getFormattedTime();
  Serial.println(date);

}

void loop() {
  timeClient.update();
  unsigned long currentMillis = millis();

  if (currentMillis - lastExecutionTime >= interval) {
    // Hora em hora - Executar sua função aqui
    coletaEnvio();

    lastExecutionTime = currentMillis;
  }

  // Outras coisas que seu código precise fazer no loop
}


void coletaEnvio() {
  //get_bmp();
  get_dht();
  //get_temt();
  envio_firebase();
}

// Coleta

void print(String sensor, float valor, String medida){
  Serial.print(sensor);
  Serial.print(valor);
  Serial.println(medida);
}

void get_dht() {
  // Armazena a temperatura lida pelo sensor
  temperatura_dht = dht.readTemperature();
  // Armazena a umidade lida pelo sensor
  umidade_dht = dht.readHumidity();

  print("[DHT] Temperatura: ", temperatura_dht, " °C");
  print("[DHT] Umidade: ", umidade_dht, " %");
}


// Envio
void send_to_firebase(String variable_name, float value) {
  String path = "/Produtor/Cultura/Meteorologia/" + variable_name;
  
  Firebase.push(path, value);
  if (Firebase.failed()) {
    Serial.print("[ERROR][");
    Serial.print("] Falha ao enviar valor:");
    Serial.println(Firebase.error());
    Serial.println();
    return;
  }
}

void envio_firebase() {  
  //send_to_firebase("pressao", pressao_bmp);
  send_to_firebase("temperatura", temperatura_dht);
  send_to_firebase("umidade", umidade_dht);
  //send_to_firebase("radiacao", radiacao);
}
