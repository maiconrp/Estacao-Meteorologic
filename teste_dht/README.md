# Documentação - ESP32 com Sensor DHT22 e Firebase
Este exemplo mostra como usar o ESP32 com o sensor DHT22 para ler dados de temperatura e umidade e enviá-los para o Firebase.

<br>
<img src="https://user-images.githubusercontent.com/60708311/213896567-85050a7b-e66d-48cd-bf20-c49cee2e76ee.png" width=250 align="left"/>

## DHT22
O DHT22 é um sensor de umidade e temperatura digital que se comunica com o ESP32 através de um único pino de dados. Ele é composto por um termistor (para medir a temperatura) e um capacitor (para medir a umidade). Para utilizar o sensor, é necessário instalar a biblioteca DHT.h e criar um objeto "dht" inicializado com o pino de dados e o tipo de sensor (DHT22).

<br>
<br>

## Bibliotecas
* **DHT.h:** Biblioteca para o sensor DHT22, versão 1.2.3.
* **WiFi.h:** Biblioteca para conectar o ESP32 com WiFi.
* **IOXhop_FirebaseESP32.h:** Biblioteca para comunicação do ESP32 com o Firebase.
* **ArduinoJson.h:** Biblioteca para manipulação de informações no formato JSON, utilizado no Firebase. Versão 5.13.3 é recomendada.

## Credenciais
As credenciais do Firebase e WiFi precisam ser configuradas antes de usar o exemplo.

* **Firebase**: Link e Senha
```c++
#define FIREBASE_HOST "link do banco de dados"
#define FIREBASE_AUTH "senha"
```
Senha em: _https://console.firebase.google.com/u/0/project/NOME-DO-PROJETO/settings/serviceaccounts/databasesecrets?hl=pt_

* **WiFi**: Nome e Senha
```c++
#define WIFI_SSID "nome"
#define WIFI_PASSWORD "senha"
```

## Pinagem
Este exemplo usa o pino 27 do ESP32 para se comunicar com o DHT22.

## Funcionamento
1. No setup, o ESP32 inicia a comunicação serial com baud rate de 115200.
```c++
void setup() {
  //inicia comunicação serial
  Serial.begin(115200);   
  ...
```
<br>

2. Em seguida, é chamada a função **set_wifi()** que se conecta à rede WiFi utilizando as credenciais definidas anteriormente. Enquanto se conecta ao WiFi, é impresso "Conectando ao wifi" e coloca pontos para indicar que a conexão está sendo estabelecida. Quando a conexão é estabelecida, é impresso "connected: " seguido do endereço IP local do ESP32.
```c++
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
  ...
```
<br>

3. Em seguida, é chamada a função set_firebase() que inicia a comunicação com o Firebase utilizando as credenciais definidas anteriormente. 
```c++
void set_firebase(){
  //inicia comunicação com firebase 
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH); 
};

```
<br>

4. Em seguida, é chamada a função pegar_dados() que inicia a comunicação com o sensor DHT22 e armazena os valores de temperatura e umidade lidos pelo sensor.
```c++
void pegar_dados(){
  // Inicia comunicação com o sensor DHT22
  dht.begin();
  // Armazena a temperatura lida pelo sensor
  temperatura = dht.readTemperature();
  // Armazena a umidade lida pelo sensor
  umidade = dht.readHumidity();
};

 ``` 
<br>

5. Em seguida, é chamada a função enviar_dados() que envia os valores armazenados de temperatura e umidade para o Firebase.

```c++
void enviar_dados(){
  // Envia os dados de umidade para o Firebase
  Firebase.setFloat("umidade", umidade);
  // Envia os dados de temperatura para o Firebase
  Firebase.setFloat("temperatura", temperatura);
  // setFloat(variavel, valor)
};

```
<br>

6. Na função loop(), é chamada a função **pegar_dados()**, em seguida, é chamada a função enviar_dados(). A função loop é então pausada por 10 segundos antes de repetir o processo de leitura e envio de dados novamente.

```c++
void loop() {
  pegar_dados(); // Lê os dados do sensor DHT22
  enviar_dados(); // Envia os dados lidos para o Firebase
  Serial.print("Temperatura: "); // Imprime a temperatura no monitor serial
  Serial.print(temperatura);
  Serial.print(",");
  Serial.print("Umidade:" ); // Imprime a umidade no monitor serial
  Serial.println(umidade);
  delay(10000); // Espera 10 segundos antes de ler novamente os dados
 }

```

## Referências
- [Documentação WiFi.h](https://arduino-esp32.readthedocs.io/en/latest/esp32/api-reference/wifi/WiFi.html)
- [Documentação IOXhop_FirebaseESP32.h](https://github.com/IOXhop/IOXhop_FirebaseESP32)
- [Documentação ArduinoJson.h](https://arduinojson.org/)
- [Firebase Console](https://console.firebase.google.com/)
- [DHT sensor library](https://github.com/adafruit/DHT-sensor-library)
