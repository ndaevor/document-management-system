from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Document
from .forms import DocumentForm
from django.urls import reverse


#check if the user is superuser
def superuser_check(user):
    return user.is_superuser


#home page of user
@login_required(login_url='login')
def HomePage(request):
    if superuser_check(request.user):
        messages.error(request, "Username or Password is incorrect!!!")
        return redirect('login')#(reverse('admin:index'))
    if not request.user.is_authenticated:
        return redirect('login')
    documents = Document.objects.filter(user=request.user)
    return render(request, 'home.html', {'documents': documents})


#signup page
def SignuPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            messages.error(request, "Your password and confirm password do not match!")
            return redirect('signup')
        else:
            if User.objects.filter(username=uname).exists():
                messages.error(request, "Username already exists!")
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists!")
                return redirect('signup')
            else:
                my_user = User.objects.create_user(username=uname, email=email, password=pass1)
                my_user.save()
                messages.success(request, "Account created successfully! Please log in.")
                return redirect('login')

    return render(request, 'signup.html')


#login page
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None :     
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password is incorrect!!!")

    return render(request, 'login.html')

#logout button
def LogoutPage(request):
    logout(request)
    request.session.clear()
    return redirect('login')



#uploading document
@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            return redirect('home')  
    else:
        form = DocumentForm()
    
    # Retrieve all documents for the current user
    documents = Document.objects.filter(user=request.user)
    return render(request, 'home.html', {'documents': documents, 'form': form})

#downloading document
@login_required
def document_download(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    
    if document.user == request.user:        
        return redirect(document.file.url)
    else:
        
        return redirect('home')
    
#deleting document
def delete_document(request, document_id):
    
    document = get_object_or_404(Document, id=document_id)    
   
    if document.user == request.user:
        document.delete()
    
    
    return redirect('home')


#settings 
@login_required
def settingsPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        user = request.user

        # Check if the new username already exists and is not the current user's username
        if User.objects.filter(username=username).exclude(pk=user.pk).exists():
            messages.error(request, 'Username is already taken!')
        # Check if the new email already exists and is not the current user's email
        elif User.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, 'Email is already in use!')
        # Check if passwords match, if provided
        elif password1 and password1 != password2:
            messages.error(request, 'Passwords do not match!')
        else:
            user.username = username
            user.email = email
            if password1:
                user.set_password(password1)
            user.save()
            messages.success(request, 'Your settings have been updated!')
            return render(request, 'settings.html')

    return render(request, 'settings.html')




