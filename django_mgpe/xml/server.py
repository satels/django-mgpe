#coding:utf8
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.utils.importlib import import_module
from django_mgpe.xml.conf import MGPE_APP
from django_mgpe.xml.forms import PaymentCommandForm, UpdatePaymentForm
from django_mgpe.xml.utils import get_check_result_as_xml, prepare_comment


def get_mgpe_app():
    mgpe_app = MGPE_APP
    if mgpe_app not in settings.INSTALLED_APPS:
        raise ImproperlyConfigured(
            u"MGPE_APP (%r) должен быть установлен в INSTALLED_APPS" % mgpe_app
        )
    try:
        package = import_module(mgpe_app)
    except ImportError:
        raise ImproperlyConfigured(
            u"MGPE_APP ссылается на несуществующий пакет."
        )
    return package


def mgpe(request):
    command_form = PaymentCommandForm(request.GET)
    if command_form.is_valid():
        command = command_form.cleaned_data['command']
        account = command_form.cleaned_data['account']
        if command == 'check':
            return HttpResponse(_check_payment(account), mimetype='text/xml')
        elif command == 'pay':
            update_payment_form = UpdatePaymentForm(request.GET)
            if update_payment_form.is_valid():
                txn_id = update_payment_form.cleaned_data['txn_id']
                txn_date = update_payment_form.cleaned_data['txn_date']
                sum = update_payment_form.cleaned_data['sum']
                text_response = _update_payment(account, txn_id, txn_date, sum)
                return HttpResponse(text_response, mimetype='text/xml')
            else:
                comment = prepare_comment(update_payment_form.errors)
                text_response = get_check_result_as_xml('300', comment=comment)
                return HttpResponse(text_response, mimetype='text/xml')
    else:
        comment = prepare_comment(command_form.errors)
        text_response = get_check_result_as_xml('300', comment=comment)
        return HttpResponse(text_response, mimetype='text/xml')


def _check_payment(account):
    mgpe_package = get_mgpe_app()
    if hasattr(mgpe_package, "check_payment"):
        return mgpe_package.check_payment(account)
    else:
        raise ImproperlyConfigured(
            u"Задайте функцию check_payment(account) в пакете MGPE_APP (%r)" % \
                MGPE_APP
        )


def _update_payment(account, txn_id, txn_date, sum):
    mgpe_package = get_mgpe_app()
    if hasattr(mgpe_package, "update_payment"):
        return mgpe_package.update_payment(account, txn_id, txn_date, sum)
    else:
        raise ImproperlyConfigured(
            u"Задайте функцию update_payment(account, txn_id, txn_date, sum) в "
            u"пакете MGPE_APP (%r)" % MGPE_APP
        )
