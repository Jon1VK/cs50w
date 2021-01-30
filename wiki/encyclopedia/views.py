from django.shortcuts import render
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
