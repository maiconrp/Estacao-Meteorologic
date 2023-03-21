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

/* CONSTANTES */

// Credenciais do firebase: Link e Senha
#define FIREBASE_HOST "https://exemplo-nome-default-rtdb.firebaseio.com/"
#define FIREBASE_AUTH "senha"
// senha em https://console.firebase.google.com/u/0/project/NOME-DO-PROJETO/settings/serviceaccounts/databasesecrets?hl=pt>

// Credenciais de wifi: Nome e Senha
#define WIFI_SSID "nome"
#define WIFI_PASSWORD "senha"

// Pinos Sensores 
#define TEMT6000_PIN 34
#define REED_SWITCH_PIN 19

// Pressão Atmosférica local
#define PATM 1013.25

// Calibração Reed Switch
#define VENTO_CALIBRACAO 20
#define INTERRUPCAO_CALIBRACAO 10

const float CALIBRACAO = VENTO_CALIBRACAO/INTERRUPCAO_CALIBRACAO;

/* VARIÁVEIS */

// wifi
int delay_de_tentativas = 500;
int tentativas = 20;

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
volatile int contador_de_interrupcoes = 0; // Variável volátil para contar o número de interrupções
float vento_reed = 0; // Velocidade atual do vento em m/s

/* OBJETOS */

// sensor bmp
Adafruit_BMP280 bmp;  // Inicialização do objeto Adafruit_BMP280 para comunicação com o BMP280 via I2C

// sensor dht
DHT dht(13, DHT22);  // Parametros: Pino para dados, Tipo do sensor (DHT11, 21 ou 22)

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

void handleInterrupt() {
  contador_de_interrupcoes++;
}

void setup() {
  Serial.begin(115200); // Inicia a comunicação serial
  pinMode(REED_SWITCH_PIN, INPUT_PULLUP); // Define o pino como entrada com resistor pull-up
  attachInterrupt(digitalPinToInterrupt(REED_SWITCH_PIN), handleInterrupt, RISING); // Configura a interrupção para ocorrer em uma borda de subida

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
  };

  // Inicia comunicação com o sensor DHT22
  dht.begin();

  conect_wifi();

  // Inicia comunicação com firebase
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  delay(5000);


};

void loop() {
  get_bmp();
  get_dht();
  get_temt();
  get_reed();

  envio_bmp();
  envio_dht();
  envio_temt();
  envio_reed();

  delay(2000);
};

// Coleta
void get_bmp() {
  temperatura_bmp = bmp.readTemperature();  // Leitura da temperatura em graus Celsius
  pressao_bmp = bmp.readPressure() / 100;   // Leitura da pressão atmosférica em hectopascals
  altitude_bmp = bmp.readAltitude(PATM);    // Cálculo da altitude baseado na pressão atmosférica padrão de 1013.25 hPa

  Serial.print("[BMP] Temperatura: ");
  Serial.print(temperatura_bmp);
  Serial.println(" °C");

  Serial.print("[BMP] Pressão Atmosférica: ");
  Serial.print(pressao_bmp);
  Serial.println(" hPa");

  Serial.print("[BMP] Altitude: ");
  Serial.print(altitude_bmp);
  Serial.println(" m");
  Serial.println();
};

void get_dht() {
  // Armazena a temperatura lida pelo sensor
  temperatura_dht = dht.readTemperature();
  // Armazena a umidade lida pelo sensor
  umidade_dht = dht.readHumidity();

  Serial.print("[DHT] Temperatura: ");
  Serial.print(temperatura_dht);
  Serial.println(" °C");

  Serial.print("[DHT] Umidade: ");
  Serial.print(umidade_dht);
  Serial.println(" %");
  Serial.println();
};

void get_temt(){
  leitura = analogRead(TEMT6000_PIN);  //Lê o valor da entrada analógica
  radiacao = leitura * 0.0079;         //Converte o valor lido em W/m²

  Serial.print("[TEMT] Leitura: ");
  Serial.print(leitura);
  Serial.println(" lux");

  Serial.print("[TEMT] Radiação: ");
  Serial.print(radiacao);
  Serial.println(" W/m²");
  Serial.println();
};

void get_reed(){
  detachInterrupt(digitalPinToInterrupt(REED_SWITCH_PIN)); // Desativa a interrupção para ler o contador
  vento_reed = (contador_de_interrupcoes * CALIBRACAO); // Calcula a velocidade do vento em m/s
  contador_de_interrupcoes = 0; // Zera o contador
  attachInterrupt(digitalPinToInterrupt(REED_SWITCH_PIN), handleInterrupt, RISING); // Reativa a interrupção

  Serial.print("[REED] Velocidade do Vento: ");
  Serial.print(vento_reed);
  Serial.println(" m/s");
  Serial.println();
}

// Envio
void envio_bmp() {
  Firebase.set("/Produtor/Cultura/Meteorologia/temperatura/valor_atual_bmp", temperatura_bmp);
  // handle error
  if (Firebase.failed()) {
    Serial.print("[ERROR][bmp] Falha ao enviar temperatura:");
    Serial.println(Firebase.error());
    Serial.println();
    return;
  };

  Firebase.set("/Produtor/Cultura/Meteorologia/pressao/valor_atual_bmp", pressao_bmp);
  // handle error
  if (Firebase.failed()) {
    Serial.print("[ERROR][bmp] Falha ao enviar pressao:");
    Serial.println(Firebase.error());
    Serial.println();
    return;
  };

  Firebase.set("/Produtor/Cultura/Meteorologia/altitude/valor_atual", altitude_bmp);
  // handle error
  if (Firebase.failed()) {
    Serial.print("[ERROR][bmp] Falha ao enviar altitude:");
    Serial.println(Firebase.error());
    Serial.println();

    return;
  };
};

void envio_dht() {
  
  Firebase.set("/Produtor/Cultura/Meteorologia/temperatura/valor_atual_dht", temperatura_dht);
  // handle error
  if (Firebase.failed()) {
    Serial.print("[ERROR][dht] Falha ao enviar temperatura:");
    Serial.println(Firebase.error());
    Serial.println();

    return;
  };

  Firebase.set("/Produtor/Cultura/Meteorologia/umidade/valor_atual", umidade_dht);
  // handle error
  if (Firebase.failed()) {
    Serial.print("[ERROR][bmp] Falha ao enviar umidade:");
    Serial.println(Firebase.error());
    Serial.println();

    return;
  };
};

void envio_temt() {
  // Envia os dados de radiação em MJ para o Firebase;
  Firebase.set("Produtor/Cultura/Meteorologia/radiacao/valor_atual", radiacao);  
  // handle error
  if (Firebase.failed()) {
    Serial.print("[ERROR][temt] Falha ao enviar radiação:");
    Serial.println(Firebase.error());
    Serial.println();

    return;
  };
};

void envio_reed() {
  // Envia os dados de radiação em MJ para o Firebase;
  Firebase.set("Produtor/Cultura/Meteorologia/vento/valor_atual", vento_reed);  
  // handle error
  if (Firebase.failed()) {
    Serial.print("[ERROR][reed] Falha ao enviar velocidade do vento: ");
    Serial.println(Firebase.error());
    Serial.println();

    return;
  };
};
