/*
Board: Esp32 Dev Module
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


#define TEMT6000_PIN A0 


// VARIAVEIS 


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
  /*
   float lux2 = analogRead(TEMT6000_PIN) * 0.9765625; // 1000 / 1024 = 0.9765625
  Serial.println(lux2);
  */
  int reading = analogRead(TEMT6000_PIN); //Lê o valor da entrada analógica
  double volts = reading * 5.0 / 1024.0; //Converte o valor lido em volts
  double irradiance = volts / 0.05; //Calcula o fluxo de radiação em W/m²
  double irradiance_mj = irradiance * 0.0036; //Converte o fluxo de radiação para MJ m^(-2) d^(-1)
  
  Serial.print("Irradiance: ");
  Serial.print(irradiance);
  Serial.println(" W/m²");
  
  Serial.print("Irradiance (MJ m^(-2) d^(-1)): ");
  Serial.println(irradiance_mj);
  
  delay(1000); //Aguarda 1 segundo antes de realizar a próxima leitura
  
};

void void enviar_dados(){
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
  pinMode(TEMT6000_PIN,  INPUT); 
};

 
void loop() {
  pegar_dados();
  enviar_dados();
  
  delay(1000);
}
