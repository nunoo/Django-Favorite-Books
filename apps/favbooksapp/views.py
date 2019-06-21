from django.shortcuts import render, HttpResponse, redirect
from .models import User, Book
from django.contrib import messages
import bcrypt
import datetime
import re

#----------------------------------------------------------------------------
# Route to render Login Reg page
#----------------------------------------------------------------------------

def index(request):
    return render(request, 'favbooksapp/index.html')

#----------------------------------------------------------------------------
# Route to render Home page
#----------------------------------------------------------------------------


def books(request):
    if not request.session['isloggedin']:
        return redirect('/')
    else:
        context = {
            'all_books': Book.objects.all(),
        }
        return render(request, 'favbooksapp/add_books.html', context)

#----------------------------------------------------------------------------
# Route to add book and validate
#----------------------------------------------------------------------------


def addbook(request):
    errors = Book.objects.basic_validator_add(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            return redirect('/books')
    else:        
        DBtitle = request.POST['form_add_title']
        DBdesc = request.POST['form_add_description']
        uploaded_by_id = request.session['userid']
        uploaded_by = User.objects.get(id=uploaded_by_id)
        new_book = Book.objects.create(
            DBtitle=DBtitle, DBdesc=DBdesc, uploaded_by=uploaded_by)
        new_book.users_who_like.add(uploaded_by)
        return redirect('/books')

#----------------------------------------------------------------------------
# Route to edit book and validate
#----------------------------------------------------------------------------


def edit_book(request, bookid):
    errors = Book.objects.basic_validator_edit(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            return redirect('/books/'+str(bookid))

    else:

        current_book = Book.objects.get(id=bookid)
        new_title = request.POST['form_edit_title']
        new_desc = request.POST['form_edit_description']
        current_book.DBtitle = new_title
        current_book.DBdesc = new_desc
        current_book.save()

        return redirect('/books/'+str(bookid))

#----------------------------------------------------------------------------
# Route to delete book and validate
#----------------------------------------------------------------------------


def delete_book(request, bookid):
    
    current_book = Book.objects.get(id=bookid)
    book_creator_id = current_book.uploaded_by_id
    if (request.session['userid'] == book_creator_id):
        current_book.delete()
        return redirect('/books')
    else:
        return redirect('/')


#----------------------------------------------------------------------------
# Route to show book info (if user created show edit page else show view page)
#----------------------------------------------------------------------------


def book_click(request, bookid):
    current_book = Book.objects.get(id=bookid)
    book_creator_id = current_book.uploaded_by_id
    if (request.session['userid'] == book_creator_id):
        context = {
            'book': current_book,
            'users': current_book.users_who_like.all()
        }
        return render(request, 'favbooksapp/edit_books.html', context)
    else:
        context = {
            'book': current_book,
            'users': current_book.users_who_like.all()
        }
        return render(request, 'favbooksapp/view_books.html', context)

#----------------------------------------------------------------------------
# Route to like and unlike book
#----------------------------------------------------------------------------


def like_book(request, bookid):
    current_book = Book.objects.get(id=bookid)
    current_user = User.objects.get(id=request.session['userid'])
    current_book.users_who_like.add(current_user)
    return redirect('/books/'+str(bookid))


def unlike_book(request, bookid):
    current_book = Book.objects.get(id=bookid)
    current_user = User.objects.get(id=request.session['userid'])
    current_book.users_who_like.remove(current_user)
    return redirect('/books/'+str(bookid))

# ----------------------------------------------------------------------------
# Route to validate, register user and redirect to home page
# ----------------------------------------------------------------------------

def addUserToDB(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        messages.error(request, request.POST["first_name"], "holdFName")
        messages.error(request, request.POST["last_name"], "holdLName")
        messages.error(request, request.POST["email"], "holdEmail")
        return redirect('/')
    else:
        DBfirst_name = request.POST["first_name"]
        DBlast_name = request.POST["last_name"]
        DBemail = request.POST["email"]
        pw_to_hash = request.POST["password"]
        DBpassword = bcrypt.hashpw(pw_to_hash.encode(), bcrypt.gensalt())
        DBpassword = DBpassword.decode()
        new_user = User.objects.create(
            DBfirst_name=DBfirst_name, DBlast_name=DBlast_name, DBemail=DBemail, DBpassword=DBpassword)
        request.session['userid'] = new_user.id
        request.session['first_name'] = new_user.DBfirst_name
        request.session['isloggedin'] = True
        request.session.modified = True
        return redirect("/books")

# ----------------------------------------------------------------------------
# Route to login and route to home page
# ----------------------------------------------------------------------------

def loginUserToDB(request):
    if len(request.POST['emailLogin']) == 0:
            
        return redirect('/')
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        messages.error(request, request.POST["emailLogin"], "holdLoginEmail")
        return redirect('/')
    else:
        current_user = User.objects.get(DBemail=request.POST['emailLogin'])
        request.session['userid'] = current_user.id
        request.session['isloggedin'] = True
        request.session['first_name'] = current_user.DBfirst_name
        return redirect("/books")

# ----------------------------------------------------------------------------
# Route to logout user
# ----------------------------------------------------------------------------

def logout(request):
    request.session.clear()
    request.session['isloggedin'] = False
    return redirect('/')
