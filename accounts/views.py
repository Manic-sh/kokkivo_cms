from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import csrf
from django.http import JsonResponse
from django.db import IntegrityError

from accounts.models import Address, Profile, User
from accounts.forms import UserRegistrationForm, UserLoginForm, AddressForm, UserDetailsForm


def login(request):
    if request.method == 'POST' and 'register' in request.POST:
        form_register = UserRegistrationForm(request.POST)
        form_address = AddressForm(request.POST)

        try:
            if all([form_register.is_valid(), form_address.is_valid()]):
                user = form_register.save()
                address = form_address.save(commit=False)
                address.user = user
                address.save()

                user = auth.authenticate(email=request.POST.get('email'),
                                         password=request.POST.get('password1'))
                if user:
                    auth.login(request, user)
                    return JsonResponse({"status": "200"})
                else:
                    return JsonResponse({"message": "Your email or password was not recognised"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "User with this email already exists"}, status=400)
        else:
            return JsonResponse({"message": "Passwords do not match"}, status=400)

    else:
        form_register = UserRegistrationForm()
        form_address = AddressForm()

    if request.method == 'POST' and 'login' in request.POST:

        form_login = UserLoginForm(request.POST)
        if form_login.is_valid():
            user = auth.authenticate(email=request.POST.get('login_email'),
                                     password=request.POST.get('password'))
            if user is not None:
                auth.login(request, user)
                return JsonResponse({"status": "200"})
            else:
                return JsonResponse({"message": "Your email or password was not recognised"}, status=400)

    else:
        form_login = UserLoginForm()

    args = {'form_register': form_register,
            'form_address': form_address, 'form_login': form_login}
    args.update(csrf(request))
    return render(request, 'accounts/login.html', args)


@login_required(login_url='/account/login/')
def account(request):
    user = request.user
    try:
        address = Address.objects.get(user=user)
    except Address.DoesNotExist:
        address = None
        print("User does not exist")
    return render(request, 'accounts/account.html', {'address': address})


def logout(request):
    auth.logout(request)
    return redirect(reverse('home'))


@login_required(login_url='/account/login/')
def edit_address(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    address = get_object_or_404(Address, user=user)

    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect(reverse('account'))
    else:
        form = AddressForm(instance=address)

    args = {'form': form}
    args.update(csrf(request))

    return render(request, 'accounts/account_address_form.html', args)


@login_required(login_url="/account/login/")
def edit_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile = get_object_or_404(Profile, user=user)


@login_required(login_url='/account/login/')
def edit_details(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        form = UserDetailsForm(request.POST, instance=user)
        if form.is_valid():
            try:
                existing_user = User.objects.get(
                    email=request.POST.get('email'))
            except User.DoesNotExist:
                existing_user = None

            if existing_user and existing_user != user:
                return JsonResponse({"message": "User with this email already exists"}, status=400)
            else:
                form.save()
                return JsonResponse({"status": "200"})
    else:
        form = UserDetailsForm(instance=user)

    args = {'form': form}
    args.update(csrf(request))

    return render(request, 'accounts/account_details_form.html', args)
