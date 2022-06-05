from django.test import TestCase, RequestFactory
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Aircraft, Airport, Flight, Location, User
from .utils import datetime, format_datetime_str
from .serializers import AirCraftSerializer, AirportSerializer, CreateFlightSerializer


def create_user(data: dict, role: str = "user"):
    user = User(**data, role=role)
    user.set_password(data["password"])
    user.save()
    return user


class UtilsTest(TestCase):
    def test_date_formatter(self):
        val1 = "2022-06-05 17:22"
        val2 = "20-60-05 17:22"
        val3 = "hello"
        res = format_datetime_str(val1)
        self.assertEqual(res, datetime(2022, 6, 5, 17, 22))
        with self.assertRaises(ValueError):
            format_datetime_str(val2)
        with self.assertRaises(ValueError):
            format_datetime_str(val3)


class UserManagerTests(TestCase):
    def setUp(self):
        self.user = {"email": "test@user.mail", "password": "test"}
        self.admin = {"email": "test@admin.mail", "password": "admintest"}
        return super().setUp()

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(**self.user)
        self.assertEqual(user.email, self.user["email"])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="test")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(**self.admin)
        self.assertEqual(admin_user.email, self.admin["email"])
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
                "lng": "6.7890",
            },
        }
        self.factory = RequestFactory()
        self.craft = {"serial_number": "AS12HD4I", "manufacturer": "Nuvola"}
        return super().setUp()

    def test_airport_serializer(self) -> None:
        post_rf = self.factory.post("")
        ser1 = AirportSerializer(data=self.airport, context={"request": post_rf})
        self.assertEqual(ser1.is_valid(), True)
        inst = ser1.save()
        self.assertEqual(inst.name, self.airport["name"])
        self.assertEqual(inst.icao, self.airport["icao"].upper())
        ser2 = AirportSerializer(data={"name": "hii"}, context={"request": post_rf})
        self.assertEqual(ser2.is_valid(), False)

    def test_aircraft_serializer(self) -> None:
        post_rf = self.factory.post("")
        ser = AirCraftSerializer(data=self.craft, context={"request": post_rf})
        self.assertEqual(ser.is_valid(), True)
        inst = ser.save()
        self.assertEqual(inst.serial_number, self.craft["serial_number"].upper())
        self.assertEqual(inst.manufacturer, self.craft["manufacturer"])
        ser2 = AirCraftSerializer(data={}, context={"request": post_rf})
        self.assertEqual(ser2.is_valid(), False)

    def test_create_flight_serializer(self) -> None:
        # creating test aircraft and airports
        craft = Aircraft.objects.create(
            **{"serial_number": "AS12HD4B", "manufacturer": "Nuvola"}
        )
        loc1 = Location.objects.create(
            **{
                "area": "Test Area3",
                "city": "Test City3",
                "country": "Test Country3",
                "lat": "7.8964",
                "lng": "6.7893",
            }
        )
        loc2 = Location.objects.create(
            **{
                "area": "Test Area2",
                "city": "Test City2",
                "country": "Test Country2",
                "lat": "7.8963",
                "lng": "6.7892",
            }
        )
        departure = Airport.objects.create(
            **{"name": "Aiport1", "icao": "1EC4", "location": loc1}
        )
        arrival = Airport.objects.create(
            **{"name": "Aiport2", "icao": "1EC5", "location": loc2}
        )

        # Flight Data for Case 1(complete data)
        flight_data = {
            "aircraft": craft.serial_number,
            "arrival": arrival.icao,
            "departure": departure.icao,
            "departure_dt": timezone.now() + timezone.timedelta(minutes=10),
            "arrival_dt": timezone.now() + timezone.timedelta(minutes=60),
        }

        # Flight Data for Case 2(no airport)
        flight_data2 = {
            "arrival": arrival.icao,
            "departure": departure.icao,
            "departure_dt": timezone.now() + timezone.timedelta(minutes=10),
            "arrival_dt": timezone.now() + timezone.timedelta(minutes=60),
        }

        # Flight Data for Case 3(arrival is before departure)
        flight_data3 = {
            "arrival": arrival.icao,
            "departure": departure.icao,
            "departure_dt": timezone.now() + timezone.timedelta(minutes=60),
            "arrival_dt": timezone.now(),
        }

        # Flight Data for Case 4(departure is in the past)
        flight_data4 = {
            "arrival": arrival.icao,
            "departure": departure.icao,
            "departure_dt": timezone.now() - timezone.timedelta(minutes=60),
            "arrival_dt": timezone.now(),
        }

        # Initiating Serializers for Test Cases
        ser = CreateFlightSerializer(data=flight_data)
        ser2 = CreateFlightSerializer(data=flight_data2)
        ser3 = CreateFlightSerializer(data=flight_data3)
        ser4 = CreateFlightSerializer(data=flight_data4)

        # Testing Serializer Validations
        self.assertEqual(ser.is_valid(), True)  # Case 1
        self.assertEqual(ser2.is_valid(), True)  # Case 2
        self.assertEqual(ser3.is_valid(), False)  # Case 3
        self.assertEqual(ser4.is_valid(), False)  # Case 4

        ser.save()
        ser2.save()


class APITest(APITestCase):
    def setUp(self) -> None:
        self.user_login = {"email": "user@nuvolar.com", "password": "user"}
        self.admin_login = {"email": "admin@nuvolar.com", "password": "admin"}
        self.aircraft_data = {"serial_number": "JtFRIOPL", "manufacturer": "nuvolar"}
        self.airport_data = {
            "name": "Aiport1",
            "icao": "1Ec5",
            "location": {
                "area": "Test Area",
                "city": "Test City",
                "country": "Test Country",
                "lat": "7.8968",
                "lng": "6.7890",
            },
        }
        self.user = create_user(self.user_login)
        self.admin = create_user(self.admin_login, role="admin")

        self.aircraft = reverse("aircraft")
        self.airport = reverse("airport")
        return super().setUp()

    def test_airport_crud(self):
        # Not Logged In Test
        resp = self.client.get(self.airport)
        self.assertEqual(resp.status_code, 401)
        # Fetch Airports
        self.client.login(**self.user_login)
        resp = self.client.get(self.airport)
        self.assertEqual(resp.status_code, 200)
        # Create Airport [Only Admin]
        resp = self.client.post(self.airport, self.airport_data, format="json")
        self.assertEqual(resp.status_code, 403)
        self.client.login(**self.admin_login)
        resp = self.client.post(self.airport, self.airport_data, format="json")
        self.assertEqual(resp.status_code, 201)
        # Update Aircraft [Only Admin]
        port = Airport.objects.last()
        update_route = reverse("airport-dets", kwargs={"uid": port.uid})
        update_data = {"name": "updated airport", "icao": "4tgy"}
        self.client.login(**self.user_login)
        resp = self.client.put(update_route, self.airport_data, format="json")
        self.assertEqual(resp.status_code, 403)
        self.client.login(**self.admin_login)
        resp = self.client.put(update_route, update_data, format="json")
        port.refresh_from_db()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(port.name, update_data["name"])
        self.assertEqual(port.icao, update_data["icao"].upper())
        # Delete Craft [Only Admin]
        resp = self.client.delete(update_route)
        self.assertEqual(resp.status_code, 200)
        with self.assertRaises(Airport.DoesNotExist):
            Airport.objects.get(uid=port.uid)

    def test_aircraft_crud(self):
        # Not Logged In Test
        resp = self.client.get(self.aircraft)
        self.assertEqual(resp.status_code, 401)
        # Fetch Aircraft
        self.client.login(**self.user_login)
        resp = self.client.get(self.aircraft)
        self.assertEqual(resp.status_code, 200)
        # Create ArirCraft [Only Admin]
        resp = self.client.post(self.aircraft, self.aircraft_data)
        self.assertEqual(resp.status_code, 403)
        self.client.login(**self.admin_login)
        resp = self.client.post(self.aircraft, self.aircraft_data)
        self.assertEqual(resp.status_code, 201)
        # Update Aircraft [Only Admin]
        craft = Aircraft.objects.last()
        update_route = reverse("aircraft-dets", kwargs={"uid": craft.uid})
        update_data = {"serial_number": "hjyuth", "manufacturer": "nuvolar"}
        self.client.login(**self.user_login)
        resp = self.client.put(self.aircraft, self.aircraft_data)
        self.assertEqual(resp.status_code, 403)
        self.client.login(**self.admin_login)
        resp = self.client.put(update_route, update_data)
        craft.refresh_from_db()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(craft.serial_number, update_data["serial_number"].upper())
        self.assertEqual(craft.manufacturer, update_data["manufacturer"])
        # Delete Craft [Only Admin]
        resp = self.client.delete(update_route)
        self.assertEqual(resp.status_code, 200)
        with self.assertRaises(Aircraft.DoesNotExist):
            Aircraft.objects.get(uid=craft.uid)

    def test_flight_crud(self):
        flight_route = reverse("flight")
        # creating test aircraft and airports
        craft = Aircraft.objects.create(
            **{"serial_number": "AS12HD4B", "manufacturer": "Nuvola"}
        )
        loc1 = Location.objects.create(
            **{
                "area": "Test Area3",
                "city": "Test City3",
                "country": "Test Country3",
                "lat": "7.8964",
                "lng": "6.7893",
            }
        )
        loc2 = Location.objects.create(
            **{
                "area": "Test Area2",
                "city": "Test City2",
                "country": "Test Country2",
                "lat": "7.8963",
                "lng": "6.7892",
            }
        )
        departure = Airport.objects.create(
            **{"name": "Aiport1", "icao": "1EC4", "location": loc1}
        )
        arrival = Airport.objects.create(
            **{"name": "Aiport2", "icao": "1EC5", "location": loc2}
        )
        # Flight Data for Case 1
        flight_data = {
            "aircraft": craft.serial_number,
            "arrival": arrival.icao,
            "departure": departure.icao,
            "departure_dt": str(timezone.now() + timezone.timedelta(minutes=10)),
            "arrival_dt": str(timezone.now() + timezone.timedelta(minutes=60)),
        }
        # Not Logged In Test
        resp = self.client.get(flight_route)
        self.assertEqual(resp.status_code, 401)
        # Fetch Aircraft
        self.client.login(**self.user_login)
        resp = self.client.get(flight_route)
        self.assertEqual(resp.status_code, 200)
        # Create ArirCraft [Only Admin]
        resp = self.client.post(flight_route, flight_data)
        self.assertEqual(resp.status_code, 403)
        self.client.login(**self.admin_login)
        resp = self.client.post(flight_route, flight_data)
        self.assertEqual(resp.status_code, 201)
        # Update Aircraft [Only Admin]
        flight = Flight.objects.last()
        update_route = reverse("flight-dets", kwargs={"uid": flight.uid})
        update_data = {
            "status": "cancelled",
            "departure": arrival.icao,
            "arrival": departure.icao,
            "departure_dt": str(timezone.now() + timezone.timedelta(30)),
        }
        self.client.login(**self.admin_login)
        resp = self.client.put(update_route, update_data)
        flight.refresh_from_db()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(flight.departure, arrival)
        self.assertEqual(flight.arrival, departure)
        self.assertEqual(flight.status, update_data["status"])
        self.assertEqual(str(flight.departure_dt), update_data["departure_dt"])
        # Delete Craft [Only Admin]
        resp = self.client.delete(update_route)
        self.assertEqual(resp.status_code, 200)
        with self.assertRaises(Flight.DoesNotExist):
            Flight.objects.get(uid=flight.uid)

    def test_flight_search(self):
        pass
