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

        response = requests.get(*args, **kwargs)

        data = {'status': response.status_code}

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

    def get_by_address(self, uf, city, street):
        """
        Return ZipCode from Address
        :param uf: str State abbreviation
        :param city: str City name
        :param street: str Street of Address
        :return: dict with ZipCode and Address data
        """
        url = f'{self.api_base}/ws/{uf}/{city}/{street}/json'
        message = 'City and street must be at least three characters'

        return self.connect_api_base(url, message=message)

    def normalize_keys(self, data):
        data['zip_code'] = data.pop('cep')
        data['address'] = data.pop('logradouro')
        data['address2'] = data.pop('complemento')
        data['neighborhood'] = data.pop('bairro')
        data['city'] = data.pop('localidade')
        data['unity'] = data.pop('unidade')
        return data
