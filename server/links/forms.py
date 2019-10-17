from urllib.parse import urlparse

from django import forms
from django.utils.translation import ugettext_lazy as _
from links.models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=150,
        label=_("title *"),
        widget=forms.TextInput(attrs={"class": "ba b--moon-gray h2"}),
    )
    url = forms.URLField(
        label=_("url"),
        widget=forms.TextInput(attrs={"class": "input-reset ba b--moon-gray h2"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        self.fields["content"] = forms.CharField(
            label=_("text"),
            widget=forms.Textarea(attrs={"rows": "3", "cols": 30, "class": "ba b--moon-gray h3"}),
            required=False,
            max_length=1000,
        )

    class Meta:
        model = Post
        fields = ("title", "url", "content")

    def clean_url(self):
        url = self.cleaned_data.get("url", "")
        if url:
            domain = urlparse(url).netloc
            if domain in self.request.site.detail.banned_domain_list:
                raise forms.ValidationError(
                    f"Links from '{domain}' are not allowed for submission."
                )
        return url


class ReplyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        self.fields["content"] = forms.CharField(
            label=_("text"),
            widget=forms.Textarea(
                attrs={"rows": "3", "class": "ba b--moon-gray h3", "style": "width: 100%"}
            ),
            required=True,
            max_length=1000,
            disabled=not self.request.user.is_authenticated,
        )

    class Meta:
        model = Post
        fields = ("content",)
