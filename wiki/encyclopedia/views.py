from django.shortcuts import render, redirect
from django.http import Http404
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

    
