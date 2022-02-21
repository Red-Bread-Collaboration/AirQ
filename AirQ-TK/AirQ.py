#! /usr/bin/python3

import requests
import json

import datetime
from math import radians, cos, sin, asin, sqrt

DEFAULT_HOST = "https://my.cityair.io/api/request.php?map="
STATIONS_URL = "MoApi2/GetMoItems"
STATIONS_PACKETS_URL = "MoApi2/GetMoPackets"


def anonymize_request(body: dict) -> dict:
    request = body.copy()
    request.update(Token="***")
    return request


def haversine(lat1, lon1, lat2, lon2):
    """
    Вычисляет расстояние в километрах между двумя точками, учитывая окружность Земли.
    https://en.wikipedia.org/wiki/Haversine_formula
    """

    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return round(km, 2)


class AirQException(Exception):
    pass


class TransportException(AirQException):
    """
    raised when request contains bad json
    """

    def __init__(self, response: requests.models.Response):
        body = anonymize_request(json.loads(response.request.body.decode("utf-8")))
        message = (
            f"Error while getting data:\n"
            f"url: {response.url}\n"
            f"request body: {json.dumps(body)}\n"
            f"request headers: {response.headers}\n"
            f"response code: {response.status_code}"
            f"response headers: {response.headers}"
            f"response content: {response.content}"
        )
        super().__init__(message)


class ServerException(AirQException):
    """
    cityair backend exception. raised when request contains 'IsError'=True
    """

    def __init__(self, response: requests.models.Response):
        body = anonymize_request(json.loads(response.request.body.decode("utf-8")))
        message = (
            f"Error while getting data:\n"
            f"url: {response.url}\n"
            f"request body: {json.dumps(body)}\n"
        )
        try:
            message += (
                f"{response.json()['ErrorMessage']}:\n"
                f"{response.json().get('ErrorMessageDetals')}"
            )
        except KeyError:
            message += str(response.json())
        super().__init__(message)


class EmptyDataException(AirQException):
    """
    raised whe 'Result' field in response is empty
    """

    def __init__(self, response: requests.models.Response = None, item=None):
        message = (
            "No data for the request. Try changing query arguments, "
            "i.e. start_date or finish_date.\n"
        )
        if response:
            body = anonymize_request(json.loads(response.request.body.decode("utf-8")))
            message += f"url: {response.url}\n" f"request body: {json.dumps(body)}\n"
        if item:
            message += f"item: {item}"
        super().__init__(message)


class AirQ:
    def __init__(
        self,
        token: str,
        host_url: str = DEFAULT_HOST,
        timeout: int = 100,
        verify_ssl: bool = True,
    ):
        """
        Parameters
        ----------
        token:  str
            auth information
        host_url: str, default {DEFAULT_HOST}
            url of the CityAir API, you may want to change it in case using a
            StandAloneServer
        timeout: int, default 100
            timeout for the server request
        verify_ssl: bool, default True
            whether to verify SSL certificate
        """

        self.host_url = host_url
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not token:
            raise ValueError("Err: Could not find token")

        self.token = token

    def _make_request(self, method_url: str, *keys: str, **kwargs: object):
        """
        Making request to cityair backend

        Parameters
        ----------
        method_url :  str
            url of the specified method
        *keys: [str]
            keys, which data to return from the raw server response
        **kwargs : dict
            additional args which are directly passed to the request body
        -------"""
        body = {"Token": self.token, **kwargs}
        url = f"{self.host_url}/{method_url}"

        try:
            response = requests.post(
                url, json=body, timeout=self.timeout, verify=self.verify_ssl
            )

        except requests.exceptions.ConnectionError as e:
            raise AirQException(f"Got connection error: {e}") from e

        try:
            response.raise_for_status()

        except requests.exceptions.HTTPError as e:
            try:
                details = response.json().get("ErrorMessage")
            except Exception:
                details = ""

            raise AirQException(f"Got HTTP error: {e}: {details}") from e

        try:
            response_json = response.json()

        except json.JSONDecodeError as e:
            raise TransportException(response) from e

        if response_json.get("IsError"):
            raise ServerException(response)

        response_data = response_json.get("Result")

        for key in keys:
            if len(response_data[key]) == 0:
                raise EmptyDataException(response=response, item=key)

        if len(keys) == 0:
            return response_data
        elif len(keys) == 1:
            return response_data[keys[0]]
        else:
            return [response_data[key] for key in keys]

    def get_stations(self):
        """
        Provides devices information in various formats
        """

        locations_data, stations_data = self._make_request(
            STATIONS_URL, "Locations", "MoItems"
        )

        compressed_locations_data = {
            i["LocationId"]: [i["Name"], i["NameRu"]] for i in locations_data
        }

        compressed_stations_data = [
            {
                "MoId": i["MoId"],
                "DotItem": i["DotItem"],
                "PublishName": i["PublishName"],
                "PublishNameRu": i["PublishNameRu"],
                "City": compressed_locations_data[i["LocationId"]][0],
                "CityRu": compressed_locations_data[i["LocationId"]][1],
            }
            for i in stations_data
        ]

        return compressed_stations_data

    def get_station_data(self, station_id: int):
        """
        Provides data from the selected station
        Parameters
        ----------
        station_id : int
            id of the station
        -------"""

        start_date = str(
            datetime.datetime.utcnow() - datetime.timedelta(hours=1)
        ).replace(" ", "T")

        finish_date = str(datetime.datetime.utcnow()).replace(" ", "T")

        filter_ = {
            "TakeCount": 15,
            "MoId": station_id,
            "IntervalType": 1,
            "FilterType": 1,
            "BeginTime": start_date,
            "EndTime": finish_date,
        }

        measurescheme, packets = self._make_request(
            STATIONS_PACKETS_URL, "MeasureSchemeItems", "Packets", Filter=filter_
        )

        compressed_measurescheme = {
            i["ValueType"]: [
                i["TypeName"],
                i["TypeNameRu"],
                i["Measurement"],
                i["MeasurementRu"],
            ]
            for i in measurescheme
        }

        # metrics = [
        #     f"{compressed_measurescheme[i['VT']][0]}: {i['V']} {compressed_measurescheme[i['VT']][2]}"
        #     for i in packets[-1]["Data"]
        # ]

        metrics = {
            compressed_measurescheme[i["VT"]][
                0
            ]: f"{round(i['V'], 1)} {compressed_measurescheme[i['VT']][3]}"
            for i in packets[-1]["Data"]
        }

        aqi = packets[-1]["VtAqi"]["CityairAqi"]

        return metrics, aqi
