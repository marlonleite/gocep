from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .viacep import ViaCepApi


class GoCepApiView(APIView):
    """
    GoCepApiView Api to consult Address or ZipCode
    """
    vc = ViaCepApi()

    def get(self, request, zipcode=None):
        if zipcode:
            data = self.vc.get_by_zip_code(zipcode)
        else:

            address_data = {}
            for k, v in request.query_params.items():
                address_data.update({k: v})

            if address_data.get("zip_code"):
                data = self.vc.get_by_zip_code(address_data["zip_code"])
            else:
                if address_data.get("zip_code"):
                    del address_data["zip_code"]

                allowed_keys = {"uf", "city", "street"}

                if allowed_keys != address_data.keys():
                    message = "Required fields uf, city, street"
                    return Response({'message': message}, status.HTTP_400_BAD_REQUEST)

                data = self.vc.get_by_address(**address_data)

        if data['status'] == 200:
            return Response(data['response'], status.HTTP_200_OK)

        if data['status'] == 400:
            return Response({'message': data['message']}, status.HTTP_404_NOT_FOUND)

        return Response({'error': 'API Error'}, status.HTTP_400_BAD_REQUEST)
