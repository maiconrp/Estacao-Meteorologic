/*
Board: Esp32 DevKit
ArduinoID v2.0.3
*/

//importando bibliotecas
#include <Arduino.h>
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

#define TEMT6000_PIN 13 //Define o pino a ser usado como entrada do sensor


// Variaveis
int reading;
double volts, radiacao, radiacao_mj;

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

void temt_coleta(){  
  reading = analogRead(TEMT6000_PIN); //Lê o valor da entrada analógica
  volts = reading * 5.0 / 1024.0; //Converte o valor lido em volts
  radiacao = volts / 0.05; //Calcula o fluxo de radiação em W/m²
  radiacao_mj = radiacao * 0.0036; //Converte o fluxo de radiação para MJ m^(-2) d^(-1)
  
  Serial.print("radiacao: ");
  Serial.print(radiacao);
  Serial.println(" W/m²");
  
  Serial.print("radiacao (MJ m^(-2) d^(-1)): ");
  Serial.println(radiacao_mj);
};

void temt_envio(){
  // Envia os dados de radiação em MJ para o Firebase
  Firebase.setFloat("Produtor/Cultura/Meteorologia/radiacao/valor_atual", radiacao_mj);
};

void setup() {
  Serial.begin(115200); //Inicia a comunicação serial
  set_wifi();
  set_firebase();
}

void loop() {
  temt_coleta();
  temt_envio();
  delay(1000); //Aguarda 1 segundo antes de realizar a próxima leitura
};
