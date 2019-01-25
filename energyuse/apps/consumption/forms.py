from datetime import date, datetime
from django import forms

from energyuse.apps.concepts.models import Concept
from energyuse.apps.consumption.models import ManualEnergyConsumption

class ManualEnergyConsumptionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(ManualEnergyConsumptionForm, self).__init__(*args, **kwargs)
        self.fields['concept'].queryset = Concept.objects.filter(appliance=True)


    class Meta:
        model = ManualEnergyConsumption
        fields = ['concept', 'consumption']

        help_texts = {
            'concept': 'The appliance or concept that is measured.',
            'consumption': 'The energy consumption measured in kWh.'
        }

        labels = {
            'concept': 'Appliance',
            'consumption': 'Energy Consumption in kWh'
        }

    def clean(self):
        cleaned_data = super(ManualEnergyConsumptionForm, self).clean()
        concept = cleaned_data.get("concept")

        #Check if there is an reading already submited for today and the given appliance for the user:
        today = date.today()
        print self.user

        sc = ManualEnergyConsumption.objects.filter(creation_date__contains=today, concept=concept, user=self.user)
        if sc.count() > 0:
            raise forms.ValidationError(
                        "You can only submit one reading per day for a given appliance.")

