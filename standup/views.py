from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from .models import StandupEntry
from .forms import StandupForm, RegisterForm


@login_required
def feed(request):
    """Main page: standup feed + submission form."""
    already_posted = StandupEntry.user_posted_today(request.user)
    form = StandupForm()
    entries = StandupEntry.todays_entries()
    total_team = User.objects.filter(is_active=True).count()
    posted_count = entries.count()

    context = {
        'entries': entries,
        'form': form,
        'already_posted': already_posted,
        'today': timezone.now().date(),
        'total_team': total_team,
        'posted_count': posted_count,
    }
    return render(request, 'feed.html', context)


@login_required
def post_standup(request):
    """Handle standup form submission — returns HTMX partial."""
    if request.method != 'POST':
        return redirect('feed')

    if StandupEntry.user_posted_today(request.user):
        return HttpResponse('<p class="already-msg">You already posted today!</p>')

    form = StandupForm(request.POST)
    if form.is_valid():
        entry = form.save(commit=False)
        entry.user = request.user
        entry.save()
        # Return updated feed partial for HTMX to swap in
        entries = StandupEntry.todays_entries()
        return render(request, 'partials/feed_list.html', {
            'entries': entries,
            'already_posted': True,
            'posted_count': entries.count(),
        })

    # Return form with errors
    return render(request, 'partials/form_partial.html', {'form': form})


@login_required
def feed_partial(request):
    """Polled by HTMX every 30s to refresh the feed."""
    entries = StandupEntry.todays_entries()
    return render(request, 'partials/feed_list.html', {
        'entries': entries,
        'already_posted': StandupEntry.user_posted_today(request.user),
        'posted_count': entries.count(),
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('feed')

    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data.get('email', ''),
                password=form.cleaned_data['password'],
            )
            login(request, user)
            return redirect('feed')

    return render(request, 'register.html', {'form': form})
