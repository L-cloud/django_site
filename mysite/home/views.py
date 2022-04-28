from django.views import View
from django.contrib.auth.views import LoginView
from .models import Report,Fav
from django.http import FileResponse, Http404
from django.utils.encoding import force_str
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from .forms import CreateForm
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from .tasks import send_email
import json

# Create your views here.
class MainView(LoginView): # 메인화면
    template = 'home/main.html'
    def get(self, request) :
        report_objects = Report.objects.all().order_by('-id')
        report_list = {"report_list" : report_objects}
        return render(request, self.template, report_list)

class Pdfview(View): # pdf 보는 view
    def get(self,request, pk):
        try:
            x = Report.objects.get(id = pk)
            return FileResponse(open(str(x.pdf), 'rb'), content_type='application/pdf')
        except FileNotFoundError:
            raise Http404()


class SignUpView(View): # 회원가입 하는 View
    success_url = 'registration/success_sigh_up'
    template_name = 'registration/signup.html'

    def get(self, request):
        form = CreateForm()
        ctx = {'form':form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = CreateForm(request.POST)
        if not form.is_valid():
            ctx = {'form' : form}
            return render(request, self.template_name, ctx)
        user = form.save(commit= False) #  여기서 그냥 저장하지 말고 form보고 form으로 보면 될듯?
        user.is_active = False
        print('Before celery')
        dic = {"username" : user.username, "email": user.email}
        json_object = json.dumps(dic, indent = 4) 
        to_email = form.cleaned_data.get('email') 
        send_email.delay(json_object)
        user.save()
        print('Out celery')
        return redirect(self.success_url +"/" +str(to_email))

class Certification(View): # email 보낸거 정확한지 확인하는 View
    def get(self, request,uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(username=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):  #여기를 체크 해봐야할듯.. 이거 지금 안됨 03/30
            user.is_active = True 
            user.save()
            return redirect('home:emailvalidation')  
        else:
            return redirect('home:success_sigh_up', {'email': ''})  


class SuccessSignUp(View): # 메일 정삭적으로 보낸 뒤 나오는 화면
    template_name = 'registration/success_sign_up.html'
    def get(self, request, email):
        try:
            user = User.objects.get(email = email)
            ctx = {'email' : user.email}
            if user.is_active:
                return render(request, self.template_name)

            else:
                return render(request, self.template_name, ctx)
        except:
            return render(request, self.template_name)



class EmailvalidationView(View):
    success_template = 'registration/validation.html'
    def get(self, request):
        return render(request, self.success_template)


class AddFavoriteView(LoginRequiredMixin, View):
    template = 'home/main.html'
    def post(self, request, pk) :  
        t = Report.objects.get(id = pk)
        fav = Fav(user=request.user, report=t)
        try:
            fav.save()  # In case of duplicate key
            print(request.user.favorite_reports, '여기 들어옴')
            print('t =', t.favorite)
            print('fav =',fav.report, fav.user)
            print('uesr =',request.user, request.user.favorite_reports.all(),request.user.favs_users)
            # report.company_name in  user.favorite_reports
        except IntegrityError as e:
            pass
        return redirect('home:homepage')


class DeleteFavoriteView(LoginRequiredMixin, View):
    template = 'home/main.html'
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Report, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, report=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return redirect('home:homepage')