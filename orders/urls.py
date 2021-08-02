from django.conf.urls import url
from django.urls import path, include
from django.views.generic import TemplateView

from orders.views import payment_process, PaymentDone

urlpatterns = [

    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^payment_process/$', payment_process, name='payment_process'),
    url(r'^payment_done/$', PaymentDone.as_view(), name='payment_done'),
    url(r'^payment_canceled/$', TemplateView.as_view(template_name="payment_canceled.html"), name='payment_canceled'),
]
