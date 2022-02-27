import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, VelocityBodyYawspeed, PositionNedYaw)


async def run():

    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered!")
            break

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: \
              {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print("-- Subir normal a 5 m.")
    await drone.offboard.set_position_ned(
        PositionNedYaw(0, 0.0, -5, 0.0))
    await asyncio.sleep(10)

    print("-- Guenta coração")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(1.5)
    
    print("-- Fazer o infinito parte 1")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(2.0, 0.0, 0.0, 35.0)) #Para aumentar a velocidade dobrar esses valores
    await asyncio.sleep(10)                        #Dimuinuir na mesma proporção o tempo

    print("-- Fazer o infinito parte 2")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(2.0, 0.0, 0.0, -34.0))
    await asyncio.sleep(10)

    print("-- Guenta coração parte 2")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(1.5)

    print("-- Fazer o reinfinito parte 1")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(-2.0, 0.0, 0.0, 34.0))
    await asyncio.sleep(10)

    print("-- Fazer o renfinito parte 2")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(-2.0, 0.0, 0.0, -35.0))
    await asyncio.sleep(10)

    print("-- Guenta coração parte 3")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(1.5)

    print("-- Descer espiralando")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0, 0.0, 2, -46.0))
    await asyncio.sleep(8)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: \
              {error._result.result}")

    await drone.action.land()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())