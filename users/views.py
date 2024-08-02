from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm, CustomUserLoginForm
from .models import CustomUser

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_verification_email(request, user)
            return redirect('users:registration_complete')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def send_verification_email(request, user):
    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    message = render_to_string('users/account_activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.email_verified = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'users/account_activation_invalid.html')

def registration_complete(request):
    return render(request, 'users/registration_complete.html')

def custom_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = CustomUserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('home')
