# ESP32 Dev Module - Controlar LED com Firebase
Este exemplo mostra como usar o ESP32 Dev Module para controlar um LED através do Firebase.

## Bibliotecas
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
Este exemplo usa o pino 2 do ESP32 como o LED. Isso pode ser alterado de acordo com a necessidade.

## Funcionamento
1. No setup, o ESP32 inicia a comunicação serial com baud rate de 115200.
```c++
void setup() {
  //inicia comunicação serial
  Serial.begin(115200);   
  ...
```
<br>

2. Em seguida, ele se conecta à rede WiFi utilizando as credenciais definidas anteriormente. Enquanto se conecta ao WiFi, ele imprime "Conectando ao wifi" e coloca pontos para indicar que a conexão está sendo estabelecida. Quando a conexão é estabelecida, é impresso "connected: " seguido do endereço IP local do ESP32.
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

3. Em seguida, o ESP32 inicia a comunicação com o Firebase utilizando as credenciais definidas anteriormente. Ele define o pino LED como saída e o liga e desliga para indicar que a conexão com o Firebase foi estabelecida.
```c++
  //inicia comunicação com firebase definido anteriormente
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH); 
  
  // Define o pino definido anteriormente como saída
  pinMode(LED_BUILTIN, OUTPUT); 
  
  // Liga o pino ativando a voltalgem como Alta
  digitalWrite(LED_BUILTIN, HIGH);  
  delay(1000); // espera 1segundo
  digitalWrite(LED_BUILTIN, LOW);  
  // Desliga o pino ativando a voltalgem como Baixa
  ...
```
<br>

4. No loop, o ESP32 verifica o valor da variável "led" no Firebase utilizando a função "Firebase.getInt("/led")" que retorna o valor da variável como um inteiro. Ele imprime esse valor na serial para indicar o estado atual do LED.
```c++
void loop() {
  
  // Pega a variavel 'led' do firebase como inteiro'getInt' e imprime
  Serial.print("led: ");
  Serial.println(Firebase.getInt("/led")); 
  delay(1000);
  ...
 ``` 
<br>

5. A seguir, ele define a variável "firebaseStatus" com o valor da variável "led" no Firebase. Se o valor for 1, o LED é ligado com o comando "digitalWrite(LED_BUILTIN, HIGH);". Se o valor for 0, o LED é desligado com o comando "digitalWrite(LED_BUILTIN, LOW);". Se houver algum erro na conexão, o erro é exibido na serial com "Serial.println(Firebase.error());".

```c++
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
```

## Referências
- [Documentação WiFi.h](https://arduino-esp32.readthedocs.io/en/latest/esp32/api-reference/wifi/WiFi.html)
- [Documentação IOXhop_FirebaseESP32.h](https://github.com/IOXhop/IOXhop_FirebaseESP32)
- [Documentação ArduinoJson.h](https://arduinojson.org/)
- [Firebase Console](https://console.firebase.google.com/)
