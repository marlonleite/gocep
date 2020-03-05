import requests
from django.conf import settings

from .exceptions import BaseException


class ViaCepApi:
    """
    Class ViaCep Api
    https://viacep.com.br/
    """
    def __init__(self):
        self.path = settings.VIACEP_URL

    def _connect_api(self, *args, **kwargs):
        return requests.get(*args, **kwargs)

    def get_by_zip_code(self, zip_code):
        """
        Return Address from ZipCode
        :param zip_code: str ZipCode 8 digits
        :return: dict with address
        """
        url = f'{self.path}/ws/{zip_code}/json'

        response = self._connect_api(url)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            raise BaseException(message=f"Invalid Zip Code: {zip_code}")
        else:
            raise BaseException(message="Error")

    def get_by_address(self, uf, city, street):
        """
        Return ZipCode from Address
        :param uf: str State abbreviation
        :param city: str City name
        :param street: str Street of Address
        :return: dict with ZipCode and Address data
        """
        url = f'{self.path}/ws/{uf}/{city}/{street}/json'

        response = self._connect_api(url)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            raise BaseException(
                message=f"City and Street must be 3 characters of lenght")
        else:
            raise BaseException(message="Error")
