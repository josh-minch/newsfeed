from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import logout

from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account {username} created')
            return redirect('feed:all')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, f'Account logged out.')
    return redirect('feed:all')
