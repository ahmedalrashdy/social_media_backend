import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email


class CustomUserManager(BaseUserManager):
    def _validate_email(self, email):
        """تحقق من صحة البريد الإلكتروني وتطبيع قيمته"""
        try:
            validate_email(email)
            return self.normalize_email(email)
        except ValidationError:
            raise ValidationError({'email': _('يرجى إدخال عنوان بريد إلكتروني صحيح')})

    def _validate_password(self, password):
        """تحقق من قوة كلمة المرور باستخدام معايير أمان قوية"""
        if len(password) < 8:
            raise ValidationError({'password': _('يجب أن تحتوي كلمة المرور على 8 حرفًا على الأقل')})
        


    def create_user(self, email, password=None, **extra_fields):
        """
        إنشاء مستخدم عادي مع تطبيق شروط التحقق القوية
        """
        # تحقق من البريد الإلكتروني
        email = self._validate_email(email)
        
        # التحقق من كلمة المرور
        if password:
            self._validate_password(password)
        else:
            raise ValidationError({'password': _('يجب تعيين كلمة مرور')})
        
        # إنشاء المستخدم
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        إنشاء مستخدم مع صلاحيات المشرف العام
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValidationError({'is_staff': _('يجب أن يتمتع المشرف العام بصلاحيات فريق العمل')})
        
        if extra_fields.get('is_superuser') is not True:
            raise ValidationError({'is_superuser': _('يجب أن يتمتع المشرف العام بصلاحيات المشرف العام')})

        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    # الحقول الأساسية
    name = models.CharField(
        _("الاسم الكامل"),
        max_length=255,
        blank=True,
        default='',
        help_text=_("ادخل اسمك الكامل (اختياري)")
    )
    
    email = models.EmailField(
        _("البريد الإلكتروني"),
        unique=True,
        db_index=True,
        error_messages={
            'unique': _("هذا البريد الإلكتروني مسجل مسبقًا.")
        }
    )
    
    
    # الحقول الإدارية
    date_joined = models.DateTimeField(
        _("تاريخ الانضمام"),
        auto_now_add=True
    )
    
    last_login = models.DateTimeField(
        _("آخر تسجيل دخول"),
        auto_now=True
    )
    
    is_staff = models.BooleanField(
        _("عضو فريق العمل"),
        default=False,
        help_text=_("يحدد ما إذا كان المستخدم يمكنه الوصول لوحة الإدارة.")
    )
    
    is_active = models.BooleanField(
        _("نشط"),
        default=True,
        help_text=_("يحدد ما إذا كان الحساب مفعلاً. يمكنك إلغاء التفعيل بدل الحذف.")
    )
    
    verified = models.BooleanField(
        _("تم التحقق"),
        default=False,
        help_text=_("يحدد ما إذا كان البريد الإلكتروني تم التحقق منه.")
    )

    # الحقول المطلوبة للنظام
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("مستخدم")
        verbose_name_plural = _("المستخدمون")
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['date_joined']),
        ]
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.email} ({self.name})" if self.name else self.email

    def get_full_name(self):
        return self.name.strip() or self.email

    def get_short_name(self):
        return self.name.split()[0] if self.name else self.email.split('@')[0]

    def clean(self):
        """تنظيف البيانات قبل الحفظ"""
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


