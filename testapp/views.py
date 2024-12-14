from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Room, AirConditioner,Customer
from .serializer import RoomSerializer, AirConditionerSerializer
from .config import environment_temperature_cool, environment_temperature_heat,default_temperature
from decimal import Decimal

def get_object_or_none(klass, *args, **kwargs):
    queryset = klass._default_manager.filter(*args, **kwargs)
    try:
        return queryset.get()
    except klass.DoesNotExist:
        return None
    
# Check-in API
class CheckInView(APIView):
    def post(self, request):
        data = request.data
        try:
            room = Room.objects.get(room_number=data['roomNumber'])
            if room.is_occupied:
                return Response({"error": "房间已被占用"}, status=status.HTTP_400_BAD_REQUEST)
            #初始化顾客信息
            Customer.objects.create(id_card=data['idCard'], name=data['name'], phone=data['phone'], room_number=room)
            #初始化房间信息
            room.check_in_date = data['checkInDate']
            room.check_out_date = data['checkOutDate']
            room.total_fee = Decimal(0.00)
            room.is_occupied = True
            room.environment_temperature = environment_temperature_cool[room.room_number]
            room.current_temperature = room.environment_temperature
            room.save()

            air_conditioner = AirConditioner.objects.get(room=room)
            air_conditioner.ac_fee = Decimal(0.00)
            air_conditioner.ac_usage_time = 0
            air_conditioner.save()


            return Response({"message": "入住登记成功！"}, status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response({"error": "房间不存在"}, status=status.HTTP_404_NOT_FOUND)


# Check-out API
class CheckOutView(APIView):
    def post(self, request):
        data = request.data
        try:
            room = Room.objects.get(room_number=data['roomNumber'])
            if not room.is_occupied:
                return Response({"error": "房间当前未被占用"}, status=status.HTTP_400_BAD_REQUEST)

            room_number = request.data.get('roomNumber')
            check_out_date = request.data.get('checkOutDate')
            payment_method = request.data.get('paymentMethod')
            total_amount = request.data.get('totalAmount')

            # Clear room data
            room.check_in_date = None
            room.check_out_date = None
            room.is_occupied = False
            room.power = False
            room.save()

            # Clear air conditioner data if it exists
            air_conditioner = get_object_or_none(AirConditioner, room=room)
            if air_conditioner:
                air_conditioner.delete()

            # Delete related customer data
            customer = get_object_or_404(Customer, room_number=room)
            customer.delete()

            return Response({"message": "退房成功！"}, status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response({"error": "房间不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Customer.DoesNotExist:
            return Response({"error": "顾客对象不存在"}, status=status.HTTP_404_NOT_FOUND)


# Air Conditioner API
class AirConditionerView(APIView):
    def get(self, request, room_number):
        try:
            air_conditioner = AirConditioner.objects.get(room__room_number=room_number)
            room = air_conditioner.room
            air_conditioner_data = AirConditionerSerializer(air_conditioner).data
            room_data = RoomSerializer(room).data
            response_data = {
                "air_conditioner": air_conditioner_data,
                "room": room_data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except AirConditioner.DoesNotExist:
            return Response({"error": "空调设置不存在"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, room_number):
        try:
            room = Room.objects.get(room_number=room_number)
            room.power = request.data.get('power')

            if room.power:
                air_conditioner, created = AirConditioner.objects.get_or_create(room=room)
                serializer = AirConditionerSerializer(air_conditioner, data=request.data, partial=True)

                if serializer.is_valid():
                    # 根据模式(制冷/制热)设置环境温度和目标温度,改变模式时启用
                    new_mode = serializer.validated_data.get('mode')
                    if new_mode == 'cool' and air_conditioner.mode == 'heat':
                        room.environment_temperature = environment_temperature_cool[room_number]
                        air_conditioner.temperature = default_temperature['cool']
                        room.current_temperature = room.environment_temperature
                    elif new_mode == 'heat' and air_conditioner.mode == 'cool':
                        room.environment_temperature = environment_temperature_heat[room_number]
                        air_conditioner.temperature = default_temperature['heat']
                        room.current_temperature = room.environment_temperature

                    air_conditioner.save()
                    room.save()
                    serializer.save()  # 将更新后的数据保存到数据库

                    return Response({"message": "空调设置更新成功！"}, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                air_conditioner = get_object_or_none(AirConditioner, room=room)
                if air_conditioner:
                    air_conditioner.delete()
                return Response({"message": "空调已关闭"}, status=status.HTTP_200_OK)

        except Room.DoesNotExist:
            return Response({"error": "房间不存在"}, status=status.HTTP_404_NOT_FOUND)
        except AirConditioner.DoesNotExist:
            return Response({"error": "空调设置不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RoomInfoView(APIView):
    def get(self, request, room_number):
        try:
            room = Room.objects.get(room_number=room_number)
            serializer = RoomSerializer(room)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response({"error": "房间未找到"}, status=status.HTTP_404_NOT_FOUND)
        
class CustomerLoginView(APIView):
    def post(self, request):
        data = request.data
        try:
            customer = Customer.objects.get(id_card=data['idCard'])
            if customer.room_number.room_number != data['roomNumber']:
                return Response({"error": "房间号与身份证不匹配"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "登录成功！"}, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"error": "顾客不存在"}, status=status.HTTP_404_NOT_FOUND)
        