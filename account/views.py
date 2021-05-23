import math
from datetime import datetime, timedelta

import shortuuid as shortuuid
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from account.forms import UserRegistrationForm, ProfileRegistrationForm, UserLoginForm, NewCellForm
from account.models import Profile, Cell
from account.post import Position, PostCode


def vacation_accept(request, cell_id):
    cell = Cell.objects.get(id=cell_id)
    cell.status = ('Accepted', 1)
    cell.save()
    return redirect('account:vacancies')


def vacancies(request):
    user = Profile.objects.get(user=request.user)
    cells = Cell.objects.all()
    if Position[user.position] == Position.PO:
        cells = list(filter(lambda x: user.post_code == x.post_code and x.profile_set.all(), cells))
    else:
        cells = list(filter(lambda x: user in x.profile_set.all(), cells))
    new_cells = []
    for i in range(math.ceil(len(cells) / 5)):
        new_cells.append([])
        for j in range(5 * i, min(((i + 1) * 5, len(cells)))):
            new_cells[-1].append({
                'date': cells[j].date,
                'address': cells[j].post_code,
                'post_code': PostCode[cells[j].post_code].value,
                'vacancy': Position[cells[j].vacancy].value,
                'status': cells[j].status.split()[0].replace("'", '').replace("(", '').replace(",", ''),
                'id': cells[j].id,
            })

    return render(request, 'account/vacancies.html', {
        'user': user,
        'cells': new_cells,
        'is_ro': Position[user.position] == Position.PO
    })


def cancel(request, cell_id):
    Cell.objects.get(id=cell_id).profile_set.remove(Profile.objects.get(user=request.user))
    return redirect('account:vacancies')


def decline(request, cell_id):
    cell = Cell.objects.get(id=cell_id)
    cell.status = ('Declined', -1)
    cell.save()
    return redirect('account:vacancies')


def accept(request, id):
    Cell.objects.get(id=id).profile_set.add(Profile.objects.get(user=request.user))
    return redirect('account:profile')


def remove(request, id):
    instance = Cell.objects.get(id=id)
    instance.delete()
    return redirect('account:profile')


def profile(request):
    user = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        cell_form = NewCellForm(user.post_code, request.POST)
        if cell_form.is_valid():
            new_cell = cell_form.save(commit=False)
            new_cell.save()
            Cell.objects.create(date=new_cell.date, post_code=PostCode[new_cell.post_code], vacancy=Position[new_cell.vacancy])

    cells = sorted(Cell.objects.filter(date__range=[datetime.now(), datetime.now() + timedelta(days=31)]), key=lambda x: x.date)
    cells = list(filter(lambda x: x.post_code == user.post_code, cells))
    cells = list(filter(lambda x: user not in x.profile_set.all(), cells))
    if user.position in [Position.CMO.name, Position.BMO.name, Position.MO.name]:
        cells = list(filter(lambda x: x.vacancy in [Position.CMO.name, Position.BMO.name, Position.MO.name], cells))
    elif user.position in [Position.CKM.name, Position.KM.name]:
        cells = list(filter(lambda x: x.vacancy in [Position.CKM.name, Position.KM.name], cells))
    elif user.position == Position.K.name:
        cells = list(filter(lambda x: x.vacancy == Position.K.name, cells))

    new_cells = []
    for i in range(math.ceil(len(cells) / 5)):
        new_cells.append([])
        for j in range(5 * i, min(((i + 1) * 5, len(cells)))):
            new_cells[-1].append({
                'date': cells[j].date,
                'address': cells[j].post_code,
                'post_code': PostCode[cells[j].post_code].value,
                'vacancy': Position[cells[j].vacancy].value,
                'id': cells[j].id
            })

    return render(request, 'account/profile.html', {
        'user': user,
        'cells': new_cells,
        'is_ro': Position[user.position] == Position.PO,
        'cell_form': NewCellForm(post_code=PostCode[user.post_code])
    })


def home(request, error):
    username = ''
    password = ''
    if request.session.has_key('username') and request.session.has_key('password'):
        username = request.session['username']
        password = request.session['password']
        return profile(request)
    form = UserLoginForm()
    return render(request, 'account/login.html', {
        'form': form,
        'error': error
    })


def user_logout(request):
    logout(request)
    return redirect('account:user_login')


@csrf_exempt
def user_login(request):
    error = False
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form['username'].value(), password=form['password'].value())
            if user is not None and user.is_active:
                if request.POST.get('remember'):
                    request.session['username'] = form['username'].value()
                    request.session['password'] = form['password'].value()
                login(request, user)
                return redirect('account:profile')
        error = True
    return home(request, error)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            try:
                new_user = user_form.save(commit=False)
                new_user.username = shortuuid.uuid(new_user.first_name + new_user.last_name)
                new_profile = profile_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()
                new_profile.save()
                Profile.objects.create(user=new_user, position=new_profile.position, post_code=new_profile.post_code)
                return render(request, 'account/register_done.html', {'new_user': new_user})
            except:
                return render(request, 'account/register.html', {
                    'user_form': UserRegistrationForm(),
                    'profile_form': ProfileRegistrationForm(),
                    'error': True
                })
    else:
        if request.session.has_key('username') and request.session.has_key('password'):
            username = request.session['username']
            password = request.session['password']
            return redirect('account:profile')
        user_form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()
    return render(request, 'account/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'error': False
    })
