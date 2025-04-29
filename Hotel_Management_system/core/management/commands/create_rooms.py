from django.core.management.base import BaseCommand
from core.models import Room

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        rooms_data = [
            {'number': '101', 'type': 'single', 'price': 100, 'status': 'available'},
            {'number': '102', 'type': 'single', 'price': 100, 'status': 'available'},
            {'number': '201', 'type': 'double', 'price': 150, 'status': 'available'},
            {'number': '202', 'type': 'double', 'price': 150, 'status': 'available'},
            {'number': '301', 'type': 'suite', 'price': 250, 'status': 'available'},
            {'number': '302', 'type': 'suite', 'price': 250, 'status': 'available'},
        ]

        for room_data in rooms_data:
            Room.objects.create(**room_data)
            self.stdout.write(f"Created room {room_data['number']}")
