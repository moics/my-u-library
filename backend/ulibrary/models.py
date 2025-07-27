from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone


class User(AbstractUser):
    # Choices for user roles
    STUDENT = 'student'
    LIBRARIAN = 'librarian'
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (LIBRARIAN, 'Librarian'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STUDENT)

    # Add custom related_name to avoid clashes with auth.User's default related_name
    groups = models.ManyToManyField(
        Group,
        related_name='library_users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='library_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_year = models.IntegerField()
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class BookInstance(models.Model):
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='instances')

    unique_id = models.CharField(max_length=100, unique=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.book.title} ({self.unique_id}) - {'Available' if self.available else 'Not Available'}"

class Checkout(models.Model):
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': User.STUDENT}, related_name='checkouts')
    book_instance = models.ForeignKey(BookInstance, on_delete=models.CASCADE, related_name='checkouts')
    checkout_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True, blank=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} checked out {self.book_instance.book.title}"

    class Meta:
        ordering = ['-checkout_date']