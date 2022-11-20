from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm, AuthenticationForm

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Телефон", widget=forms.TextInput(
        attrs={'class': "from-input", "placeholder": "телефон"}), required=True)
    password = forms.CharField(label="пароль", widget=forms.TextInput(
        attrs={'class': "from-input", "placeholder": "Введите пароль"}), required=True)

    class Meta:
        model = User
        fields = ['phone', 'password1']


class ConvertForm(forms.Form):
    amount_from = forms.IntegerField()
    currency_from = forms.CharField(max_length=4)
    amount_to = forms.IntegerField(required=False)
    currency_to = forms.CharField(max_length=4)



class RegisterForm(UserCreationForm):
    phone = forms.CharField(label="Телефон", widget=forms.TextInput(
        attrs={'class': "form-control", "placeholder": "телефон" ,}), required=True)
    passport_ID = forms.CharField(label="Номер паспорта", widget=forms.TextInput(
        attrs={'class': "form-control", "placeholder": "серия паспорта"}), required=True)
    passport_Series = forms.CharField(label="Серия паспорта", widget=forms.TextInput(
        attrs={'class': "form-control", "placeholder": "номер паспорта"}), required=True)
    password1 = forms.CharField(label="пароль", widget=forms.TextInput(
        attrs={'class': "form-control", "placeholder": "Введите пароль"}), required=True)
    password2 = forms.CharField(label="подтверждения пароля", widget=forms.TextInput(
        attrs={'class': "form-control", "placeholder": "Повторите пароль"}), required=True)

    class Meta:
        model = User
        fields = ['phone', 'passport_ID', 'passport_Series', 'password1', 'password2']


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="пароль", widget=forms.TextInput(
        attrs={'class': "from-input", "placeholder": "Введите пароль"}))
    password2 = forms.CharField(label="повторите пароль", widget=forms.TextInput(
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
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error("password2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password1 in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password1 = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['phone', 'passport_ID', 'passport_Series',
                  "approved", "banned", 'password1',
                  'is_active', 'admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password1"]
