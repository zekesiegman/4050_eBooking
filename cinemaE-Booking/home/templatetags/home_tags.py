from django import template
from django.template import Library

from ..models import CardEncr

register = template.Library()

@register.simple_tag
def decrypt(s):
    fernet = CardEncr.fernet
    bites = bytes(s, 'utf-8')
    decoded = fernet.decrypt(bites).decode()
    return decoded[-4:]

register.filter('decrypt',decrypt)