from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser, User
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory, Client
from django.utils.translation import ugettext_lazy as _

from webaccount.views import AccountAuthView, AccountEditView
from webshopcart.models import ProductCart
from website.views import index_page

REQUIRED_FIELD = 'Обязательное поле.'
BAD_PASSWORD = 'Пожалуйста, введите правильные имя пользователя и пароль. ' \
               'Оба поля могут быть чувствительны к регистру.'
USER_IS_EXiSTS = _("A user with that email address already exists")
LOGIN_BUTTON_LABEL = 'Log in'
REGISTRATION_BUTTON_LABEL = 'Register'


class AccountPageProfileTest(TestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.email = 'test@user.net'
        self.username = 'test'
        self.password = 'top_secret'
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username=self.username, email=self.email, password=self.password)

    def test_profile_url_without_auth_user(self):
        request = self.factory.get(settings.LOGIN_REDIRECT_URL)
        request.user = AnonymousUser()
        response = AccountEditView.as_view()(request)

        self.assertEqual(response.status_code, 302)

    def test_profile_url_with_auth_user(self):
        request = self.factory.get(settings.LOGIN_REDIRECT_URL)
        request.user = self.user
        response = AccountEditView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="{}"'.format(self.username))
        self.assertContains(response, 'value="{}"'.format(self.email))

    # TODO
    def test_profile_active_tab(self):
        pass
        # c = Client()
        # c.login(username=self.email, password=self.password)
        #
        # response = c.get(reverse('account:profile'))
        #
        # self.assertEqual(response.status_code, 200)

    def test_profile_change_email(self):
        c = Client()
        c.login(username=self.email, password=self.password)

        new_email = 'other@email.change'

        response = c.post(settings.LOGIN_REDIRECT_URL, data={
            'email': new_email,
            'username': self.username,
            'old_password': '',
            'password1': '',
            'password2': '',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.get(username=self.username).email, new_email)

    def test_profile_change_email_to_exists(self):
        c = Client()

        new_email = 'other@email.change'
        User.objects.create_user(
            username='newuser', email=new_email, password=self.password)

        c.login(username=self.email, password=self.password)

        response = c.post(settings.LOGIN_REDIRECT_URL, data={
            'email': new_email,
            'username': self.username,
            'old_password': '',
            'password1': '',
            'password2': '',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.user, User.objects.get(username=self.username))
        self.assertEqual(User.objects.get(username=self.username).email, self.email)
        self.assertContains(response, USER_IS_EXiSTS)

    def test_profile_change_username(self):
        c = Client()
        c.login(username=self.email, password=self.password)

        response = c.post(settings.LOGIN_REDIRECT_URL, data={
            'email': self.email,
            'username': self.username + 'other',
            'old_password': '',
            'password1': '',
            'password2': '',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.get(email=self.email).username, self.username + 'other')

    def test_profile_change_password(self):
        c = Client()
        c.login(username=self.user.email, password=self.password)

        newpassword = 'newpassword'

        response = c.post(settings.LOGIN_REDIRECT_URL, data={
            'email': self.email,
            'username': self.username,
            'old_password': self.password,
            'password1': newpassword,
            'password2': newpassword,
        })

        user = authenticate(
            username=self.email,
            password=self.password)
        self.assertFalse(user)

        user = authenticate(
            username=self.email,
            password=newpassword)

        self.assertTrue(user)
        self.assertEqual(response.status_code, 302)

    def test_profile_change_password_with_bad_old_password(self):
        c = Client()
        c.login(username=self.user.email, password=self.password)

        newpassword = 'newpassword'

        response = c.post(settings.LOGIN_REDIRECT_URL, data={
            'email': self.email,
            'username': self.username,
            'old_password': 'not{}'.format(self.password),
            'password1': newpassword,
            'password2': newpassword,
        })

        user = authenticate(
            username=self.email,
            password=newpassword)
        self.assertFalse(user)

        user = authenticate(
            username=self.email,
            password=self.password)
        self.assertTrue(user)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, BAD_PASSWORD)

    def test_profile_change_password_without_old_password(self):
        c = Client()
        c.login(username=self.user.email, password=self.password)

        newpassword = 'newpassword'

        response = c.post(settings.LOGIN_REDIRECT_URL, data={
            'email': self.email,
            'username': self.username,
            'old_password': '',
            'password1': newpassword,
            'password2': newpassword,
        })

        user = authenticate(
            username=self.email,
            password=newpassword)
        self.assertFalse(user)

        user = authenticate(
            username=self.email,
            password=self.password)
        self.assertTrue(user)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, BAD_PASSWORD)

    def test_profile_change_password_with_old_password_and_without_new_password(self):
        c = Client()
        c.login(username=self.user.email, password=self.password)

        newpassword = ''

        response = c.post(settings.LOGIN_REDIRECT_URL, data={
            'email': self.email,
            'username': self.username,
            'old_password': self.password,
            'password1': newpassword,
            'password2': newpassword,
        })

        user = authenticate(
            username=self.email,
            password=self.password)
        self.assertTrue(user)

        self.assertEqual(response.status_code, 302)

    def test_profile_set_email_to_empty(self):
        c = Client()
        c.login(username=self.email, password=self.password)

        response = c.post(settings.LOGIN_REDIRECT_URL, data={
            'email': '',
            'username': self.username,
            'old_password': '',
            'password1': '',
            'password2': '',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, REQUIRED_FIELD)

    def test_profile_set_username_to_empty(self):
        c = Client()
        c.login(username=self.email, password=self.password)

        response = c.post(settings.LOGIN_REDIRECT_URL, data={
            'email': self.email,
            'username': '',
            'old_password': '',
            'password1': '',
            'password2': '',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, REQUIRED_FIELD)


class AccountPageLoginTest(TestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.email = 'test@user.net'
        self.username = 'test'
        self.password = 'top_secret'
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username=self.username, email=self.email, password=self.password)

    def test_login_url_without_auth_user(self):
        request = self.factory.get(settings.LOGIN_URL)
        request.user = AnonymousUser()
        response = AccountAuthView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_login_url_with_auth_user(self):
        request = self.factory.get(settings.LOGIN_URL)
        request.user = self.user
        response = AccountAuthView.as_view()(request)

        self.assertEqual(response.status_code, 302)

    def test_login_button_without_auth_user(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        request.session = {}
        response = index_page(request)

        self.assertContains(response, 'Логин/Регистрация')
        self.assertContains(response, 'href="{}"'.format(settings.LOGIN_URL))

    def test_login_button_with_auth_user(self):
        request = self.factory.get('/')
        request.user = self.user
        request.session = {}
        response = index_page(request)

        self.assertContains(response, 'Здравствуйте, test')
        self.assertContains(response, 'href="{}"'.format(settings.LOGIN_REDIRECT_URL))

    def test_login_user(self):
        c = Client()
        response = c.post(settings.LOGIN_URL, data={
            'login-username': self.email,
            'login-password': self.password,
            'login_submit': LOGIN_BUTTON_LABEL,
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.wsgi_request.user, User.objects.get(username=self.username))

    def test_login_user_with_bad_password(self):
        c = Client()
        response = c.post(settings.LOGIN_URL, data={
            'login-username': self.email,
            'login-password': 'bad{}'.format(self.password),
            'login_submit': LOGIN_BUTTON_LABEL,
        })

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.wsgi_request.user, User.objects.get(username=self.username))
        self.assertContains(response, BAD_PASSWORD)

    def test_login_user_required_fields(self):
        c = Client()
        response = c.post(settings.LOGIN_URL, data={
            'login-username': '',
            'login-password': self.password,
            'login_submit': LOGIN_BUTTON_LABEL,
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, REQUIRED_FIELD)

        response = c.post(settings.LOGIN_URL, data={
            'login-username': self.email,
            'login-password': '',
            'login_submit': LOGIN_BUTTON_LABEL,
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, REQUIRED_FIELD)

    def test_registration_user(self):
        c = Client()

        username = 'newuser'

        response = c.post(settings.LOGIN_URL, data={
            'registration-email': 'new@user.name',
            'registration-username': username,
            'registration-password1': 'secret',
            'registration-password2': 'secret',
            'registration_submit': REGISTRATION_BUTTON_LABEL,
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username=username).exists())
        self.assertEqual(response.wsgi_request.user, User.objects.get(username=username))

    def test_registration_exists_user(self):
        c = Client()

        username = 'newuser'

        response = c.post(settings.LOGIN_URL, data={
            'registration-email': self.email,
            'registration-username': username,
            'registration-password1': 'secret',
            'registration-password2': 'secret',
            'registration_submit': REGISTRATION_BUTTON_LABEL,
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.user, AnonymousUser())
        self.assertContains(response, USER_IS_EXiSTS)

    def test_registration_user_different_password(self):
        c = Client()

        username = 'newuser'

        response = c.post(settings.LOGIN_URL, data={
            'registration-email': 'new@user.name',
            'registration-username': username,
            'registration-password1': 'supersecret',
            'registration-password2': 'extrasecret',
            'registration_submit': REGISTRATION_BUTTON_LABEL,
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=username).exists())
        self.assertEqual(response.wsgi_request.user, AnonymousUser())
        self.assertContains(response, _("The two password fields didn't match."))

    def test_registration_user_required_fields(self):
        c = Client()

        username = 'newuser'

        response = c.post(settings.LOGIN_URL, data={
            'registration-email': '',
            'registration-username': username,
            'registration-password1': 'secret',
            'registration-password2': 'secret',
            'registration_submit': REGISTRATION_BUTTON_LABEL,
        })

        self.assertContains(response, REQUIRED_FIELD)

        response = c.post(settings.LOGIN_URL, data={
            'registration-email': 'new@user.name',
            'registration-username': '',
            'registration-password1': 'secret',
            'registration-password2': 'secret',
            'registration_submit': REGISTRATION_BUTTON_LABEL,
        })

        self.assertContains(response, REQUIRED_FIELD)

        response = c.post(settings.LOGIN_URL, data={
            'registration-email': 'new@user.name',
            'registration-username': username,
            'registration-password1': '',
            'registration-password2': 'secret',
            'registration_submit': REGISTRATION_BUTTON_LABEL,
        })

        self.assertContains(response, REQUIRED_FIELD)

        response = c.post(settings.LOGIN_URL, data={
            'registration-email': 'new@user.name',
            'registration-username': username,
            'registration-password1': 'secret',
            'registration-password2': '',
            'registration_submit': REGISTRATION_BUTTON_LABEL,
        })

        self.assertContains(response, REQUIRED_FIELD)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=username).exists())
        self.assertEqual(response.wsgi_request.user, AnonymousUser())

    def test_logout(self):
        c = Client()
        c.login(username=self.email, password=self.password)

        response = c.get(settings.LOGOUT_URL)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.wsgi_request.user, AnonymousUser())


class ProfileOrdersTest(TestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.email = 'test@user.net'
        self.username = 'test'
        self.password = 'top_secret'
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username=self.username, email=self.email, password=self.password)

        client = Client()
        client.login(username=self.email, password=self.password)
        self.login_client = client
        self.order = ProductCart.objects.get(pk=100)

    def test_profile_orders_without_login(self):
        response = self.client.get(reverse('account:profile_orders'))
        self.assertEqual(response.status_code, 302)

    def test_profile_orders_with_login(self):
        response = self.login_client.get(reverse('account:profile_orders'))
        self.assertEqual(response.status_code, 200)

    def test_profile_detail_order_without_login(self):
        response = self.client.get(reverse('account:profile_order', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 302)

    def test_profile_another_detail_order_with_login(self):
        response = self.login_client.get(reverse('account:profile_order', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 302)

    def test_profile_your_detail_order_with_login(self):
        self.order.owner = self.user
        self.order.save()

        response = self.login_client.get(reverse('account:profile_order', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 200)
