from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserAuthTest(APITestCase):
    '''
    Test if all endpoints are returning the expected data
    '''

    def setUp(self):
        self.username = 'testuser'
        self.email = 'testuser@gmail.com'
        self.password = 'pass'

        self.login_data = {
            'password': self.password,
            'username': self.username,
        }

        self.register_data = {
            **self.login_data,
            'email': self.email,
            'passwordConfirm': self.password
        }

    def create_user(self):
        '''
        Helper function used to create a user directly in the database
        '''
        user = User(
            username=self.username,
            email=self.email
        )
        user.set_password(self.password)
        user.save()
        return user

    def test_register(self):
        '''
        Test if the registration endpoint is working
        '''
        url = reverse('v1:register')
        response = self.client.post(url, self.register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        self.assertTrue(User.objects.get().is_active)
        self.assertFalse(User.objects.get().is_verified)
        self.assertFalse(User.objects.get().is_admin)

    def test_login(self):
        '''
        Test if the login endpoint is working
        '''
        url = reverse('v1:token_pair')
        user = self.create_user()

        response = self.client.post(url, self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should return access and refresh tokens
        data = response.json()
        self.assertIn('access', data.keys())
        self.assertIn('refresh', data.keys())

    def test_refresh(self):
        '''
        Test if refresh token endpoint is working
        This endpoint is used to generate a new access token
        '''
        login_url = reverse('v1:token_pair')
        refresh_url = reverse('v1:token_refresh')
        user = self.create_user()

        login_response = self.client.post(login_url, self.login_data)
        initial_access_token = login_response.json().get('access')
        refresh_token = login_response.json().get('refresh')

        refresh_response = self.client.post(
            refresh_url, {'refresh': refresh_token}
        )
        refresh_data = refresh_response.json()

        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_data.keys())

        new_access_token = refresh_data.get('access')
        self.assertNotEqual(new_access_token, initial_access_token)
