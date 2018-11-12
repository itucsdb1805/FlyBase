from flight import Flight


class Database:
    def __init__(self):
        self.flights = {}
        self._last_flight_key = 0

    def add_flight(self, flight):
        self._last_flight_key += 1
        self.flights[self._last_flight_key] = flight
        return self._last_flight_key

    def delete_flight(self, flight_key):
        if flight_key in self.flights:
            del self.flights[flight_key]

    def get_flight(self, flight_key):
        flight = self.flights.get(flight_key)
        if flight is None:
            return None
        flight_ = Flight(flight.title, date=flight.date, airport=flight.airport)
        return flight_

    def get_flights(self):
        flights = []
        for flight_key, flight in self.flights.items():
            flight_ = Flight(flight.title, date=flight.date, airport=flight.airport)
            flights.append((flight_key, flight_))
        return flights
