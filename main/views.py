from difflib import HtmlDiff

from django.shortcuts import render

from .models import Note, History


def index(request):
    notes = Note.objects.filter()
    return render(request, "index.html", {"notes": notes})


def page(request, slug):
    note = get_object_404(Note, slug=slug)
    return render(request, "page.html", {"note": note})


def page_history(request, slug):
    note = get_object_404(Note, slug=slug)
    history_list = History.objects.filter(note=note).order_by("-added")
    return render(request, "page-history.html", {"history": history})
