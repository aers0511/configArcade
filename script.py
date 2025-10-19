import serial
import serial.tools.list_ports
import time
import vgamepad as vg

# ==============================
# Función para detectar el ESP32
# ==============================
def detectar_esp32():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB" in port.description or "CH340" in port.description:
            return port.device
    return None

# ==============================
# Inicializar mando virtual
# ==============================
gamepad = vg.VX360Gamepad()

buttons_map = [
    vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
    vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
    vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
    vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
    vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
    vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
    vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,   # SELECT
    vg.XUSB_BUTTON.XUSB_GAMEPAD_START   # START
]

ser = None
BAUD = 115200
print("🔍 Buscando ESP32...")

# ==============================
# Bucle principal
# ==============================
while True:
    try:
        # Si no hay conexión, buscarla
        if ser is None or not ser.is_open:
            port = detectar_esp32()
            if port:
                ser = serial.Serial(port, BAUD, timeout=0.01)
                print(f"✅ ESP32 conectado en {port}")
            else:
                print("❌ ESP32 no detectado, esperando...")
                time.sleep(2)
                continue

        # Leer datos del ESP32
        data = ser.read(3)
        if len(data) == 3 and data[0] == 0xAA:
            joystick_mask = data[1]
            button_mask = data[2]

            # === Joystick 8 direcciones ===
            x, y = 0, 0
            if joystick_mask & (1 << 0): y += 32767   # UP
            if joystick_mask & (1 << 1): y -= 32767   # DOWN
            if joystick_mask & (1 << 2): x -= 32767   # LEFT
            if joystick_mask & (1 << 3): x += 32767   # RIGHT
            gamepad.left_joystick_float(x / 32767, y / 32767)

            # === Botones ===
            for i, button in enumerate(buttons_map):
                if button_mask & (1 << i):
                    gamepad.press_button(button)
                else:
                    gamepad.release_button(button)

            gamepad.update()

        time.sleep(0.001)

    except serial.SerialException:
        print("⚠️ Conexión perdida. Esperando reconexión...")
        if ser:
            try:
                ser.close()
            except:
                pass
            ser = None
        time.sleep(2)
    except KeyboardInterrupt:
        print("\n🛑 Programa detenido por el usuario.")
        break
