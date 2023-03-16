// Bibliotecas necessárias para o uso do BMP280
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

// Definição dos pinos usados na comunicação SPI com o BMP280
#define BMP_SCK (13)
#define BMP_MISO (12)
#define BMP_MOSI (11)
#define BMP_CS (10)

Adafruit_BMP280 bmp;  // Inicialização do objeto Adafruit_BMP280 para comunicação com o BMP280 via I2C

void setup() {
  Serial.begin(115200);              // Inicialização da comunicação serial com taxa de transmissão de 115200 baud
  Serial.println(F("BMP280 test"));  // Impressão de mensagem de teste

  // Inicialização da comunicação I2C com o endereço do BMP280 (0x76)
  // e verificação da conexão com o sensor
  if (!bmp.begin(0x76)) {
    Serial.println("Não foi possível inicializar o BMP280");
  };

  /* Configurações padrão do datasheet. */
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Modo de operação */
                  Adafruit_BMP280::SAMPLING_X2,     /* Oversampling da temperatura */
                  Adafruit_BMP280::SAMPLING_X16,    /* Oversampling da pressão */
                  Adafruit_BMP280::FILTER_X16,      /* Filtro */
                  Adafruit_BMP280::STANDBY_MS_500); /* Tempo de espera em standby */
};

void loop() {
  float temperature = bmp.readTemperature();    // Leitura da temperatura em graus Celsius
  float pressure = bmp.readPressure() / 100;    // Leitura da pressão atmosférica em hectopascals
  float altitude = bmp.readAltitude(pressure);  // Cálculo da altitude baseado na pressão atmosférica padrão de 1013.25 hPa

  Serial.print("Temperatura: ");
  Serial.print(bmp.readTemperature());
  Serial.println(" *C");

  Serial.print("Pressão Atmosférica: ");
  Serial.print(pressure);
  Serial.println(" hPa");

  Serial.print("Altitude: ");
  Serial.print(altitude);
  Serial.println(" m");

  delay(2000);  // Espera de 2 segundos antes da próxima leitura
};