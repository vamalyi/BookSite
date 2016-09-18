from django.conf import settings
from django.db import models
from django.utils.translation import pgettext_lazy, ugettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('User'))

    note = models.TextField(pgettext_lazy('user_profile', 'Note'), blank=True)
    birthday = models.DateField(_('Birthday'), blank=True, null=True)
    SEX = (
        (None, '-----'),
        ('1', _('Male')),
        ('2', _('Female')),
    )
    sex = models.CharField(_('Sex'), choices=SEX, max_length=2, blank=True)

    company = models.CharField(_('Company'), max_length=255, blank=True)

    receive_mailing = models.BooleanField(_('Receive mailing'), default=True)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')


class AbstractAddress(models.Model):
    line1 = models.CharField(_("First line of address"), max_length=255)
    line2 = models.CharField(
        _("Second line of address"), max_length=255, blank=True)
    line3 = models.CharField(
        _("Third line of address"), max_length=255, blank=True)
    line4 = models.CharField(_("City"), max_length=255, blank=True)

    class Meta:
        abstract = True
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')


class UserAddress(AbstractAddress):
    user = models.ForeignKey(
        'webaccount.UserProfile', on_delete=models.CASCADE,
        related_name='addresses', verbose_name=_("User"))

    is_default_for_shipping = models.BooleanField(
        _("Default shipping address?"), default=False)

    num_orders = models.PositiveIntegerField(_("Number of Orders"), default=0)

    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("User address")
        verbose_name_plural = _("User addresses")
        ordering = ['-num_orders']

    def save(self, *args, **kwargs):
        self._ensure_defaults_integrity()
        super().save(*args, **kwargs)

    def _ensure_defaults_integrity(self):
        if self.is_default_for_shipping:
            self.__class__._default_manager \
                .filter(user=self.user, is_default_for_shipping=True) \
                .update(is_default_for_shipping=False)


class UserPhoneNumber(models.Model):
    user = models.ForeignKey(
        'webaccount.UserProfile', on_delete=models.CASCADE,
        related_name='phone_numbers', verbose_name=_("User"))
    phone_number = models.CharField(_('Phone number'), max_length=25)

    is_default_phone_number = models.BooleanField(
        _("Default phone number?"), default=False)

    class Meta:
        verbose_name = _("Phone number")
        verbose_name_plural = _("Phone numbers")
        unique_together = ('user', 'phone_number')

    def save(self, *args, **kwargs):
        self._ensure_defaults_integrity()
        super().save(*args, **kwargs)

    def _ensure_defaults_integrity(self):
        if self.is_default_phone_number:
            self.__class__._default_manager \
                .filter(user=self.user, is_default_phone_number=True) \
                .update(is_default_phone_number=False)
