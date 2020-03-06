from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .viacep import ViaCepApi


class GoCepApiView(APIView):
    """
    GoCepApiView Api to consult Address or ZipCode
    """
    vc = ViaCepApi()

    def get(self, request, code=None):
        if code:
            data = self.vc.get_by_zip_code(code)
        else:
            uf = request.data.get('uf')
            city = request.data.get('city')
            street = request.data.get('street')
            zip_code = request.data.get('zip_code')

            if zip_code:
                data = self.vc.get_by_zip_code(zip_code)
            else:
                if None in [uf, city, street]:
                    message = "Required fields uf, city, street or zip_code"
                    return Response({'message': message}, status.HTTP_400_BAD_REQUEST)

                data = self.vc.get_by_address(uf, city, street)

        if data['status'] == 200:
            return Response(data['response'], status.HTTP_200_OK)

        if data['status'] == 400:
            return Response({'message': data['message']}, status.HTTP_404_NOT_FOUND)

        return Response({'error': 'API Error'}, status.HTTP_400_BAD_REQUEST)
