#include <Arduino.h>
#include <WiFi.h>                  //Biblioteca para conectar o ESP32 com WiFi
#include <IOXhop_FirebaseESP32.h>  //Biblioteca para esp32 se comunicar com firebase
#include <ArduinoJson.h>           //Biblioteca para colocar informação no formato json, utilizado no firebase (versão 5.13.3)
#include <DHT.h>                   //Biblioteca para o sensor DHT22, v1.2.3
#include <Wire.h>
#include <Adafruit_Sensor.h>       //Biblioteca para o sensor BMP80
#include <Adafruit_BMP280.h>       //Biblioteca para o sensor BMP280

#define FIREBASE_HOST "link do banco de dados"
#define FIREBASE_AUTH "senha"


#define WIFI_SSID "nome"
#define WIFI_PASSWORD "senha"

// VARIAVEIS 
float temperatura, umidade, pressao;
double volts, radiacao, radiacao_mj;
int reading;

// Objeto correspondente ao sensor
// Parametros: Pino para dados, Tipo do sensor (DHT11, 21 ou 22)
DHT dht(27, DHT22);

#define TEMT6000_PIN 13 //Define o pino a ser usado como entrada do TEMT6000    

Adafruit_BMP280 bmp; //Instância do sensor BMP280

void set_wifi(){
  //inicia comunicação com wifi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);     
  
  //imprime "Conectando ao wifi"
  Serial.print("Conectando ao wifi");    

  //Enquanto se conecta ao WiFi, fica colocando pontos 
  while (WiFi.status() != WL_CONNECTED){    
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());
  // Imprime o IP do WiFi 
};


void set_firebase(){
  //inicia comunicação com firebase 
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH); 
};


////////////////// ---- Funções de coleta de dados ----- ////////////////////

////////////////// ---- DHT 22 ----- ////////////////////
void dht_coleta(){
  // Inicia comunicação com o sensor DHT22
  dht.begin();
  // Armazena a temperatura lida pelo sensor
  temperatura = dht.readTemperature();
  // Armazena a umidade lida pelo sensor
  umidade = dht.readHumidity();
};

void dht_envio(){
  // Envia os dados de umidade para o Firebase
  Firebase.setFloat("Produtor/Cultura/Meteorologia/umidade/valor_atual", umidade);
  // Envia os dados de temperatura para o Firebase
  Firebase.setFloat("Produtor/Cultura/Meteorologia/temperatura/valor_atual", temperatura);
  // setFloat(variavel, valor)
};

////////////////// ---- TEMT6000 ----- ////////////////////
void temt_coleta(){  
  reading = analogRead(TEMT6000_PIN); //Lê o valor da entrada analógica
  volts = reading * 5.0 / 1024.0; //Converte o valor lido em volts
  radiacao = volts / 0.05; //Calcula o fluxo de radiação em W/m²
  //radiacao_mj = radiacao * 0.0036; //Converte o fluxo de radiação para MJ m^(-2) d^(-1)
};

void temt_envio(){
  // Envia os dados de radiação em MJ para o Firebase
  Firebase.setFloat("Produtor/Cultura/Meteorologia/radiacao/valor_atual", radiacao);
};

////////////////// ---- BMP280 ----- ////////////////////
void bmp_coleta(){
  bmp.begin(0x76); //Inicia a comunicação I2C com o endereço do BMP280 (0x76)
  pressao = bmp.readPressure() / 100.0F; //Lê a pressão atmosférica
};

void bmp_envio(){
  // Envia os dados de presão para o Firebase
  Firebase.setFloat("Produtor/Cultura/Meteorologia/pressao/valor_atual", pressao);
};

// Chama todas funções que coletam os dados
void coleta(){
  dht_coleta();
  temt_coleta();
  bmp_coleta();
};

// Chama todas funções que enviam os dados para o Firebase e depois os imprime
void envio(){
  dht_envio();
  Serial.print("Temperatura: "); // Imprime a temperatura no monitor serial
  Serial.print(temperatura);
  Serial.print(",");
  Serial.print("Umidade:" ); // Imprime a umidade no monitor serial
  Serial.println(umidade);
  temt_envio();
  Serial.print("radiacao: ");  // Imprime a radiação no monitor serial
  Serial.print(radiacao);
  Serial.println(" W/m²");
  bmp_envio();
  Serial.print("Pressao: "); // Imprime a temperatura no monitor serial
  Serial.print(pressao);
};

// O ESP32 inicia a comunicação serial com baud rate de 115200 e chama as funções do configuração do wi-fi e firebase
void setup() {
  Serial.begin(115200); //Inicia a comunicação serial
  set_wifi();
  set_firebase();
}

void loop() {
  coleta();
  envio();
  delay(1000); //Aguarda 1 segundo antes de realizar a próxima leitura
};
