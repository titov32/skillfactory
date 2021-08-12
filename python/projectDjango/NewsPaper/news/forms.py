from django.forms import ModelForm, BooleanField, TextInput, Textarea, SelectMultiple, Select, CheckboxInput
from .models import Post


# Создаём модельную форму
class PostForm(ModelForm):
    check_box = BooleanField(label='Уверены что запись надо добавить?')  # добавляем галочку, или же true-false поле
    # в класс мета как обычно надо написать модель по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.

    class Meta:
        model = Post
        fields = ['material', 'author', 'title', 'text', 'postCategory', 'check_box']

        widgets = {
            'material': Select(attrs={
                'class': 'form-control'
            }),
            'author': Select(attrs={
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