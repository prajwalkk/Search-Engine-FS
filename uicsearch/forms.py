from django import forms


class SearchForm(forms.Form):
    choices = (('10', 'Ten'),
               ('20', 'Twenty'),
               ('30', 'Thirty'))
    choices_2 = (('1', 'PageRank'),
                 ('2', 'CosSim'))
    result_size = forms.ChoiceField(widget=forms.Select(
                                    attrs={'class': 'custom-select'}),
                                    choices=choices)
    eval_func = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'custom-select'}),
        choices=choices_2)
    query = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mr-sm-2',
               'type': 'search',
               'placeholder': 'Search',
               'aria-label': 'Search'
               }
    )
    )
