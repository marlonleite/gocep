from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class AddressApiTest(APITestCase):
    """
    AddressApiTest APITestCase
    """

    def test_address_url(self):
        """
          Ensure we can consult by site_url/api/<value>/.
        """
        data = {'zip_code': '57052180'}
        url = reverse('gocep-zip_code', kwargs=data)
        response = self.client.get(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)

    def test_address_params(self):
        """
          Ensure we can consult by site_url/?uf=value or site_url/api/?zip_code=value.
        """
        url = reverse('gocep-address')
        data = {'uf': 'AL', 'city': 'Maceió', 'street': 'Rua centro'}
        response = self.client.get(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data2 = {"zip_code": "57052180"}
        response2 = self.client.get(url, data2, format="json")

        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_address_few_chars_city_street(self):
        """
            Ensure we can prevent invalid city, street fields
        """
        url = reverse('gocep-address')
        data = {'uf': 'AL', 'city': 'M', 'street': 'R'}
        response = self.client.get(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(response.data), 1)

    def test_address_invalid_fields(self):
        """
          Ensure we can prevent no required fields
        """
        url = reverse('gocep-address')
        data = {'street': 'Rua das Acácias'}
        response = self.client.get(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['message'], "Required fields uf, city, street or zip_code.")

    def test_address_invalid_zip_code(self):
        """
          Ensure we can prevent invalid field zip_code
        """
        data = {'zip_code': '5701551435'}
        url = reverse('gocep-zip_code', kwargs=data)
        response = self.client.get(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(response.data), 1)

        url2 = reverse('gocep-address')
        response2 = self.client.get(url2, data, format="json")

        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(response2.data), 1)
