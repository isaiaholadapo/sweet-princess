from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import generic

from . import forms, models
from .token import account_activation_token


# Create your views here.


def account_register(request):

    # if request.user.is_authenticated:
    #     return redirect('account:dashboard')

    if request.method == 'POST':
        registerForm = forms.RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('registered succesfully and activation sent')
    else:
        registerForm = forms.RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})

# class AccountRegister(generic.CreateView):
#     model = models.UserBase
#     form_class = forms.RegistrationForm
#     template_name = 'account/registration/register.html'
#
#     # def dispatch(self, request, *args, **kwargs):
#     #     if request.user.is_authenticated:
#     #         return HttpResponseRedirect('account:dashboard')
#     #
#     #     return super().dispatch(request, *args, **kwargs)
#
#     def get_queryset(self):
#         return models.UserBase.objects.all()
#
#     def post(self, request, *args, **kwargs):
#         # self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.email = form.cleaned_data['email']
#             user.set_password(form.cleaned_data['password'])
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             subject = 'Activate your Account'
#             message = render_to_string('account/registration/account_activation_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#             user.email_user(subject=subject, message=message)
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = models.UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')


@login_required
def dashboard(request):
    # orders = user_orders(request)
    return render(request,
                  'account/user/dashboard.html',
                  # {'section': 'profile', 'orders': orders}
           )

@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = forms.UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = forms.UserEditForm(instance=request.user)

    return render(request,
                  'account/user/edit_details.html', {'user_form': user_form})


@login_required
def delete_user(request):
    user = models.UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')

