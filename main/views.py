from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Note, History
from .forms import AddPageForm


def index(request):
    user = request.user
    if user.is_authenticated:
        notes = Note.objects.filter()
    else:
        notes = []
    return render(request, "index.html", {"notes": notes})


def page(request, slug):
    note = get_object_404(Note, slug=slug)
    return render(request, "page.html", {"note": note})


def page_history(request, slug):
    note = get_object_404(Note, slug=slug)
    history_list = History.objects.filter(note=note).order_by("-added")
    return render(request, "page-history.html", {"history": history})


@login_required
def add_page(request):
    if request.method == "POST":
        form = AddPage(request.POST)
        if form.is_valid():
            inst = form.save()
            return HttpResponseRedirect(reverse("main:page", args=(inst.slug,)))
