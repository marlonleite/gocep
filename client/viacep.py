import logging

import requests
from django.conf import settings


class ViaCepApi:
    """
    Class ViaCep Api
    https://viacep.com.br/
    """

    def __init__(self):
        self.api_base = settings.VIACEP_URL

    def connect_api_base(self, *args, **kwargs):
        message = kwargs.get("message")
        if message:
            del kwargs["message"]

        data = {}

        try:
            response = requests.get(*args, **kwargs)
            data.update({'status': response.status_code})

            if response.status_code == 200:
                response_data = response.json()

                if type(response_data) == list:
                    data['response'] = [self.normalize_keys(d) for d in response_data]
                else:
                    data['response'] = self.normalize_keys(response_data)

            elif response.status_code == 400:
                data['message'] = message
            else:
                # response.raise_for_status()
                pass

        except Exception as e:
            logging.error("Connection error")
            data.update({'status': 500 })

        return data

    def get_by_zip_code(self, zip_code):
        """
        Return Address from ZipCode
        :param zip_code: str ZipCode 8 digits
        :return: dict with address
        """
        url = f'{self.api_base}/ws/{zip_code}/json'
        message = f'Invalid Zip Code: {zip_code}'

        return self.connect_api_base(url, message=message)

    def get_by_address(self, federated_state, city, street):
        """
        Return ZipCode from Address
        :param federated_state: str state abbreviation
        :param city: str city name
        :param street: str street address
        :return: dict or list address
        """
        url = f'{self.api_base}/ws/{federated_state}/{city}/{street}/json'
        message = 'City and address must be at least three characters'

        return self.connect_api_base(url, message=message)

    def normalize_keys(self, data):

        if data.get('erro'):
            return data

        remove_keys = ['unidade', 'complemento', 'gia', 'ibge']

        for k in remove_keys:
            data.pop(k)

        data.update({
            "zip_code": data.pop('cep').replace('-', ''),
            "federated_state": data.pop('uf'),
            "city": data.pop('localidade'),
            "street": data.pop('logradouro'),
            "neighborhood": data.pop('bairro'),
        })

        return data
