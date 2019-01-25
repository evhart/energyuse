from django import forms
from biostar.apps.users.models import Profile
from energyuse.apps.eusers.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.contrib.auth import get_user_model


class SignupForm(forms.ModelForm):
    name = forms.CharField(max_length=30, label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'password1', 'password2')
        field_order = ['email', 'name', 'password1', 'password2']


    def clean_name(self):
        name = self.cleaned_data.get("name")
        if get_user_model().objects.filter(name=name).exists():
            raise forms.ValidationError("A user is already registered with this username.")
        return name


    def signup(self, request, user):
        user = super(SignupForm, self).save(commit=False)
        user.name = self.cleaned_data['name']
        user.save()
        #Profile.auto_create(instance=user, created=True) #Created with the signals
