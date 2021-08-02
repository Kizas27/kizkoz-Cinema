from django.contrib.auth import views
from django.urls import path

from Cinema.views import index, tickets, signup, activate, SubmittableLoginView, session, movie, SubmittableLogoutView, \
    contact_us, SubmittableChangePassword, SubmittableResetPassword, \
    SubmittableResetConfirmPassword, payment_processing

views.LoginView.template_name = "accounts/login.html"
views.LogoutView.template_name = "accounts/form.html"
# views.PasswordChangeView.template_name = "accounts/form.html"
# views.PasswordChangeDoneView.template_name = "accounts/form.html"
# views.PasswordResetView.template_name = "accounts/form.html"
# views.PasswordResetView.email_template_name = "accounts/form.html"

urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contact_us, name='contact_us'),
    path('tickets/', tickets, name='tickets'),
    path('login/', SubmittableLoginView.as_view(), name="login"),
    path('logout/', SubmittableLogoutView.as_view(), name='logout'),
    path('change_password/', SubmittableChangePassword.as_view(), name='pass_change'),
    path('reset_password/', SubmittableResetPassword.as_view(), name='pass_reset'),
    path('confirm_password_reset/<uidb64>/<token>/', SubmittableResetConfirmPassword.as_view(), name='password_reset_confirm'),
    path('signup/', signup, name='signup'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('session/<int:id>/', session, name='session'),
    path('movie/<int:id>/', movie, name='movie'),
    path('payment_processing', payment_processing, name='payment_processing'),

]
