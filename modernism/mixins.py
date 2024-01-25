from django.core.exceptions import ValidationError

from modernism.tools import validate_and_clean_content_markup


class ContentMarkupMixin:
    def clean_description(self):
        description = self.cleaned_data.get("description")
        was_clean, cleaned_content_data = validate_and_clean_content_markup(description)

        if not was_clean:
            copied_form_data = self.data.copy()
            copied_form_data["description"] = cleaned_content_data
            self.data = copied_form_data
            raise ValidationError(
                f"Your text markup needed to be cleaned. Please review, correct if necessary and save again."
            )

        return description

    def clean_history(self):
        history_content = self.cleaned_data.get("history")
        clean, cleaned_content_data = validate_and_clean_content_markup(history_content)

        if not clean:
            # Solved in this unconventional way to provide the cleaned data to the user for review
            copied_form_data = self.data.copy()
            copied_form_data["history"] = cleaned_content_data
            self.data = copied_form_data
            raise ValidationError(
                f"Your text markup needed to be cleaned. Please review, correct if necessary and save again."
            )

        return history_content
