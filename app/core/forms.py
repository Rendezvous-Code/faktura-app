from django import forms
from core import models


class CustomUserProfileModelAdminForm(forms.ModelForm):
    """
    Replacement for default Django admin form for the UserProfile model
    """
    class Meta:
        model = models.UserProfile
        fields = '__all__'

    def clean(self):
        """
        Checks that 'Group permission' related for the account are unique.
        """

        chosen_groups = self.cleaned_data.get('group_permisions')
        account_groups = list(filter(lambda x: x.name.startswith('account-'),
                                     chosen_groups))

        if len(account_groups) > 1:
            raise forms.ValidationError(
                "Error in chosen group permissions! \
                    Only one account group allowed.")
        return self.cleaned_data
