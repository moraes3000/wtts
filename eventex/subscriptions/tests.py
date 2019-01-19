from django.core import mail
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
class SubcribePostTest(TestCase):
    def setUp(self):
        data = dict(name="Bruno Moraes", cpf="12345678901",
                    email="bruno_bmoraes@hotmail.com", phone='11-94160-0000')

        self.response = self.client.post('/inscricao/', data)


    def test_post(self):
        """valid post shoultd redirect to /inscricao/"""


        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1,len(mail.outbox))

    def test_subscription_email_subjects(self):
        email = mail.outbox[0]
        expect = 'Confirmação de Inscrição'

        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@evetex.com.br' , 'bruno_bmoraes@hotmail.com']

        self.assertEqual(expect, email.to)


    def test_subscription_email_body(self):
        email = mail.outbox[0]
        self.assertIn('Bruno Moraes', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('bruno_bmoraes@hotmail.com', email.body)
        self.assertIn('11-94160-0000', email.body)


class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """ Invalid Post should not redirect """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscriptions_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)


class SubscribeSuccessMensage(TestCase):
    def test_message(self):
        data = dict(name="Bruno Moraes", cpf="12345678901",
                    email="bruno_bmoraes@hotmail.com", phone='11-94160-0000')

        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição  realizada com sucesso')



