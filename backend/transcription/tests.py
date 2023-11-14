import unittest
from transcription.validators import validate_transcription
from django.core.exceptions import ValidationError

class TestTranscriptionValidation(unittest.TestCase):

    def test_valid_transcription(self):
        self.assertEqual(validate_transcription("This is a valid transcription."), "This is a valid transcription.")

    def test_invalid_characters(self):
        with self.assertRaises(ValidationError):
            validate_transcription("Invalid charact3rs")

    def test_capital_letters(self):
        test_string = "this Is A Valid Capitalization"
        validated_string = validate_transcription(test_string)
        self.assertEqual(validated_string, test_string)

    def test_multiple_consecutive_spaces(self):
        with self.assertRaises(ValidationError):
            validate_transcription("Multiple  spaces")

    def test_punctuation_end_of_text(self):
        with self.assertRaises(ValidationError):
            validate_transcription("Incorrect punctuation?here")

    def test_punctuation_followed_by_space_and_uppercase(self):
        self.assertEqual(validate_transcription("Correct punctuation? Here it is."), "Correct punctuation? Here it is.")

    def test_commas_semicolons_colons(self):
        with self.assertRaises(ValidationError):
            validate_transcription("Incorrect,use of punctuation")

    def test_commas_semicolons_colons_correct_usage(self):
        self.assertEqual(validate_transcription("Correct, use of punctuation."), "Correct, use of punctuation.")

if __name__ == '__main__':
    unittest.main()
