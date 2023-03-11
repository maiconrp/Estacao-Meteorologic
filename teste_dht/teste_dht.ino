/*
Board: Esp32 Dev Module
ArduinoID v2.0.3
*/

//importando bibliotecas
#include <DHT.h>                   //Biblioteca para o sensor DHT22, v1.2.3
#include <WiFi.h>                  //Biblioteca para conectar o ESP32 com WiFi
#include <IOXhop_FirebaseESP32.h>  //Biblioteca para esp32 se comunicar com firebase
#include <ArduinoJson.h>           //Biblioteca para colocar informação no formato json, utilizado no firebase (versão 5.13.3)

// Credenciais do firebase: Link e Senha
#define FIREBASE_HOST "link"
#define FIREBASE_AUTH "senha"
// senha em https://console.firebase.google.com/u/0/project/NOME-DO-PROJETO/settings/serviceaccounts/databasesecrets?hl=pt>

// Credenciais de wifi: Nome e Senha
#define WIFI_SSID "nome"
#define WIFI_PASSWORD "senha"

// VARIAVEIS 
float temperatura, umidade;

// Objeto correspondente ao sensor
// Parametros: Pino para dados, Tipo do sensor (DHT11, 21 ou 22)
DHT dht(27, DHT22);

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

void pegar_dados(){
  // Inicia comunicação com o sensor DHT22
  dht.begin();
  // Armazena a temperatura lida pelo sensor
  temperatura = dht.readTemperature();
  // Armazena a umidade lida pelo sensor
  umidade = dht.readHumidity();
};

void enviar_dados(){
  // Envia os dados de umidade para o Firebase
  Firebase.setFloat("umidade", umidade);
  // Envia os dados de temperatura para o Firebase
  Firebase.setFloat("temperatura", temperatura);
  // setFloat(variavel, valor)
};

void setup() {
  //inicia comunicação serial
  Serial.begin(115200);   
  set_wifi();
  set_firebase();
};

void loop() {
  pegar_dados(); // Lê os dados do sensor DHT22
  enviar_dados(); // Envia os dados lidos para o Firebase
  Serial.print("Temperatura: "); // Imprime a temperatura no monitor serial
  Serial.print(temperatura);
  Serial.print(",");
  Serial.print("Umidade:" ); // Imprime a umidade no monitor serial
  Serial.println(umidade);
  delay(10000); // Espera 10 segundos antes de ler novamente os dados
 };

