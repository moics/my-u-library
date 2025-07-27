from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Book, BookInstance, Checkout

class UserRegistrationForm(UserCreationForm):
    """
    Form for librarians to register new users (students or other librarians).
    """
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, initial=User.STUDENT)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'role',)
        # Ensure email is included if you want it to be required or displayed

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

class BookForm(forms.ModelForm):
    """
    Form for librarians to add new books.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_year', 'genre']
        widgets = {
            'published_year': forms.NumberInput(attrs={'min': 1000, 'max': 2100}), # Example validation
        }

class CheckoutRequestForm(forms.Form):
    """
    A simple form to trigger a checkout request.
    It doesn't have fields, but its submission signifies the request.
    """
    # No fields needed, just a submit button
    pass

class ReturnBookForm(forms.Form):
    """
    A simple form to trigger a book return.
    It doesn't have fields, but its submission signifies the return.
    """
    # No fields needed, just a submit button
    pass

class LoginForm(AuthenticationForm):
    """
    Custom login form to ensure it uses our custom User model.
    """
    pass
