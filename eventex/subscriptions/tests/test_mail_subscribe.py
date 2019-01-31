from django.core import mail
from django.test import TestCase


class SubcribePostTestValid(TestCase):
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
