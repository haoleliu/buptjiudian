#config.py
from decimal import Decimal

environment_temperature_cool = {
    '房间一': Decimal('32.0'),
    '房间二': Decimal('28.0'),
    '房间三': Decimal('30.0'),
    '房间四': Decimal('29.0'),
    '房间五': Decimal('35.0')
}

environment_temperature_heat = {
    '房间一': Decimal('10.0'),
    '房间二': Decimal('15.0'),
    '房间三': Decimal('18.0'),
    '房间四': Decimal('12.0'),
    '房间五': Decimal('14.0')
}

temperature_change_speed = {1:0.333,2:0.5,3:1}

default_temperature = {'cool':Decimal('25.0'),'heat':Decimal('22.0')}