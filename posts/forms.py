from django import forms

from .models import Post

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'content', 'image', 'draft', 'publish' ]


		widgets={
        'publish': forms.DateInput(attrs={"type":"date"}),
        }

