

const int pin_led_r = 8;
const int pin_led_y = 9;
const int pin_led_g = 10;

void setup() {
  pinMode(pin_led_r, OUTPUT);
  pinMode(pin_led_y, OUTPUT);
  pinMode(pin_led_g, OUTPUT);
}

void loop() {
  digitalWrite(pin_led_r, HIGH);
  digitalWrite(pin_led_y, HIGH);
  digitalWrite(pin_led_g, HIGH);
  delay(1000); // atraso de 1000 ms
  digitalWrite(pin_led_r, LOW);
  digitalWrite(pin_led_y, LOW);
  digitalWrite(pin_led_g, LOW);
  delay(1000); // atraso de 1000 ms
}
