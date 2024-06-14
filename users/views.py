from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

def register(request):                                             #create an html form
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username}, your account is created! Now, you can login to the page.')
            return redirect('login')                           #redirect the user to blog's home page
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required                     #will make sure that users must be logged in to view the profile
def profile(request):
    return render(request, 'users/profile.html')