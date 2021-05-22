import shortuuid as shortuuid
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from account.forms import UserRegistrationForm, ProfileRegistrationForm, UserLoginForm
from account.models import Profile


def home(request):
    username = ''
    password = ''
    if request.session.has_key('username') and request.session.has_key('password'):
        username = request.session['username']
        password = request.session['password']
        return HttpResponse('Auth success')
    form = UserLoginForm()
    return render(request, 'account/login.html', {
        'form': form
    })


def user_logout(request):
    logout(request)

    return redirect('account:user_login')

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form['username'].value(), password=form['password'].value())
            if user is not None and user.is_active:
                if request.POST.get('remember'):
                    request.session['username'] = form['username'].value()
                    request.session['password'] = form['password'].value()
                login(request, user)
                return HttpResponse('Auth success')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        return home(request)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.username = shortuuid.uuid(new_user.first_name + new_user.last_name)
            new_profile = profile_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile.save()
            Profile.objects.create(user=new_user, position=new_profile.position, post_code=new_profile.post_code)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()
    return render(request, 'account/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
