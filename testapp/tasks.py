import threading
import time
from .models import Room, AirConditioner
from decimal import Decimal
from .config import temperature_change_speed,environment_temperature_cool,environment_temperature_heat
def update_temperature_and_fee():
    while True:
        time.sleep(10)
        rooms = Room.objects.all()
        for room in rooms:
            if room.power:
                ac_settings = room.air_conditioner
                # 更新温度
                if ac_settings.mode == 'cool':
                    room.current_temperature -= temperature_change_speed[ac_settings.speed]
                elif ac_settings.mode == 'heat':
                    room.current_temperature += temperature_change_speed[ac_settings.speed]
                

                # 更新费用
                room.ac_usage_time += 1
                room.ac_fee += temperature_change_speed[ac_settings.speed]
                ac_settings.save()
            else:
                #房间回温
                if room.environment_temperature > room.current_temperature:
                    room.current_temperature = min(room.current_temperature + Decimal('0.5'),room.environment_temperature)
                elif room.environment_temperature < room.current_temperature:
                    room.current_temperature = max(room.current_temperature - Decimal('0.5'),room.environment_temperature) 
            room.save()

        # 启动定时任务
def start_scheduler():
    thread = threading.Thread(target=update_temperature_and_fee)
    thread.daemon = True
    thread.start()