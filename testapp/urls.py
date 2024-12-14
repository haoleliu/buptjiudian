from django.urls import path
from .views import CheckInView, CheckOutView, AirConditionerView,RoomInfoView,CustomerLoginView

urlpatterns = [
    path('check-in/', CheckInView.as_view(), name='check_in'),
    path('check-out/', CheckOutView.as_view(), name='check_out'),
    path('air-conditioner/<str:room_number>/', AirConditionerView.as_view(), name='air_conditioner'),
    path('customer-login/', CustomerLoginView.as_view, name='customer-login'),
    path('room-info/<str:room_number>/', RoomInfoView.as_view(), name='room-info'),
]