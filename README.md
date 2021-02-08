# Projects of CS50W: Web Programming with Python and Javascript

## Project 0: Search

Project 0 is a Google frontend clone. It has three html pages corresponding to
Google's primary search page, image search page and advanced search page. CSS
is used to style pages to look somewhat like Google's corresponding pages.
Forms use the real Google search as the action attribute. So the inputted
search queries are redirected to Google search.

## Project 1: Wiki

Project 1 is an encyclopedia site. It uses django to show wikipages that are
stored directly to server's disk as Markdown files. Markdown is converted to
HTML before it is shown to the user. User's of the site can add new wikipages
by submitting content of the wikipage as Markdown in the create new wikipage
page. User's can also edit pages that are already saved. There is also options
to search for wikipages and a button that gives a random wikipage every time
it is clicked.

## Project 2: Commerce

Project 2 is a commerce site for user's to keep auctions in which other user's
can bid for the item. It uses django to store listings of items in the database.
Django is also used to serve HTML pages which show data about listings. User's
can create listings, add listings to watchlist, bid for listings and comment for
listings. The owner of the listing can also close the listing as the price of
the item is high enough. The site also supports Django's Admin Interface to
modify records stored in the database.