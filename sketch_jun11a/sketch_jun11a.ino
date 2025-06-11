int led = 2

void setup() {
  // put your setup code here, to run once:

  pinMode(led, OUTPUT);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available()){
    chat situacao = Serial.read();
    if (situacao == "CONHECIDO") {
      digitalWrite(led, HIGH);
      delay(5000);
      digitalWrite(led,LOW);
    }
    if (situacao == "DESCONHECIDO"){
      digitalWrite(led,LOW);
    }
  }
}
