from django import forms

from .models import Event, Participant


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('event', 'name', 'email', 'transaction_id', 'receipt', 'photo')
        widgets = {'event': forms.Select(attrs={'class': 'form-control'})}

    def clean_transaction_id(self):
        value = self.cleaned_data['transaction_id'].strip()
        if Participant.objects.filter(transaction_id=value).exists():
            raise forms.ValidationError('This transaction ID is already registered.')
        return value


class MarksForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('marks',)
        widgets = {'marks': forms.NumberInput(attrs={'min': 0, 'max': 100})}


class FeedbackForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), label='Comment')

    class Meta:
        model = Participant
        fields = ('rating',)
        widgets = {'rating': forms.NumberInput(attrs={'min': 1, 'max': 5})}

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if not 1 <= rating <= 5:
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return rating


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'event_date', 'description')
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
