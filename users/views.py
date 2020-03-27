from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout

from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, f'Account {username} created')
            new_user = authenticate(username=username,
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('feed:all')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, f"You've been logged out.")
    return redirect('feed:all')


def favorites(request):
    if not request.user.is_authenticated:
        return register(request)

    username = request.user.username
    articles = request.user.favorites.all()
    title = 'Favorites'

    context = {'wide_title': title, 'narrow_title': title, 'username': username, 'articles': articles}
    return render(request, 'users/favorites.html', context)
