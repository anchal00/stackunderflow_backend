from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from stack_underflow_app.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = '__all__'
