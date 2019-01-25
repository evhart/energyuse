# Create your views here.
import csv
import logging

import biostar
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, ButtonHolder, Div
from biostar.apps.users import auth
from energyuse.apps.eusers.models import User, EnergyConsumption
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, ListView, FormView, UpdateView
import mechanize
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


class EnergyNoteEditForm(forms.Form):
    energynote_email = forms.EmailField(help_text="Your energy note email, it will not be visible to other users")
    energynote_password = forms.CharField(
        help_text="Your energy note password, it will not be stored and is only used once for validating your account",
        widget=forms.PasswordInput())


    def verify_credentials(self, energynote_email, energynote_password):
        email = energynote_email #Actually an email
        password = energynote_password

        #Fake a login and see if it is successful:
        br = mechanize.Browser()
        ernergynote_url = 'https://www.energynote.eu/login/?action=login'

        br.open(ernergynote_url)
        br.select_form(name='registerform')
        br.form['log'] = email
        br.form['pwd'] = password

        req = br.submit()

        #Simply check if the login failed based on the url:
        #if req.read().find('<strong>Something went wrong.</strong>') is -1:
        if req.geturl() != ernergynote_url:
            return True
        return False


    def clean(self):
        '''
            Check if the account is valid by submitting it to energynote website
        '''
        cleaned_data = super(EnergyNoteEditForm, self).clean()
        email = cleaned_data.get("energynote_email")
        password = cleaned_data.get("energynote_password")

        if email and password:
            if not self.verify_credentials(email, password):
                raise forms.ValidationError("Could not connect your EnergyNote account. Please check your credentials and make sure that you are part of the DecarboNet Energy Trial.")



    def __init__(self, *args, **kwargs):
        super(EnergyNoteEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.error_text_inline = False
        self.helper.help_text_inline = True
        self.helper.layout = Layout(
            # Fieldset(
            #     'Connect your EnergyNote account',
                Div(
                    Div('energynote_email', ),
                    Div('energynote_password', ),
                    Submit('submit', u'Connect Account', css_class='btn btn-success'),
                    css_class="col-md-offset-3 col-md-6",
                ),

            # ),

        )


class EditEnergyNote(LoginRequiredMixin, FormView):
    form_class = EnergyNoteEditForm

    def get(self, request, *args, **kwargs):
        target = User.objects.get(pk=self.kwargs['pk'])
        target = auth.user_permissions(request=request, target=target)
        if not target.has_ownership:
            messages.error(request, "Only owners may edit their EnergyNote account")
            return HttpResponseRedirect(reverse("home"))

        initial = {}
        initial['energynote_email'] = getattr(target, 'energynote_email')

        form = self.form_class(initial=initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request=None, *args, **kwargs):
        target = User.objects.get(pk=self.kwargs['pk'])
        target = auth.user_permissions(request=request, target=target)


        # The essential authentication step.
        if not target.has_ownership:
            messages.error(request, "Only owners may edit their EnergyNote account")
            return HttpResponseRedirect(reverse("home"))

        form = self.form_class(request.POST)
        if form.is_valid():
            f = form.cleaned_data

            # Valid data. Save model attributes and redirect.
            setattr(target, 'energynote_email', f['energynote_email'])
            setattr(target, 'is_energynote_verified', True)

            target.save()
            messages.success(request, "EnergyNote account connected")
            return HttpResponseRedirect(self.get_success_url())


        # There is an error in the form.
        return render(request, self.template_name, {'form': form})



    def get_success_url(self):
        return reverse("user-details", kwargs=dict(pk=self.kwargs['pk']))


class UserEditForm(biostar.apps.users.views.UserEditForm):


    def clean_name(self):
        print(self.profile)
        name = self.cleaned_data.get("name")
        if get_user_model().objects.filter(name=name).exclude(profile=self.profile):
            raise forms.ValidationError("Another user is already registered with this username.")
        return name


    def __init__(self, profile,  *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.profile = profile
        self.helper = FormHelper()
        self.helper.error_text_inline = False
        self.helper.help_text_inline = True
        self.helper.layout = Layout(
            Fieldset(
                'Update your profile',
                Div(
                    Div('name', ),
                    Div('email', ),
                    Div('location'),
                    Div('website'),
                    css_class="col-md-offset-3 col-md-6",
                ),
                Div(
                    Div('twitter_id', css_class="col-md-6"),
                    Div('scholar', css_class="col-md-6"),
                    Div('digest_prefs', css_class="col-md-6"),
                    Div('message_prefs', css_class="col-md-6"),
                    css_class="col-md-12",
                ),
                Div(
                    Div('my_tags'),
                    Div('watched_tags'),
                    Div('info'),
                    ButtonHolder(
                        Submit('submit', 'Submit')
                    ),
                    css_class="col-md-12",
                ),
            ),

        )


class EditUser(biostar.apps.users.views.EditUser):
    form_class = UserEditForm
    user_fields = "name email".split()
    prof_fields = "location website info scholar my_tags watched_tags twitter_id message_prefs digest_prefs".split()

    
    def get(self, request, *args, **kwargs):
        target = User.objects.get(pk=self.kwargs['pk'])
        target = auth.user_permissions(request=request, target=target)
        profile = target.profile

        if not target.has_ownership:
            messages.error(request, "Only owners may edit their profiles")
            return HttpResponseRedirect(reverse("home"))

        initial = {}

        for field in self.user_fields:
            initial[field] = getattr(target, field)

        for field in self.prof_fields:
            initial[field] = getattr(target.profile, field)

        form = self.form_class(profile, initial=initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        target = User.objects.get(pk=self.kwargs['pk'])
        target = auth.user_permissions(request=request, target=target)
        profile = target.profile

        # The essential authentication step.
        if not target.has_ownership:
            messages.error(request, "Only owners may edit their profiles")
            return HttpResponseRedirect(reverse("home"))

        form = self.form_class(profile, request.POST)
        if form.is_valid():
            f = form.cleaned_data

            if User.objects.filter(email=f['email']).exclude(pk=request.user.id):
                # Changing email to one that already belongs to someone else.
                messages.error(request, "The email that you've entered is already registered to another user!")
                return render(request, self.template_name, {'form': form})

            # Valid data. Save model attributes and redirect.
            for field in self.user_fields:
                setattr(target, field, f[field])

            for field in self.prof_fields:
                setattr(profile, field, f[field])

            target.save()
            profile.add_tags(profile.watched_tags)
            profile.save()
            messages.success(request, "Profile updated")
            return HttpResponseRedirect(self.get_success_url())

        # There is an error in the form.
        return render(request, self.template_name, {'form': form})

    def get_success_url(self):
        return reverse("user-details", kwargs=dict(pk=self.kwargs['pk']))



