from django import forms
from django.contrib.auth.models import User
from django.forms import widgets

from account.models import Profile, Cell
from account.post import PostCode, Position


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ()

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.errors.clear()
        for k, v in self.fields.items():
            v.widget.attrs.update({'class': 'login_form-field', 'placeholder': v.label})
            v.label = ''
            v.help_text = None


class ProfileRegistrationForm(forms.ModelForm):
    error_css_class = 'error'
    POSITIONS = ((x.name, x.value) for x in Position)
    CODES = ((x.name, x.value) for x in PostCode)
    position = forms.ChoiceField(widget=forms.Select, choices=POSITIONS)
    post_code = forms.ChoiceField(widget=forms.Select, choices=CODES)

    class Meta:
        model = Profile
        fields = ('position', 'post_code')

    def __init__(self, *args, **kwargs):
        super(ProfileRegistrationForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            v.widget.attrs.update({'class': 'rg_form-field', 'placeholder': v.label})
            v.label = ''
            v.help_text = None


class UserRegistrationForm(forms.ModelForm):
    error_css_class = 'error'

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            v.widget.attrs.update({'class': 'rg_form-field', 'placeholder': v.label})
            v.label = ''
            v.help_text = None


class NewCellForm(forms.ModelForm):
    date = forms.DateField(widget=widgets.SelectDateWidget)
    post_code = forms.CharField(disabled=True)

    class Meta:
        model = Cell
        fields = ('date', 'post_code', 'vacancy')

    def __init__(self, post_code, *args, **kwargs):
        super(NewCellForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            if k == 'date':
                v.widget.attrs.update({'class': 'form-date', 'placeholder': v.label})
            else:
                v.widget.attrs.update({'class': 'form-field', 'placeholder': v.label})
            v.label = ''
            v.help_text = None
            if k == 'post_code':
                try:
                    v.initial = post_code.value
                except:
                    v.initial = post_code
