from django import forms
from .models import Topic, Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )
    # where is the field for subject? How does subject field work without defining here??? 
    # Why is there only message here???
    
    class Meta:
        model = Topic
        fields = ['subject', 'message']