import json

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from paypal.standard.forms import PayPalPaymentsForm

from Cinema.createtickets import ticket_send
from Cinema.models import Tickets


def payment_process(request):
    global order_ticket_id_from_web
    global customers_email
    order_ticket_id_from_web = list(map(int, json.loads(request.body).get('data', [])))
    customers_email = str(json.loads(request.body).get('email', []))
    print(customers_email)
    host = request.get_host()
    ticket_id = str(order_ticket_id_from_web)
    amount = 0.00
    for all_tickets in Tickets.objects.all():
        for order_id in order_ticket_id_from_web:
            if all_tickets.id == order_id:
                amount += all_tickets.price
    print(amount)
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(amount),
        'item_name': f"Ticket{ticket_id}",
        'invoice': f"Payment Invoice(tickets {ticket_id})",
        'currency_code': 'EUR',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment_canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment_process.html', {'form': form})


class PaymentDone(View):
    def get(self, request):
        for buy_ticket_id in order_ticket_id_from_web:
            ticket = Tickets.objects.get(id=buy_ticket_id)
            ticket.sold = True
            ticket.save()
        ticket_send(order_ticket_id_from_web, customers_email)
        template_name = 'payment_done.html'
        return render(request, template_name, )
