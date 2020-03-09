from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .viacep import ViaCepApi


class AddressApiView(APIView):
    """
        View consult Zip Code.
    """
    vc = ViaCepApi()

    def get(self, request, zip_code=None):
        """
        Method Get address or list of addresses
        :param zip_code: <int>
        :param federated_state, city, street or zip_code: <string> query params
        :return: dict or list addresses
        """

        if zip_code:
            response = self.vc.get_by_zip_code(zip_code)
        else:
            address_data = {}
            for k, v in request.query_params.items():
                address_data.update({k: v})

            allowed_keys = {"federated_state", "city", "street"}

            if allowed_keys != address_data.keys():
                message = "Required fields federated_state, city, street."
                return Response({'message': message}, status.HTTP_400_BAD_REQUEST)

            response = self.vc.get_by_address(**address_data)

        if response['status'] == 200:
            return Response(response['response'], status.HTTP_200_OK)

        if response['status'] == 400:
            return Response({'message': response['message']}, status.HTTP_404_NOT_FOUND)

        return Response({'error': 'API Error'}, status.HTTP_400_BAD_REQUEST)
