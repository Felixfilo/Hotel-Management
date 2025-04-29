from django.core.management.base import BaseCommand
from core.models import Room

class Command(BaseCommand):
    help = 'Creates initial rooms and updates room status based on current reservations'

    def add_arguments(self, parser):
        parser.add_argument('--create', action='store_true', help='Create initial 100 rooms')
        parser.add_argument('--update', action='store_true', help='Update room statuses')

    def handle(self, *args, **options):
        if options['create']:
            Room.create_rooms()
            self.stdout.write(self.style.SUCCESS('Successfully created 100 rooms'))
        
        if options['update']:
            occupied, available = Room.update_room_status()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated room statuses. Occupied: {occupied}, Available: {available}'))
        
        if not options['create'] and not options['update']:
            self.stdout.write(self.style.WARNING('Please specify --create or --update'))