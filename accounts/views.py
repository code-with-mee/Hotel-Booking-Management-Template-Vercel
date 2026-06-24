from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Registration successful! Please log in with your new account.'
            )
            return redirect('login')
        else:
            messages.error(
                request,
                'Registration failed. Please fix the errors below and try again.'
            )
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {
        'form': form
    })


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')
