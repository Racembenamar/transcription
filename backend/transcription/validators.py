# validators.py

import re
from django.core.exceptions import ValidationError
from .models import CharacterSet

def validate_transcription(value):
    # Get the allowed character set from the database
    character_set = CharacterSet.get_default_characters().characters

    # Check if all characters in the value are in the character set
    if not all(char in character_set or char.isspace() for char in value):
        raise ValidationError('Invalid characters in transcription.')

    # Check that capital letters are only used appropriately
    if not re.match(r'^([A-Z][a-zàâçéèêëîïôûù]+|\b[A-Z]+\b)(\s[A-Z]?[a-zàâçéèêëîïôûù]+)*$', value):
        raise ValidationError('Invalid use of capital letters.')

    # Check that there is at most one space between words
    if '  ' in value:
        raise ValidationError('Multiple consecutive spaces are not allowed.')

    # Check that punctuation is followed by a space and an uppercase letter, or is the end of text
    if re.search(r'[\?\.!](?![\s$])', value):
        raise ValidationError('Punctuation must be followed by a space or be at the end of the text.')

    # Check that commas, semicolons, colons are followed by a space or are the end of text
    if re.search(r'[,;:](?![\s$])', value):
        raise ValidationError('Commas, semicolons, and colons must be followed by a space or be at the end of the text.')

    return value
