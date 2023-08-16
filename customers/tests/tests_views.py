from django.test import TestCase
from django.shortcuts import reverse


class LoginTest(TestCase):
    def test_login_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')


""" class OrderListTest(TestCase):
    def test_order_list(self):
        # TODO some sort of test
        response = self.client.get(reverse('order-list'))
        print(response.content) """