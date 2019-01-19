from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription
class SubscribeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """GET /inscricao/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)


    def test_template(self):
        """ must use subscription/subscriptions_form.html"""
        self.assertTemplateUsed(self.response, 'subscriptions/subscriptions_form.html')

    def test_html(self):
        """teste html"""
        self.assertContains(self.response, '<form')
        # self.assertContains(self.response, '<input',0)
        self.assertContains(self.response, 'type="text"',3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """context must have subscription form """
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """contex must have subscription form """
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)
#
    def test_form_has_fields(self):
        """form must have 4 field """
        form = self.response.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))
#
#
#
#
# class SubscriptionsModelTest(TestCase):
#     def test_create(self):
#         obj = Subscription(
#             name="Bruno Moraes",
#             cpf="123456789",
#             email='brunomoraes@hotmail.com',
#             phone='11-94160-0000'
#         )
#         obj.save()
#         self.asserTrue(Subscription.objects.exists())
