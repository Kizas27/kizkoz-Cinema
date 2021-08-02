# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from Cinema.createtickets import create_tickets
from Cinema.forms import SignUpForm
from Cinema.models import Movie, Sessions, Tickets, Seats
from orders.views import payment_process

create_tickets()


def tickets(request):
    return render(
        request, template_name='tickets.html',
        context={'movies': Movie.objects.all()}
    )


def movie(request, id):
    time_now = timezone.now()
    movie = Movie.objects.get(id=id)
    context = {'time_now': time_now,
               'movie': movie,
               'Sessions': Sessions.objects.all(),
               'movies': Movie.objects.all()
               }
    return render(request, 'movie.html', context=context)


def session(request, id):
    time_now = timezone.now()
    session = Sessions.objects.get(id=id)
    session_tickets = Tickets.objects.filter(session_id=session.id)
    context = {
        'session': session,
        'session_tickets': session_tickets,
        'time_now': time_now,
        'Seats': Seats.objects.all(),
        'Tickets': Tickets.objects.all(),
        'movies': Movie.objects.all()
    }
    return render(request, 'session.html', context=context)


def index(request):
    return render(
        request, template_name='index.html',
        context={'movies': Movie.objects.all()}
    )


def contact_us(request):
    return render(
        request, template_name='contact_us.html',
        context={'movies': Movie.objects.all()}
    )


class SubmittableLoginView(LoginView):
    template_name = 'accounts/login.html'
    extra_context = {'movies': Movie.objects.all()}
    success_url = reverse_lazy('index')


class SubmittableLogoutView(LogoutView):
    template_name = 'accounts/form.html'
    extra_context = {'movies': Movie.objects.all()}
    success_url = reverse_lazy('index')


class SubmittableChangePassword(PasswordChangeView):
    template_name = 'accounts/form.html'
    extra_context = {'movies': Movie.objects.all()}
    success_url = reverse_lazy('index')


class SubmittableResetPassword(PasswordResetView):
    template_name = 'accounts/form.html'
    email_template_name = 'accounts/acc_reset_password.html'
    subject_template_name = 'accounts/acc_reset_subject.txt'
    extra_context = {'movies': Movie.objects.all()}
    success_url = reverse_lazy('index')


class SubmittableResetConfirmPassword(PasswordResetConfirmView):
    template_name = 'accounts/form.html'
    extra_context = {'movies': Movie.objects.all()}
    success_url = reverse_lazy('index')


def signup(request):
    if request.method == 'GET':
        return render(request, 'accounts/signup.html')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }
            message = render_to_string(template_name='accounts/acc_active_email.html', context=context)
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            # pataisyti y grazu teksta netgi gal grazinti
            return render(request, 'accounts/signup_confirm.html', )
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form, 'movies': Movie.objects.all()})


UserModel = get_user_model()


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.groups.add(1)
        user.save()
        return render(request, 'accounts/signup_done.html',)
    else:
        return HttpResponse('Activation link is invalid!')


def payment_processing(request):
    return payment_process(request)
