from django import forms


class AddRoomForm(forms.Form):
    def widget_common():
        return forms.TextInput(
            attrs={'class': 'form-control'}
        )

    name = forms.CharField(
        max_length=255,
        label='Name',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ))
    description = forms.CharField(max_length=3000,  label='Description',
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': '4'}
        ))
    subject = forms.CharField(max_length=255, required=False, label='subject',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ))
    room_place = forms.CharField(max_length=255, required=False, label='Room',
        widget=widget_common())