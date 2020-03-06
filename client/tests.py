from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class GoCepApiTest(APITestCase):
    """
    GoCepApiTest APITestCase
    """

    def test_address_url(self):
        """
          Ensure we can consult by site_url/<value>/.
        """
        data = {'zipcode': '57052180'}
        url = reverse('gocep-zipcode', kwargs=data)
        response = self.client.get(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 9)

    def test_address_params(self):
        """
          Ensure we can consult by site_url/?uf=value or site_url/?zip_code=value.
        """
        url = reverse('gocep-address')
        data = {'uf': 'AL', 'city': 'Maceió', 'street': 'Rua centro'}
        response = self.client.get(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data2 = {"zip_code": "57052180"}
        response2 = self.client.get(url, data2, format="json")

        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_error_address(self):
        """
            Ensure we can prevent invalid url requests
        """
        url = reverse('gocep-address')
        data = {'uf': 'AL', 'city': 'M', 'street': 'R'}
        response = self.client.get(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(response.data), 1)

        data2 = {'street': 'Rua das Acácias'}
        response2 = self.client.get(url, data2, format="json")

        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response2.data), 1)
        self.assertEqual(response2.data['message'], "Required fields uf, city, street")
