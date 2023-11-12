import re
from django.core.exceptions import ValidationError
from .models import CharacterSet

def validate_transcription(value):
    # Get the allowed character set from the database
    character_set = CharacterSet.get_default_characters().characters

    # Check if all characters in the value are in the character set
    if not all(char in character_set or char.isspace() for char in value):
        raise ValidationError('Invalid characters in transcription.')

    # Check that capital letters are allowed only as a first word letter or if all letters in the word are uppercase
    words = value.split()
    for word in words:
        if word.isupper() or (word[0].isupper() and word[1:].islower()):
            continue
        else:
            raise ValidationError('Invalid use of capital letters.')

    # Check that there is only zero or one space between two characters
    if '  ' in value:
        raise ValidationError('Multiple consecutive spaces are not allowed.')

    # Check that characters ?.! are end of text or followed by one space and an uppercase character
    if re.search(r'[?\.!](?![\s$])', value):
        raise ValidationError('Punctuation must be followed by a space or be at the end of the text.')

    # Check that characters ,;: are end of text or followed by one space
    if re.search(r'[,;:](?![\s$])', value):
        raise ValidationError('Commas, semicolons, and colons must be followed by a space or be at the end of the text.')

    return value
