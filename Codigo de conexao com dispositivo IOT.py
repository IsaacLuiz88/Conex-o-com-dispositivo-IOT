import asyncio
from bleak import BleakScanner, BleakClient

async def discover_devices():
    print("Procurando dispositivos Bluetooth...")
    nearby_devices = await BleakScanner.discover()
    return nearby_devices

async def list_characteristics(device_address):
    async with BleakClient(device_address) as client:
        print(f"Conectado ao dispositivo: {device_address}")
        services = await client.get_services()
        for service in services:
            print(f"Service UUID: {service.uuid}")
            for char in service.characteristics:
                print(f"  Characteristic UUID: {char.uuid} - Properties: {char.properties}")

async def notification_handler(sender, data):
    print(f"Notificação recebida de {sender}: {data}")
    if data == b'\x01':  # Substitua por qualquer valor que indique "conectado ao Wi-Fi"
        print("Dispositivo conectado ao Wi-Fi com sucesso!")
        return True  # Para indicar que o dispositivo se conectou

async def configure_wifi(device_address, ssid, password):
    try:
        async with BleakClient(device_address) as client:
            print(f"Conectado ao dispositivo: {device_address}")

            ssid_uuid = "00002b11-0000-1000-8000-00805f9b34fb"
            password_uuid = "00002b10-0000-1000-8000-00805f9b34fb"
            status_uuid = "00002b10-0000-1000-8000-00805f9b34fb"  # UUID da característica para notificação

            await client.write_gatt_char(ssid_uuid, ssid.encode())
            print(f"SSID '{ssid}' enviado ao dispositivo.")

            await client.write_gatt_char(password_uuid, password.encode())
            print("Senha enviada ao dispositivo.")

            # Iniciar notificação na característica de status
            await client.start_notify(status_uuid, notification_handler)
            
            try:
                # Espera até 30 segundos por uma notificação de sucesso de conexão
                await asyncio.wait_for(asyncio.sleep(30), timeout=30)
            except asyncio.TimeoutError:
                print("Nenhuma notificação recebida dentro do tempo limite.")
            finally:
                await client.stop_notify(status_uuid)

    except Exception as e:
        print(f"Erro ao enviar credenciais Wi-Fi: {e}")

async def main():
    devices = await discover_devices()
    
    for device in devices:
        print(f"Endereço MAC: {device.address} - Nome: {device.name}")
        if device.name == "TY":
            print(f"Dispositivo 'TY' encontrado! Endereço MAC: {device.address}")
            
            device_address = "05:8F:9E:12:1F:D9"
            ssid = "LAB 2 FILA 1 PC 1"
            password = "laboratorio"
            
            await list_characteristics(device_address)
            await configure_wifi(device.address, ssid, password)
            break
    else:
        print("Dispositivo 'TY' não encontrado.")

if __name__ == "__main__":
    asyncio.run(main())
