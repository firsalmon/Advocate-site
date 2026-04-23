# mainsite/forms.py
import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Lead

class LeadForm(forms.ModelForm):
    # Ловушка для ботов (оставляем)
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'style': 'position:absolute;left:-9999px;opacity:0;',
            'autocomplete': 'off', 'tabindex': '-1'
        })
    )

    class Meta:
        model = Lead
        fields = ["name", "phone", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Ваше ФИО",
                "class": "w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 outline-none",
                "autocomplete": "name"
            }),
            "phone": forms.TextInput(attrs={
                "placeholder": "+7 (999) 123-45-67",
                "class": "w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 outline-none",
                "inputmode": "tel",           
                "pattern": "\\+?[0-9\\s\\-\\(\\)]{10,18}",
                "autocomplete": "tel"
            }),
            "message": forms.Textarea(attrs={
                "placeholder": "Краткое описание дела",
                "rows": 3,
                "class": "w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 outline-none"
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        digits = re.sub(r'\D', '', phone)  # Оставляем только цифры

        if len(digits) not in (10, 11):
            raise ValidationError('Введите корректный номер (10 или 11 цифр).')
        
        # Нормализация к +7
        if len(digits) == 11:
            if digits[0] == '8':
                digits = '7' + digits[1:]
            elif digits[0] != '7':
                raise ValidationError('Номер должен начинаться с +7 или 8.')
        elif len(digits) == 10:
            digits = '7' + digits

        return f"+{digits}"  # В БД сохранится как +79991234567