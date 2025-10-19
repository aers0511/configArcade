// === Pines del joystick y botones ===
// Joystick digital (4 direcciones)
#define UP_PIN     17
#define DOWN_PIN   16
#define LEFT_PIN    5
#define RIGHT_PIN   4

// Botones principales
#define BTN_A      14
#define BTN_B      13
#define BTN_X      19
#define BTN_Y      23
#define BTN_L1     21
#define BTN_R1     22
#define BTN_SELECT 18
#define BTN_START  15

const int joystickPins[4] = {UP_PIN, DOWN_PIN, LEFT_PIN, RIGHT_PIN};
const int buttonPins[8]   = {BTN_A, BTN_B, BTN_X, BTN_Y, BTN_L1, BTN_R1, BTN_SELECT, BTN_START};

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < 4; i++) pinMode(joystickPins[i], INPUT_PULLUP);
  for (int i = 0; i < 8; i++) pinMode(buttonPins[i], INPUT_PULLUP);
}

void loop() {
  uint8_t joystickMask = 0;
  uint8_t buttonMask   = 0;

  // Leer joystick
  for (int i = 0; i < 4; i++) {
    if (!digitalRead(joystickPins[i])) joystickMask |= (1 << i);
  }

  // Leer botones
  for (int i = 0; i < 8; i++) {
    if (!digitalRead(buttonPins[i])) buttonMask |= (1 << i);
  }

  // Enviar paquete al PC: [cabecera][joystick][botones]
  Serial.write(0xAA);
  Serial.write(joystickMask);
  Serial.write(buttonMask);

  delay(5);
}
