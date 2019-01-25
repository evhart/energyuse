from biostar.apps.util.html import render
from energyuse.apps.concepts.models import Concept
from energyuse.apps.consumption.forms import ManualEnergyConsumptionForm
from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, ListView, FormView, UpdateView

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, ButtonHolder, Div
from biostar.apps.users import auth
from energyuse.apps.consumption.models import ManualEnergyConsumption
from energyuse.apps.eusers.models import User, EnergyConsumption
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.shortcuts import render
from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, ListView, FormView, UpdateView
import mechanize
from django.contrib.auth import get_user_model


class EditManualEnergyConsumption(LoginRequiredMixin, FormView):
    form_class = ManualEnergyConsumptionForm
    template_name = 'consumption_edit.html'
    success_url = '/c'

    # Sending user object to the form, to verify which fields to display/remove (depending on group)
    # def get_form_kwargs(self):
    #     kwargs = super(EditManualEnergyConsumption, self).get_form_kwargs()
    #     kwargs['request'] = self.request
    #     return kwargs

    # def get_form_kwargs(self):
    #     kwargs = super(EditManualEnergyConsumption, self).get_form_kwargs()
    #     kwargs.update({
    #         'request': self.request
    #     })
    #     return kwargs


    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)

        context['form'] = form
        return self.render_to_response(context)

    def post(self, request=None, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        form = self.form_class(request.POST, user=request.user)
        if form.is_valid():
            f = form.cleaned_data
            consumption = ManualEnergyConsumption(concept=f['concept'], consumption=f['consumption'], user=request.user)
            consumption.save()

            messages.success(request, "Reading added successfully")
            #return HttpResponseRedirect(self.get_success_url())

            #print request.META.HTTP_REFERER
            #return HttpResponseRedirect(self.success_url)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', self.success_url))

        # There is an error in the form.
        return render(request, self.template_name, {'form': form})
