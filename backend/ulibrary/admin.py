
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Book, BookInstance, Checkout

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')

# Register other models
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_year', 'genre')
    search_fields = ('title', 'author', 'genre')

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'unique_id', 'available')
    list_filter = ('available', 'book__genre') 
    search_fields = ('unique_id', 'book__title', 'book__author')

@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('student', 'book_instance', 'checkout_date', 'return_date', 'returned')
    list_filter = ('returned', 'checkout_date', 'student__username')
    search_fields = ('student__username', 'book_instance__book__title', 'book_instance__unique_id')
    raw_id_fields = ('student', 'book_instance')