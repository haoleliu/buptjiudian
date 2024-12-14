from django.db import models

class Room(models.Model):
    room_number = models.CharField(max_length=50, primary_key=True)
    is_occupied = models.BooleanField(default=False)
    check_in_date = models.DateTimeField(blank=True, null=True)
    check_out_date = models.DateTimeField(blank=True, null=True)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    environment_temperature = models.IntegerField()
    current_temperature = models.DecimalField(max_digits=5, decimal_places=2, default=26.0)
    power = models.BooleanField(default=False)
    ac_usage_time = models.IntegerField(default=0)
    ac_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return self.room_number

class AirConditioner(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE, related_name="air_conditioner")
    temperature = models.DecimalField(max_digits=5, decimal_places=2, default=26.0)
    mode = models.CharField(max_length=10, choices=[('cool', 'Cool'), ('heat', 'Heat')], default='cool')
    speed = models.IntegerField(default=2)
    queue = models.CharField(max_length=10, choices=[('服务中','服务中'),('等待中','等待中')],default='等待中')
    
    def __str__(self):
        return f"{self.room.room_number} - Air Conditioner"

class Customer(models.Model):
    id_card = models.CharField(max_length=18, primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    room_number = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_card
