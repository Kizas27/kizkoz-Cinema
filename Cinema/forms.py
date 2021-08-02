from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import (Form, )

from Cinema.models import Tickets


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username')


class TicketsForm(Form):
    class Meta:
        model = Tickets
        fields = ('session', 'price', 'sold')
