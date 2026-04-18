# Script Python para comunicarse con Arduino
# pip install pyserial
import serial, json, time

arduino = serial.Serial('COM5', 115200, timeout=1) # Cambiar puerto
time.sleep(2) # Esperar inicialización Arduino

# Clear any existing data in the buffer
arduino.reset_input_buffer()
arduino.reset_output_buffer()

def enviar(cmd):
    # Clear buffers before sending
    arduino.reset_input_buffer()
    arduino.reset_output_buffer()
    
    arduino.write((cmd + '\n').encode())
    time.sleep(0.1)  # Give Arduino time to respond
    
    linea = arduino.readline().decode().strip()
    if not linea:
        return None
    try:
        return json.loads(linea)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Received data: '{linea}'")
        return None
print('Conectado:', enviar('ALL'))
# Ciclo de monitoreo
for _ in range(5):
    resp = enviar('ALL')
    if resp:
        d = resp['data']
        print(f"Temp: {d['temp']}°C Hum: {d['hum']}% Luz: {d['luz']}")
    time.sleep(3)

enviar('LED:ON')
time.sleep(1)
enviar('LED:OFF')