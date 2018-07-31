from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self._init_field_attrs()

    def _init_field_attrs(self):
        for field in (self.fields.keys()):
            field_attrs                = self.fields[field].widget.attrs
            field_attrs['class']       = 'form-control'
            field_attrs['placeholder'] = self.fields[field].label

