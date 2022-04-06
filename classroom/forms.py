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
    subject = forms.CharField(max_length=255, required=False, label='Subject',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ))
    room_place = forms.CharField(max_length=255, required=False, label='Room',
        widget=widget_common())


class AddMaterialForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        label='Title',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    description = forms.CharField(
        max_length=3000, 
        label='Description',
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': '4'}
        )
    )
    files = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={'class': 'form-control', 'multiple': True}
        ),
        required=False
    )

class AddTaskForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        label='Title',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    description = forms.CharField(
        max_length=3000, 
        label='Description',
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': '4'}
        )
    )
    due_date = forms.DateField(initial='No due date',
        label='Date',
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}
        ),
        required=False,
    )
    due_time = forms.TimeField(
        label='Time',
        widget=forms.TimeInput(
            attrs={'class': 'form-control', 'type': 'time'}
        ),
        required=False,
    )
    files = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={'class': 'form-control', 'multiple': True}
        ),
        required=False
    )
