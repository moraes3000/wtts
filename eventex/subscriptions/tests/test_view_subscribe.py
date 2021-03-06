from django.core import mail
from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription
class SubscribeTestGet(TestCase):
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
        tags = (
            ('<form', 1),
            ('type="text"',3),
            ('type="email"', 1),
            ('type="submit"', 1),
            ('<input',6)

        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)


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



class SubscribeSuccessMensage(TestCase):
    def test_message(self):
        data = dict(name="Bruno Moraes", cpf="12345678901",
                    email="bruno_bmoraes@hotmail.com", phone='11-94160-0000')

        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição  realizada com sucesso')



