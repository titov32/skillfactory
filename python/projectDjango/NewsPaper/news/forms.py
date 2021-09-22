from django.forms import ModelForm, BooleanField, TextInput, Textarea, SelectMultiple, Select, CheckboxInput
from .models import Post


# Создаём модельную форму
class PostForm(ModelForm):
    check_box = BooleanField(label='Уверены что запись надо добавить?')  # добавляем галочку, или же true-false поле

    class Meta:



        model = Post
        fields = ['material',  'title', 'text', 'postCategory', 'check_box']

#'created_by',


        widgets = {
            'material': Select(attrs={
                'class': 'form-control'
            }),
            'created_by': Select(attrs={
                'class': 'form-control'
            }),
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'заголовок статьи'
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'текст статьи'
            }),
            'postCategory': SelectMultiple(attrs={
                'class': 'form-control'
            }),
            'check_box': CheckboxInput(attrs={
                'class': 'form-control'
            }),
        }