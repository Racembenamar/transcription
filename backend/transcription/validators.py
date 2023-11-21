import re
from django.core.exceptions import ValidationError
from .models import CharacterSet

def validate_transcription(value):
    # Reject inputs that are only spaces or specified punctuation
    if re.fullmatch(r'[\s.,;:?!]*', value):
        raise ValidationError('Transcription cannot be just punctuation or spaces.')

    # Get the allowed character set from the database
    character_set = CharacterSet.get_default_characters().characters

    # Check if all characters in the value are in the character set
    if not all(char in character_set or char.isspace() for char in value):
        raise ValidationError('Invalid characters in transcription.')

    # Capital letters validation
    words = value.split()
    for word in words:
        # Word should be all uppercase, all lowercase, or start with an uppercase followed by all lowercase
        if not (word.isupper() or word.islower() or (word[0].isupper() and word[1:].islower())):
            raise ValidationError('Invalid use of capital letters.')

    # Only zero or one space between two characters
    if '  ' in value:
        raise ValidationError('Multiple consecutive spaces are not allowed.')

    # Characters ?.! should be at end of text or followed by one space and an uppercase character
    if re.search(r'[?\.!](?![\s$][A-Z])', value) and not re.search(r'[?\.!]$', value):
        raise ValidationError('Punctuation ?.! must be followed by a space and an uppercase character or be at the end of the text.')

    # Characters ,;: should be at end of text or followed by one space
    if re.search(r'[,;:](?!\s)', value) and not re.search(r'[,;:]$', value):
        raise ValidationError('Commas, semicolons, and colons must be followed by a space or be at the end of the text.')

    return value
