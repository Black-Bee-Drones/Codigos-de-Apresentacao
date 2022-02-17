import asyncio
from mavsdk import System
from mavsdk.offboard import (VelocityBodyYawspeed)

async def run():
    #Verificar se esta porta está disponível
    drone = System(mavsdk_server_address="localhost", port=50040)

    await drone.connect(system_address="udp://:14540")

    #Estabelecendo conexão com os drones
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered!")
            break

    #Arma e decola
    print("-- Arming")
    await drone.action.arm()

    print("-- Takeoff")
    await drone.action.takeoff()

    #Aguarda par apousar
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0)
    )

    #Pousa
    await drone.action.land()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())