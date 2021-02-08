from django.forms import ModelForm, CheckboxSelectMultiple

from .models import Listing, Bid, Comment

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "image_url",
            "description",
            "starting_bid",
            "categories"
        ]


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = [
            "value"
        ]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content"
        ]
