from django import forms


class AddListingItemForm(forms.Form):
    title = forms.CharField(label="Item Title")
    description = forms.CharField(label="Item Description")
    starting_bid = forms.DecimalField(decimal_places=2)

    img_url = forms.URLField(label="Image URL")
    # choices = forms.ChoiceField(widget=forms.)