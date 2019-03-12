from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message"]

    def save(self, commit=True):
        instance = super(ContactForm, self).save(commit=False)
        # Mail yourself the contact data here.
        if commit:
            instance.save()
        return instance
