# C:\crypto\cryptobitcoin\agents\templatetags\path_utils.py
import os
from django import template

register = template.Library()

@register.filter
def basename(value):
    """Return the file name from a full path (e.g. 'media/files/data.csv' → 'data.csv')"""
    return os.path.basename(value)