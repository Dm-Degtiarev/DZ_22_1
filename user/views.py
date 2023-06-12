from config import settings
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, FormView
from django.contrib.auth import get_user_model
from django.contrib.auth import logout, login
from django.shortcuts import redirect, get_object_or_404
from .forms import UserRegistrationForm, UserPasswordResetForm, UserAuthenticationForm
from user.models import User


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'user/registration.html'
    success_url = reverse_lazy('user:login')


    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        subject = 'Верификация django'
        message = f'Добрый день,{user.first_name}! Проверьте свою учетную запись, перейдя по этой ссылке: ' \
                  f'http://localhost:8000{reverse_lazy("user:verify_account", kwargs={"user_pk": user.pk})}.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return response


def verify_account(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    user.is_active = True
    user.save()
    login(request, user)
    return redirect(to=reverse('user:login'))


class UserLoginView(LoginView):
    form_class = UserAuthenticationForm
    template_name = 'user/login.html'

    def get_success_url(self):
        return reverse_lazy('catalog:products_list')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('catalog:products_list')

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'logout':
            logout(request)  # Выполнить выход пользователя
        elif action == 'registration':
            return redirect('user:registration')  # Перенаправить на страницу регистрации

        return super().post(request, *args, **kwargs)


class UserPasswordResetView(FormView):
    template_name = 'user/password_reset.html'
    form_class = UserPasswordResetForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']

        # Получение пользователя по введенному email
        UserModel = get_user_model()
        try:
            user = get_user_model().objects.get(email=email)
        except UserModel.DoesNotExist:
            # Если пользователя с таким email не найдено, можно вывести сообщение об ошибке
            form.add_error('email', 'User with this email address does not exist.')
            return self.form_invalid(form)

        # Генерация нового случайного пароля
        new_password = UserModel.objects.make_random_password()

        # Сохранение нового пароля для пользователя
        user.set_password(new_password)
        user.save(update_fields=['password'])

        # Отправка нового пароля пользователю по email
        subject = 'Изменение пароля'
        message = f'Ваш новый пароль: {new_password}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

        # Редирект на страницу успешного сброса пароля
        return super().form_valid(form)
