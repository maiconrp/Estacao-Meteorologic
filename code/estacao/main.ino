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
#include <Adafruit_BMP280.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

/* CONSTANTES */

// Credenciais do firebase: Link e Senha
#define FIREBASE_HOST "https://estacao-meteorologic-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH ""
// senha em https://console.firebase.google.com/u/0/project/NOME-DO-PROJETO/settings/serviceaccounts/databasesecrets?hl=pt>

// Credenciais de wifi: Nome e Senha
#define WIFI_SSID "estacao"
#define WIFI_PASSWORD "meteorologica"

// Pinos Sensores
#define TEMT6000_PIN 34
#define REED_SWITCH_PIN 19

// Pressão Atmosférica local
#define PATM 1013.25

/* VARIÁVEIS */

// bmp
float temperatura_bmp = 0;
float pressao_bmp = 0;
float altitude_bmp = 0;

// dht
float temperatura_dht = 0;
float umidade_dht = 0;

// temt
float radiacao;
long leitura;

// reed switch
volatile int contador_de_interrupcoes = 0;  // Variável volátil para contar o número de interrupções
float vento_reed = 0;                       // Velocidade atual do vento em m/s

// --- Constantes ---
const float pi = 3.14159265;     //Número de pi
int period = 5000;               //Tempo de medida(miliseconds)
int delaytime = 2000;            //Invervalo entre as amostras (miliseconds)
int radius = 5.85;                //Raio do anemometro(mm)

// --- Variáveis Globais ---
unsigned int Sample  = 0;        //Armazena o número de amostras
unsigned int counter = 0;        //Contador para o sensor
unsigned int RPM = 0;            //Rotações por minuto

/* OBJETOS */

// sensor bmp
Adafruit_BMP280 bmp;  // Inicialização do objeto Adafruit_BMP280 para comunicação com o BMP280 via I2C

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
  pinMode(REED_SWITCH_PIN, INPUT_PULLUP);                                            // Define o pino como entrada com resistor pull-up
  
  analogReadResolution(10);
  analogSetPinAttenuation(TEMT6000_PIN, ADC_6db);

  // Inicialização da comunicação I2C com o sensor BMP280 (0x76)
  if (!bmp.begin(0x76)) {
    Serial.println("Não foi possível inicializar o BMP280");
  } else {
    /* Configurações padrão do datasheet. */
    bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Modo de operação */
                    Adafruit_BMP280::SAMPLING_X2,     /* Oversampling da temperatura */
                    Adafruit_BMP280::SAMPLING_X16,    /* Oversampling da pressão */
                    Adafruit_BMP280::FILTER_X16,      /* Filtro */
                    Adafruit_BMP280::STANDBY_MS_500); /* Tempo de espera em standby */
  }

  // Inicia comunicação com o sensor DHT22
  dht.begin();
  conect_wifi();

  timeClient.begin();

  timeClient.setTimeOffset(-10800); // UTC-3

  // Inicia comunicação com firebase
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  delay(5000);

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
  timeGet();
  get_bmp();
  get_dht();
  get_temt();
  get_reed();

  envio_firebase();

  delay(2000);
}

// Coleta

void print(String sensor, float valor, String medida){
  Serial.print(sensor);
  Serial.print(valor);
  Serial.println(medida);
}

void get_bmp() {
  temperatura_bmp = bmp.readTemperature();  // Leitura da temperatura em graus Celsius
  pressao_bmp = bmp.readPressure() / 100;   // Leitura da pressão atmosférica em hectopascals
  altitude_bmp = bmp.readAltitude(PATM);    // Cálculo da altitude baseado na pressão atmosférica padrão de 1013.25 hPa

  print("[BMP] Temperatura: ", temperatura_bmp, " °C");
  print("[BMP] Pressão Atmosférica: ", pressao_bmp, " hPA");
  print("[BMP] Altitude: ", altitude_bmp, " m");
}

void get_dht() {
  // Armazena a temperatura lida pelo sensor
  temperatura_dht = dht.readTemperature();
  // Armazena a umidade lida pelo sensor
  umidade_dht = dht.readHumidity();

  print("[DHT] Temperatura: ", temperatura_dht, " °C");
  print("[DHT] Umidade: ", umidade_dht, " %");
}

void get_temt() {
  leitura = analogRead(TEMT6000_PIN);  //Lê o valor da entrada analógica
  radiacao = leitura * 0.0079;         //Converte o valor lido em W/m²

  print("[TEMT] Leitura: ", leitura, " lux");
  print("[TEMT] Radiação: ", radiacao, " W/m²");
}

void get_reed() {
  vento_reed = 0;

  counter = 0;
  attachInterrupt(digitalPinToInterrupt(REED_SWITCH_PIN), addcount, RISING);
  unsigned long millis();
  long startTime = millis();
  while (millis() < startTime + period) {}

  RPM = ((counter) * 60) / (period / 1000); // Calculate revolutions per minute (RPM)
  vento_reed = ((4 * pi * radius * RPM) / 60) / 1000; //Calcula a velocidade do vento em m/s

  print("[REED] Velocidade do Vento: ", vento_reed, " m/s");
}

// Envio
void send_to_firebase(String variable_name, float value) {
  String path = "/Produtor/Cultura/Meteorologia/" + variable_name + "/historico/" + date;
  
  Firebase.set(path, value);
  if (Firebase.failed()) {
    Serial.print("[ERROR][");
    Serial.print("] Falha ao enviar valor:");
    Serial.println(Firebase.error());
    Serial.println();
    return;
  }
}

void envio_firebase() {  
  send_to_firebase("temperatura_bmp", temperatura_bmp);
  send_to_firebase("pressao_bmp", pressao_bmp);
  send_to_firebase("altitude_bmp", altitude_bmp);

  send_to_firebase("temperatura_dht", temperatura_dht);
  send_to_firebase("umidade", umidade_dht);
  
  send_to_firebase("radiacao", radiacao);
  
  send_to_firebase("vento", vento_reed);
}

//Incrementa contador
void addcount() {
  counter++;
}
