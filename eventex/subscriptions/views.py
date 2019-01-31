from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():

        # usado para teste
        # context =  dict(name="Bruno Moraes", cpf="12345678901",
        #             email="bruno_bmoraes@hotmail.com", phone='11-94160-0000')
        #
        # body = render_to_string('subscriptions/subscription_email.txt',
        #                         context )

        # mail.send_mail('Confirmação de Inscrição' ,
        #                body,
        #                'contato@eventex.com.br' ,
        #                ['contato@evetex.com.br', 'bruno_bmoraes@hotmail.com']
        #                )
        # return HttpResponseRedirect('/inscricao/')
        # fim usado para teste

            body = render_to_string('subscriptions/subscription_email.txt',
                                form.cleaned_data )

            mail.send_mail('Confirmação de Inscrição' ,
                       body,
                       'contato@eventex.com.br' ,
                       ['contato@evetex.com.br', form.cleaned_data['email']]
                       )

            messages.success(request, 'Inscrição  realizada com sucesso')
            return HttpResponseRedirect('/inscricao/' ,messages)
        else:
            return render(request, 'subscriptions/subscriptions_form.html' ,
                          {'form': form})
    else:
        context = {'form': SubscriptionForm()}
        return render(request, 'subscriptions/subscriptions_form.html', context)
