#coding:utf8
from django import forms
from datetime import datetime


class PaymentCommandForm(forms.Form):

    COMMAND_CHOICES = (
        ('check', 'check'),
        ('pay', 'pay'),
    )

    command = forms.ChoiceField(choices=COMMAND_CHOICES)
    account = forms.IntegerField()


class UpdatePaymentForm(forms.Form):

    txn_id = forms.CharField()
    txn_date = forms.CharField()
    sum = forms.FloatField(min_value=0.001)

    def clean_txn_date(self):
        txn_date = self.cleaned_data.get('txn_date')
        if txn_date:
            txn_date = datetime.strptime(txn_date, "%Y%m%d%H%M%S")
        return txn_date
