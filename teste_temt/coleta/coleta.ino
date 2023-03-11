#define TEMT6000_PIN 15 //Define o pino a ser usado como entrada do sensor

void setup() {
  Serial.begin(115200); //Inicia a comunicação serial
}

void loop() {
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
}
