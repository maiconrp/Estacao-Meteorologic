/*
Board: Esp32 Dev Module
ArduinoID v2.0.3
*/

//importando bibliotecas
#include <WiFi.h>                          //importa biblioteca para conectar esp32 com wifi
#include <IOXhop_FirebaseESP32.h>          //importa biblioteca para esp32 se comunicar com firebase
#include <ArduinoJson.h>                   //importa biblioteca para colocar informação no formato json, utilizado no firebase (intalar versão 5.13.3)

// Credenciais do firebase: Link e Senha
#define FIREBASE_HOST "link do banco de dados"
#define FIREBASE_AUTH "senha"
// senha em https://console.firebase.google.com/u/0/project/NOME-DO-PROJETO/settings/serviceaccounts/databasesecrets?hl=pt>

// Credenciais de wifi: Nome e Senha
#define WIFI_SSID "nome"
#define WIFI_PASSWORD "senha"

// Definir led interno
#define LED_BUILTIN 2

void setup() {
  //inicia comunicação serial
  Serial.begin(115200);   
  
  //inicia comunicação com wifi com rede definica anteriormente
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);     
  
  //imprime "Conectando ao wifi"
  Serial.print("Conectando ao wifi");    

  //enquanto se conecta ao wifi fica colocando pontos   
  while (WiFi.status() != WL_CONNECTED){    
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());

  //inicia comunicação com firebase definido anteriormente
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH); 
  
  // Define o pino definido anteriormente como saída
  pinMode(LED_BUILTIN, OUTPUT); 
  
  // Liga o pino ativando a voltalgem como Alta
  digitalWrite(LED_BUILTIN, HIGH);  
  delay(1000); // espera 1segundo
  digitalWrite(LED_BUILTIN, LOW);  
  // Desliga o pino ativando a voltalgem como Baixa
}

void loop() {
  
  // Pega a variavel 'led' do firebase como inteiro'getInt' e imprime
  Serial.print("led: ");
  Serial.println(Firebase.getInt("/led")); 
  delay(1000);

  // define a variavel 'firebaseStatus' com o valor da variavel 'led' do firebase
  int firebaseStatus = Firebase.getInt("/led"); 

  // Se o valor da a variavel 'led' do firebase for 1, liga o led
  if (firebaseStatus == 1) {
    Serial.println("Led ligado");
    digitalWrite(LED_BUILTIN, HIGH);  
  } 
  // Se o valor da a variavel 'led' do firebase for 0, desliga o led
  else if (firebaseStatus == 0) {
    Serial.println("Led desligado");
    digitalWrite(LED_BUILTIN, LOW);  
  } 
  // Se não for nenhum dos dois, verifica se falhou a conexão e, caso sim, imprime o erro
  else {
      if (Firebase.failed()) {
        Serial.print("Pegar /led falhou:");
        Serial.println(Firebase.error());
        return;
      }
  }
}
