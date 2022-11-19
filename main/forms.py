from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password= forms.CharField(label="phone", widget=forms.TextInput(
        attrs={'class': "from-input", "placeholder": "Введите пароль"}))
    password_2 = forms.CharField(label="phone", widget=forms.TextInput(
        attrs={'class': "from-input", "placeholder": "Повторите пароль"}))

    def clean_not_password(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('email')
        passport_ID = cleaned_data.get('passport_ID')
        passport_Series = cleaned_data.get('passport_Series')

        qs = User.objects.filter(phone=phone, passport_ID=passport_ID, passport_Series=passport_Series)
        if qs.exists():
            raise forms.ValidationError("phone is taken")
        return cleaned_data

    def clean_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "The passwords must be similar")
        return cleaned_data

    class Meta:
        model = User
        fields = ['phone', 'passport_ID', 'passport_Series']


class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(label="phone", widget=forms.TextInput(
        attrs={'class': "from-input", "placeholder": "Введите пароль"}))
    password_2 = forms.CharField(label="phone", widget=forms.TextInput(
        attrs={'class': "from-input", "placeholder": "Повторите пароль"}))

    class Meta:
        model = User
        fields = ['phone', 'passport_ID', 'passport_Series',
                  "approved", "banned"]

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['phone', 'passport_ID', 'passport_Series',
                  "approved", "banned", 'password',
                  'is_active', 'admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
