from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def home(request):
    # Home page (index) now uses index.html
    return render(request, 'index.html')

def tutorials(request):
    # Tutorials page uses tutorials.html
    return render(request, 'tutorials.html')

def challenge(request):
    # Challenge page uses challenge.html
    return render(request, 'challenge.html')

def community(request):
    # Community page uses community.html
    return render(request, 'community.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })
