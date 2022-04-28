from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
import re

class CreateForm(UserCreationForm):
    email2 = forms.EmailField(label = '이메일 확인')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'ALIGN': 'center'})
            self.fields[field].help_text = ''
            self.fields[field].error_messages = ''
        self.fields["password1"].label = '비밀번호'
        self.fields["password2"].label = '비밀번호 재확인'
        self.fields["email"].help_text =  "인증을 위한 이메일 입니다. \n 정확한 메일 주소를 입력해 주세요"
    class Meta:
        model=User
        fields=("username","email","email2",
                "last_name","password1","password2")
        labels = {
            'username' : '아이디',
            'last_name' : '이름',
            'email' : '본인 확인 이메일',
        }




    def save(self, commit=True):
        instance = super(CreateForm,self).save(commit=False)

        if commit:
            instance.save()
        return instance

    def clean_password2(self): # 왜인지는 몰라도 비밀번호 clean()으로 하면 안 됨
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def clean(self): ## views 에서 clean 돌리고, email, username, first_name 등 다 돌리고 오류 메세지 발생 시키면 될듯
       cleaned_data = super().clean()
       email = cleaned_data.get('email')
       email2 = cleaned_data.get('email2')
       username = cleaned_data.get('username')
       if User.objects.filter(email=email).exists():
           self.add_error('email', "이미 존재하는 이메일 입니다.")
       if re.sub("[^a-zA-Z0-9]","", username) != username:
           self.add_error('username', "아이디는 숫자와 소문자 대문자의 조합으로만 가능합니다")
       if User.objects.filter(username=username).exists():
           self.add_error('username', "이미 존재하는 아이디 입니다.")
       if len(username) > 150 or len(username) < 2:
           self.add_error('username', "아이디가 너무 길거나 짧습니다.")
       if email != email2:
           self.add_error('email2', "이메일 주소가 일치하지 않습니다.")

       return cleaned_data

