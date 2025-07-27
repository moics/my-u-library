from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
import json

from .models import User, Book, BookInstance, Checkout
from .forms import UserRegistrationForm, BookForm, CheckoutRequestForm, ReturnBookForm, LoginForm

# --- Helper Functions for API Responses ---

def api_response(data, status=200, error=None):
    """
    Standardized API response format.
    """
    response = {'data': data, 'error': error}
    return JsonResponse(response, status=status)

def serialize_user(user):
    """Serializes a User object."""
    return {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'role': user.role,
        'is_active': user.is_active,
        'date_joined': user.date_joined.isoformat(),
    }

def serialize_book(book):
    """Serializes a Book object."""
    return {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'published_year': book.published_year,
        'genre': book.genre,
    }

def serialize_book_instance(instance):
    """Serializes a BookInstance object."""
    return {
        'id': instance.id,
        'book_id': instance.book.id,
        'book_title': instance.book.title,
        'unique_id': instance.unique_id,
        'available': instance.available,
    }

def serialize_checkout(checkout):
    """Serializes a Checkout object."""
    return {
        'id': checkout.id,
        'student_id': checkout.student.id,
        'student_username': checkout.student.username,
        'book_instance_id': checkout.book_instance.id,
        'book_title': checkout.book_instance.book.title,
        'book_instance_unique_id': checkout.book_instance.unique_id,
        'checkout_date': checkout.checkout_date.isoformat(),
        'return_date': checkout.return_date.isoformat() if checkout.return_date else None,
        'returned': checkout.returned,
    }

# --- Mixins for API Role-Based Access Control ---

class APIAuthMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return api_response(None, status=401, error="Authentication required.")
        return super().dispatch(request, *args, **kwargs)

class APILibrarianRequiredMixin(APIAuthMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != User.LIBRARIAN:
            return api_response(None, status=403, error="Permission denied. Librarian role required.")
        return super().dispatch(request, *args, **kwargs)

class APIStudentRequiredMixin(APIAuthMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != User.STUDENT:
            return api_response(None, status=403, error="Permission denied. Student role required.")
        return super().dispatch(request, *args, **kwargs)

# --- API Authentication Views ---

@method_decorator(csrf_exempt, name='dispatch')
class APILoginView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            form = LoginForm(request, data=data)
            
            username = data['username']
            password = data['password']
            user = authenticate(request, username=username, password=password)
            print("esta es la datas", password)
            if user is not None:
                login(request, user)
                return api_response({'message': 'Login successful', 'user': serialize_user(user)}, status=200)
            else:
                return api_response(None, status=400, error="Invalid credentials.")
            
        except json.JSONDecodeError:
            return api_response(None, status=400, error="Invalid JSON.")
        except Exception as e:
            return api_response(None, status=500, error=str(e))

@method_decorator(csrf_exempt, name='dispatch')
class APILogoutView(APIAuthMixin):

    def post(self, request):
        logout(request)
        return api_response({'message': 'Logout successful'}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class APIRegisterUserView(APILibrarianRequiredMixin):

    def post(self, request):
        try:
            data = json.loads(request.body)
            form = UserRegistrationForm(data)
            if form.is_valid():
                user = form.save()
                return api_response({'message': 'User registered successfully', 'user': serialize_user(user)}, status=201)
            else:
                return api_response(None, status=400, error=form.errors)
        except json.JSONDecodeError:
            return api_response(None, status=400, error="Invalid JSON.")
        except Exception as e:
            return api_response(None, status=500, error=str(e))

# --- API Book Views ---

@method_decorator(csrf_exempt, name='dispatch')
class APIBookListView(APIAuthMixin):
    
    def get(self, request):
        books = Book.objects.all()
        # Add available copies count for each book
        books_data = []
        for book in books:
            book_data = serialize_book(book)
            book_data['available_copies'] = book.instances.filter(available=True).count()
            books_data.append(book_data)
        return api_response(books_data)

    def post(self, request):
        if request.user.role != User.LIBRARIAN:
            return api_response(None, status=403, error="Permission denied. Librarian role required to add books.")
        try:
            data = json.loads(request.body)
            form = BookForm(data)
            if form.is_valid():
                book = form.save()
                # Create one BookInstance automatically
                BookInstance.objects.create(book=book, unique_id=f"{book.title[:5]}-{book.id}-{timezone.now().strftime('%f')}")
                return api_response({'message': 'Book added successfully', 'book': serialize_book(book)}, status=201)
            else:
                return api_response(None, status=400, error=form.errors)
        except json.JSONDecodeError:
            return api_response(None, status=400, error="Invalid JSON.")
        except Exception as e:
            return api_response(None, status=500, error=str(e))

@method_decorator(csrf_exempt, name='dispatch')
class APIBookDetailView(APIAuthMixin):
    
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book_data = serialize_book(book)
        book_data['instances'] = [serialize_book_instance(inst) for inst in book.instances.all()]
        book_data['available_copies'] = book.instances.filter(available=True).count()
        return api_response(book_data)

    def put(self, request, pk):
        if request.user.role != User.LIBRARIAN:
            return api_response(None, status=403, error="Permission denied. Librarian role required to update books.")
        book = get_object_or_404(Book, pk=pk)
        try:
            data = json.loads(request.body)
            form = BookForm(data, instance=book)
            if form.is_valid():
                book = form.save()
                return api_response({'message': 'Book updated successfully', 'book': serialize_book(book)}, status=200)
            else:
                return api_response(None, status=400, error=form.errors)
        except json.JSONDecodeError:
            return api_response(None, status=400, error="Invalid JSON.")
        except Exception as e:
            return api_response(None, status=500, error=str(e))

    def delete(self, request, pk):
        if request.user.role != User.LIBRARIAN:
            return api_response(None, status=403, error="Permission denied. Librarian role required to delete books.")
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return api_response({'message': 'Book deleted successfully'}, status=204) # No Content

