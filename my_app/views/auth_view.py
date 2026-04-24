from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

def register_view(request):
    errors = {}
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        
        if not first_name:
            errors['first_name'] = 'First name is required.'
        if not last_name:
            errors['last_name'] = 'Last name is required.'
            
        username = f"{first_name}{last_name}1".lower()
        
        if User.objects.filter(username=username).exists():
            username = f"{first_name}{last_name}2".lower()
            if User.objects.filter(username=username).exists():
                username = f"{first_name}{last_name}3".lower()
                if User.objects.filter(username=username).exists():
                    username = f"{first_name}{last_name}4".lower()
                    
        password = '12345678'
            
        if not errors:
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()
            messages.success(request, f'Account created successfully! Your username is {username} and your password is {password}. Please log in to continue.')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been logged in successfully!')
                return redirect('home')
            
            messages.error(request, 'There was an error logging you in. Please try logging in manually.')
            return redirect('login')
        
        return render(request, 'auth/register_page.html', {'errors': errors, 'data': request.POST})

    return render(request, 'auth/register_page.html', {'data': request.POST})

def login_view(request):
    errors = {}
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = '12345678'
        
        if not username:
            errors['username'] = 'Username is required.'
        elif not User.objects.filter(username=username).exists():
            errors['username'] = 'Invalid username. Please check your username and try again.'
        
        if not errors:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been logged in successfully!')
                return redirect('home')
            else:
                errors['username'] = 'Invalid username or password. Please check your credentials and try again.'
        
        return render(request, 'auth/login_page.html', {'errors': errors, 'data': request.POST}) 

    return render(request, 'auth/login_page.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')