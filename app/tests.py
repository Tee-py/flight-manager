from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Aircraft, Airport, Location
from .serializers import AirCraftSerializer, AirportSerializer, FlightSerializer, LocationSerializer


class UserManagerTests(TestCase):

    def setUp(self):
        self.user = {"email": "test@user.mail", "password": "test"}
        self.admin = {"email": "test@admin.mail", "password": "admintest"}
        return super().setUp()

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(**self.user)
        self.assertEqual(user.email, self.user['email'])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="test")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(**self.admin)
        self.assertEqual(admin_user.email, self.admin['email'])
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass

class SerializerTest(TestCase):

    def setUp(self) -> None:
        self.airport = {
            "name": "Aiport1", 
            "icao": "1Ec9", 
            "location": {
                "area": "Test Area", 
                "city": "Test City", 
                "country": "Test Country", 
                "lat": "7.8968", 
                "lng": "6.7890"
            }
        }
        self.craft = {"serial_number": "AS12HD4I", "manufacturer": "Nuvola"}
        return super().setUp()

    def test_airport_serializer(self) -> None:

        ser1 = AirportSerializer(data=self.airport)
        self.assertEqual(ser1.is_valid(), True)
        inst = ser1.save()
        self.assertEqual(inst.name, self.airport['name'])
        self.assertEqual(inst.icao, self.airport['icao'].upper())
        ser2 = AirportSerializer(data={"name": "hii"})
        self.assertEqual(ser2.is_valid(), False)
    
    def test_aircraft_serializer(self) -> None:
    
        ser = AirCraftSerializer(data=self.craft)
        self.assertEqual(ser.is_valid(), True)
        inst = ser.save()
        self.assertEqual(inst.serial_number, self.craft['serial_number'].upper())
        self.assertEqual(inst.manufacturer, self.craft['manufacturer'])
        ser2 = AirCraftSerializer(data={})
        self.assertEqual(ser2.is_valid(), False)
    
    def test_flight_serializer(self) -> None:
        """
        Test Flight Serializer
        Cases:
        1. Validate Flight Data With All the Complete information.
        2. Validate Flight Data with no Aircraft.
        3. Does Not Validate Create Flight when Arrival date is lesser than Depature Date.
        4. Does Not Validate Flight Data with past departure.
        """

        # creating test aircraft and airports
        craft = Aircraft.objects.create(**{"serial_number": "AS12HD4B", "manufacturer": "Nuvola"})
        loc1 = Location.objects.create(**{
            "area": "Test Area3", 
            "city": "Test City3", 
            "country": "Test Country3", 
            "lat": "7.8964", 
            "lng": "6.7893"
        })
        loc2 = Location.objects.create(**{
            "area": "Test Area2", 
            "city": "Test City2", 
            "country": "Test Country2", 
            "lat": "7.8963", 
            "lng": "6.7892"
        })
        departure = Airport.objects.create(**{
            "name": "Aiport1", 
            "icao": "1EC4", 
            "location": loc1
        })
        arrival = Airport.objects.create(**{
            "name": "Aiport2", 
            "icao": "1EC5", 
            "location": loc2
        })
        
        # Flight Data for Case 1
        flight_data = {
            "aircraft": craft.uid, 
            "arrival": arrival.uid, 
            "departure": departure.uid,
            "departure_dt": timezone.now() + timezone.timedelta(minutes=10),
            "arrival_dt": timezone.now() + timezone.timedelta(minutes=60)
        }

        # Flight Data for Case 2
        flight_data2 = {
            "arrival": arrival.uid, 
            "departure": departure.uid,
            "departure_dt": timezone.now() + timezone.timedelta(minutes=10),
            "arrival_dt": timezone.now() + timezone.timedelta(minutes=60)
        }

        # Flight Data for Case 3
        flight_data3 = {
            "arrival": arrival.uid, 
            "departure": departure.uid,
            "departure_dt": timezone.now() + timezone.timedelta(minutes=60),
            "arrival_dt": timezone.now() 
        }

        # Flight Data for Case 4
        flight_data4 = {
            "arrival": arrival.uid, 
            "departure": departure.uid,
            "departure_dt": timezone.now() - timezone.timedelta(minutes=60),
            "arrival_dt": timezone.now() 
        }

        # Initiating Serializers for Test Cases
        ser = FlightSerializer(data=flight_data)
        ser2 = FlightSerializer(data=flight_data2)
        ser3 = FlightSerializer(data=flight_data3)
        ser4 = FlightSerializer(data=flight_data4)

        # Testing Serializer Validations
        self.assertEqual(ser.is_valid(), True) # Case 1
        self.assertEqual(ser2.is_valid(), True) # Case 2
        self.assertEqual(ser3.is_valid(), False) # Case 3
        self.assertEqual(ser4.is_valid(), False) # Case 4

        ser.save()
        ser2.save()
    
class APITest()