from django import forms
from .models import Home, Post, Comment

class HomeForm(forms.ModelForm):

    class Meta:
        model = Home
        fields = ('logo','main_banner','sub_banner1','sub_banner2','description',)

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

