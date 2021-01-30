from django.shortcuts import render, redirect
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django import forms

from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wikipage(request, title):
    page_markdown = util.get_entry(title)

    if not page_markdown:
        raise Http404(f'Wikipage for title "{title}" was not found')

    return render(request, "encyclopedia/wikipage.html", {
        "html": markdown(util.get_entry(title)),
        "title": title
    })


def search(request):
    query = request.GET["q"]

    if util.get_entry(query):
        return redirect(wikipage, query)
    
    entries = filter(lambda entry : query in entry, util.list_entries())

    return render(request, "encyclopedia/search.html", {
        "entries": entries
    })

class WikipageForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)


def new(request):
    if request.method == "POST":
        form = WikipageForm(request.POST)

        if not form.is_valid():
            return render(request, "encyclopedia/new.html", {
                form
            })

        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]

        if title in util.list_entries():
            raise PermissionDenied(f'Wikipage for title "{title}" already exists')
        
        util.save_entry(title, content)
        return redirect(wikipage, title)
    
    return render(request, "encyclopedia/new.html", {
        "form": WikipageForm()
    })
