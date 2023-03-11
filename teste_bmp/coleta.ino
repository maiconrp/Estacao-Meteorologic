#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp; //Instância do sensor BMP280

void setup() {
  Serial.begin(115200); //Inicia a comunicação serial com baud rate de 115200
  if (!bmp.begin(0x76)) { //Inicia a comunicação I2C com o endereço do BMP280 (0x76)
    Serial.println("Não foi possível inicializar o BMP280");
    while (1);
  }
}

void loop() {
  float temperature = bmp.readTemperature(); //Lê a temperatura
  float pressure = bmp.readPressure() / 100.0F; //Lê a pressão atmosférica
  float altitude = bmp.readAltitude(SEALEVELPRESSURE_HPA); //Lê a altitude

  Serial.print("Temperatura: ");
  Serial.print(temperature);
  Serial.println(" *C");
  
  Serial.print("Pressão Atmosférica: ");
  Serial.print(pressure);
  Serial.println(" hPa");
  
  Serial.print("Altitude: ");
  Serial.print(altitude);
  Serial.println(" m");
  
  delay(1000); //Aguarda 1 segundo antes de realizar a próxima leitura
}
