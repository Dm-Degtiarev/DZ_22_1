from django import forms
from catalog.models import Product, ProductVersion
from catalog.utils import len_text_matching


class ProductForm(forms.ModelForm):
    stop_list = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Product
        fields = ('product_name', 'product_info', 'product_image', 'product_price', 'product_category', )
        # exclude = ('', ...) # перечисляем поля которые не хотим отображать
        # fields = '__all__'  # выбираем все поля

    def clean_product_name(self):
        cleaned_data = self.cleaned_data['product_name']

        if len_text_matching(cleaned_data, self.stop_list):
            raise forms.ValidationError(f"Наименование не должно содержать слов: {', '.join(self.stop_list)}")

        return cleaned_data


class ProductVersionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ProductVersion
        fields = '__all__'


