from django.core.exceptions import ValidationError

from modernism.tools import validate_and_clean_content_markup


class ContentMarkupMixin:
    def _clean_content_markup_field(self, field_name):
        content_data = self.cleaned_data.get(field_name)
        clean, cleaned_content_data = validate_and_clean_content_markup(content_data)

        if not clean:
            # Solved in this unconventional way to provide the cleaned data to the user for review
            copied_form_data = self.data.copy()
            copied_form_data[field_name] = cleaned_content_data
            self.data = copied_form_data
            raise ValidationError(
                f"Your text markup in {field_name} needed to be cleaned. Please review, correct if necessary, and save again."
            )

        return content_data

    def clean_description(self):
        return self._clean_content_markup_field("description")

    def clean_history(self):
        return self._clean_content_markup_field("history")
