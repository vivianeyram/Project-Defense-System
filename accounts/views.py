import requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages, auth
from django.contrib.auth import get_user_model, authenticate, login as auth_login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from faculty.models import Faculty
from course.models import Program
from djangoProject12 import settings
from .forms import StudentRegistrationForm, LecturerRegistrationForm
from .models import Student, UserAgentInfo, Lecturer, CustomUser
from django_user_agents.utils import get_user_agent
from django.contrib.auth.models import AnonymousUser


# Create your views here.
def get_user_agents(request):
    return request.META.get('HTTP_USER_AGENT', '')


def dashboard(request):
    return render(request, 'dashboard.html')


@csrf_exempt
def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                messages.success(request, 'Login successful')
                user_agent = get_user_agents(request)

                request.session['is_mobile'] = 'Mobile' in user_agent

                if user.is_student:
                    return redirect('accounts:student_profile_url')
                elif user.is_lecturer:
                    return redirect('accounts:lect_profile_url')
                elif user.is_staff:
                    return redirect('accounts:dashboard_url')
            else:
                messages.error(request, 'Your Account is not Active')
        else:
            messages.error(request, 'Invalid Credentials')

    return render(request, 'login/login.html')


@csrf_exempt
def student_signup(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = True
            user.save()

            student = Student.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                index_number=form.cleaned_data['index_number'],
                phone=form.cleaned_data['phone'],
                program=form.cleaned_data['program'],
                level=form.cleaned_data['level'],
                supervisor=form.cleaned_data['supervisor'],

            )

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            current_site = get_current_site(request)
            email = form.cleaned_data['email']
            html_template = 'verification.html'
            html_message = render_to_string(html_template, {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),

            })
            mail_subject = "Account Activation"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            message = EmailMessage(mail_subject, html_message, email_from, recipient_list)
            message.content_type = "html"
            message.send()

            messages.success(request, 'Signup successful. Check your mail for verification')
            return redirect('/accounts/login/?command=verification&email=' + email)
    else:
        form = StudentRegistrationForm()
        program = Program.objects.all()

    return render(request, 'login/student_signup.html', {'form': form})


def student_profile(request):
    return render(request, 'login/studentprofile.html')


def lecturer_profile(request):
    return render(request, 'login/lecturerprofile.html')


def lecturer_activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        User = get_user_model()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! You Account have successfully ")
        return redirect('accounts:login_url')
    else:
        messages.error(request, "Invalid activation token")
        return redirect('accounts:lecturer_signup_url')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        User = get_user_model()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('accounts:login_url')
    else:
        messages.error(request, 'Invalid activation Link.')
        return redirect('accounts:student_signup_url')



@csrf_exempt
def lecturer_registration(request):
    if request.method == 'POST':
        form = LecturerRegistrationForm(request.POST or None, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.is_lecturer = True
            user.save()
            lecturer = Lecturer.objects.create(
                user=user,
                staff_id=form.cleaned_data['staff_id'],
                title=form.cleaned_data['title'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone=form.cleaned_data['phone'],
                faculty=form.cleaned_data['faculty'],
            )

            current_site = get_current_site(request)
            email = form.cleaned_data['email']
            html_template = 'lverification.html'
            html_message = render_to_string(html_template, {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            mail_subject = "ACCOUNT ACTIVATION"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            message = EmailMessage(mail_subject, html_message, email_from, recipient_list)
            message.content_type = 'html'
            message.send()
            messages.success(request, 'Signup Successfully Success. Please check your mail for further instructions.')
            return redirect('/accounts/login/?command=verification&email=' + email)
        else:
            messages.error(request, 'Error occurred while processing your registration. Please check the form entries.')
    else:
        form = LecturerRegistrationForm()
        faculty = Faculty.objects.all()
    return render(request, 'login/signupL.html', {'form': form})


def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out")
    return redirect('accounts:login_url')


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def forgetPassword(request):
    if request.method == 'POST':
        user_agents_str = get_user_agents(request)
        user_ip = request.META.get('REMOTE_ADDR')
        ip_info = requests.get(f'http://ip-api.com/json/{user_ip}').json()
        ip_country = ip_info.get('country', '')

        try:
            anonymous_user = CustomUser.objects.get(email='anonymous')
        except CustomUser.DoesNotExist:
            anonymous_user = CustomUser.objects.create(email='anonymous')
        user_agent_info = UserAgentInfo.objects.create(user=anonymous_user, user_agent=user_agents_str, user_ip=user_ip,
                                                       ip_country=ip_country)

        email = request.POST.get('email', '')
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email__exact=email)
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = "Reset Accounts"
            message = render_to_string('forget/resetverification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'user_agent_info': [user_agent_info]

            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, "Password reset mail has been sent to your mail")
            return redirect('accounts:login_url')
        else:
            messages.error(request, "Account Doesnot Exists")
            return redirect('accounts:forget_password')
    return render(request, 'forget/forgetpassword.html')


def resetpasswordValiate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesnotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please Reset Your Password')
        return redirect('accounts:resetpassword_url')

    else:
        messages.error(request, 'This link is expired')
        return redirect('accounts:resetpassword_url')


def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = CustomUser.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Reset Password was successfully")
            return redirect('accounts:login_url')
        else:
            messages.error(request, 'passwords do not match')
            return redirect('accounts:resetpassword_url')
    else:
        return render(request, 'forget/passrest.html')
