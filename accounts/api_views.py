# import hashlib
# from django.shortcuts import get_object_or_404, render
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.decorators import api_view
# from accounts.models import User
# from accounts.serializer import CheckOTPSerializer, LoginSerializer, RegisterSerializer, UserSerializer
# from utils.custom_permission import IsAuthenticatedArabic
# from .security import create_token,decrypt_token
# import random
# from django.utils import timezone
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib.auth import authenticate
# from rest_framework.decorators import permission_classes
# from rest_framework_simplejwt.tokens import RefreshToken

# MAX_ATTEMPTS = 3  # الحد الأقصى للمحاولات
# TIMEOUT = 300     # 5 دقائق بالثواني    
# from django.core.cache import cache
# def send_otp(user):
#     otp = random.randint(1000, 9999)
#     print(otp)
#     expiry = timezone.now() + timezone.timedelta(minutes=10)
    
#     token = create_token({
#         "id": user.id,
#         "email": user.email,
#         "name": user.name,
#         "otp": str(otp),
#         "exp": expiry
#     })
    
    
#     send_mail(
#         subject="تأكيد حسابك",
#         message=f"رمز التحقق الخاص بك هو: {otp}",
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[user.email]
#     )
#     return token

# @api_view(['POST'])
# def register(request):
#     if request.method != "POST":
#         print ("Register")
#         return Response({"error": "الطريقة غير مسموح بها"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     serializer = RegisterSerializer(data=request.data)
#     if not serializer.is_valid():
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     user = serializer.save()
#     token=send_otp(user)
#     return Response({
#         "success": "تم إنشاء الحساب بنجاح",
#         "token": token,
#     }, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
# def login(request):
#     if request.method != "POST":
#         return Response({"error": "الطريقة غير مسموح بها"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
#     serializer = LoginSerializer(data=request.data)
#     if not serializer.is_valid():
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     email = serializer.validated_data['email']
#     password = serializer.validated_data['password']
#     user = authenticate(request, username=email, password=password)
    
#     if not user:
#         return Response({"error": "كلمة المرور أو البريد الإلكتروني غير صحيح"}, status=status.HTTP_400_BAD_REQUEST)
    
#     if not user.is_active:
#         return Response({"error": "الحساب غير مفعل"}, status=status.HTTP_403_FORBIDDEN)
    
#     refresh_token = RefreshToken.for_user(user)
    
#     return Response({
#         "user": UserSerializer(user).data,
#         "access_token": str(refresh_token.access_token),
#         "refresh_token": str(refresh_token),
#         "message": "تم تسجيل الدخول بنجاح"
#     }, status=status.HTTP_200_OK)

 
# def get_short_key(token):
#     return hashlib.sha256(token.encode()).hexdigest()

   
# @api_view(['POST'])    
# def verify_email(request):
    
#     serializer = CheckOTPSerializer(data=request.data)
#     if not serializer.is_valid():
#         return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
#     token = serializer.validated_data["token"]
#     otp = serializer.validated_data["otp"]
#     print("*"*100)
#     print(token)
#     print(otp)
#     print("*"*100)
#     # التحقق من عدد المحاولات
#     hashedToken=get_short_key(token)
#     current_attempts = cache.get(hashedToken, 0)
    
#     if current_attempts >= MAX_ATTEMPTS:
#         return Response(
#             {"error": "لقد تجاوزت الحد المسموح من المحاولات. يرجى المحاولة لاحقًا"},
#             status=status.HTTP_400_BAD_REQUEST #status.HTTP_429_TOO_MANY_REQUESTS
#         )
    
#     dec_token = decrypt_token(token)
#     print("*"*100)
#     print(dec_token)
#     print("*"*100)
#     if not dec_token["status"]:
#         cache.set(hashedToken, current_attempts + 1, TIMEOUT)
#         return Response({"error": "توكن غير صحيح"}, status=status.HTTP_400_BAD_REQUEST)
    
#     if dec_token["payload"]["otp"] != otp:
#         cache.set(hashedToken, current_attempts + 1, TIMEOUT)
#         return Response({"error": "كود التحقق غير صحيح"}, status=status.HTTP_400_BAD_REQUEST)
    
#     cache.delete(hashedToken)
    
#     user = User.objects.get(id=dec_token["payload"]["id"])
#     user.verified = True
#     user.save()
    
#     refresh_token = RefreshToken.for_user(user)
#     return Response({
#         "user": UserSerializer(user).data,
#         "access_token": str(refresh_token.access_token),
#         "refresh_token": str(refresh_token), 
#         "message": "تم التحقق بنجاح"
#     }, status=status.HTTP_200_OK)


    
# @api_view(['POST'])
# def resendRegisterOTP(request):
    
#     user=get_object_or_404(User,email=request.data.get('email',"").strip())
#     if user.verified:
#         return Response({"error":"لا يمكن ارسال رمز التحقق من صحه البريد الالكتروني لانه بالفعل تم التحقق منه"},
#                         status=status.HTTP_400_BAD_REQUEST)
#     token=send_otp(user)
#     return Response({
#         "success": "تم ارسال رمز التحقق بنجاح",
#         "token": token,
#     }, status=status.HTTP_201_CREATED)
    
    
        
from json import load
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.core.mail import send_mail
from accounts.models import User
from accounts.serializer import ChangePasswordSerializer, ConfirmResetSerializer, RegisterSerializer, ResendOTPSerializer, ResetPasswordSerializer, UserSerializer, VerifyOTPSerializer
from utils.otp.otp import OTPManager
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache

class AuthBaseView(APIView):
    
    def send_otp_email(self, email, otp):
        send_mail(
        subject="تأكيد حسابك",
        message=f"رمز التحقق الخاص بك هو: {otp}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
        print(f"OTP for {email}: {otp}")

class RegisterView(AuthBaseView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        if User.objects.filter(email=email).exists():
            return Response({'email': 'البريد الإلكتروني مسجل مسبقًا'}, status=status.HTTP_400_BAD_REQUEST)
        
        User.objects.create_user(**serializer.validated_data)
        otp = OTPManager.generate_otp(email)
        self.send_otp_email(email, otp)
        
        return Response({'message': 'تم التسجيل بنجاح، يرجى التحقق من البريد'})

class VerifyOTPView(AuthBaseView):
    def post(self, request):
        
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        
        
        result = OTPManager.verify_otp(email, otp)
        if not result['valid']:
            return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)
        
        
        user = User.objects.get(email=email)
        user.is_verified = True
        user.save()
        
    
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user':UserSerializer(user).data
        })
        
import json
import pyotp # تأكد من استيراده
import secrets # لتوليد رمز إعادة تعيين آمن
import hashlib # لتجزئة رمز إعادة التعيين
from django.core.cache import cache # تأكد من استيراد cache
from rest_framework.response import Response
from rest_framework import status


# ثابت لعدد محاولات التحقق المسموح بها
MAX_VERIFY_ATTEMPTS = 5
# ثابت لمدة صلاحية رمز إعادة التعيين الذي سيتم إنشاؤه (مثلاً 10 دقائق)
RESET_TOKEN_TIMEOUT_SECONDS = 10 * 60

class VerifyResetOTPView(AuthBaseView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        
        otp_cache_key = f'otp:{email}'
        cached_otp_data = cache.get(otp_cache_key)
        
        result = OTPManager.verify_otp(email, otp)
        if not result['valid']:
            return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)
     

        if cached_otp_data is None:
            return Response({'error': 'كود التحقق منتهي الصلاحية أو غير صحيح، يرجى طلب كود جديد.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        reset_token = secrets.token_urlsafe(32) 

        hashed_reset_token = hashlib.sha256(reset_token.encode()).hexdigest()
        reset_token_cache_key = f'reset_token:{hashed_reset_token}'


        cache.set(reset_token_cache_key, {'email': email}, RESET_TOKEN_TIMEOUT_SECONDS)
        print(f"Stored hashed reset token in cache for {email} under key {reset_token_cache_key}") # للتصحيح
        
        return Response({
            "message": "تم التحقق بنجاح.",
            "reset_token": reset_token
        }, status=status.HTTP_200_OK)
       

class ResendOTPView(AuthBaseView):
    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        print(request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        
        # حساب وقت الانتظار المتبقي
        cooldown = OTPManager.get_resend_cooldown(email)
        if cooldown > 0:
            return Response({
                'error': f'يرجى الانتظار {int(cooldown)} ثانية قبل إعادة المحاولة',
                'waiting_seconds':int(cooldown)
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        
        
        # توليد OTP جديد
        otp = OTPManager.generate_otp(email)
        self.send_otp_email(email, otp)
        
        return Response({'message': 'تم إرسال كود التحقق'})

class LoginView(AuthBaseView):
    def post(self, request):
        email = request.data.get('email',None)
        password = request.data.get('password',None)
        
        user = authenticate(username=email, password=password)#it will use custom auth backends to check pass and verify
        if not user:
            return Response({'error': 'بيانات الاعتماد غير صحيحة'}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user':UserSerializer(user).data
        })

class ResetPasswordView(AuthBaseView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        if not User.objects.filter(email=email).exists():
            return Response({'error': 'البريد الإلكتروني غير مسجل'}, status=status.HTTP_404_NOT_FOUND)
        
        # حساب وقت الانتظار المتبقي
        cooldown = OTPManager.get_resend_cooldown(email)
        print(cooldown)
        if cooldown > 0:
            return Response({
                'error': f'يرجى الانتظار {int(cooldown)} ثانية قبل إعادة المحاولة',
                'waiting_seconds':cooldown
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        
        otp = OTPManager.generate_otp(email)
        self.send_otp_email(email, otp)
        return Response({'message': 'تم إرسال كود التحقق'})
    




class ConfirmResetView(AuthBaseView):
    def post(self, request):
        serializer = ConfirmResetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        reset_token_provided = serializer.validated_data['reset_token']
        new_password = serializer.validated_data['new_password']

    
        hashed_token_provided = hashlib.sha256(reset_token_provided.encode()).hexdigest()
        reset_token_cache_key = f'reset_token:{hashed_token_provided}'

        cached_data = cache.get(reset_token_cache_key)

        if cached_data is None:
            return Response(
                {'error': 'رمز إعادة التعيين غير صالح أو منتهي الصلاحية. يرجى طلب إعادة تعيين مرة أخرى.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cache.delete(reset_token_cache_key)
        print(f"Deleted reset token from cache with key: {reset_token_cache_key}") # للتصحيح

        email = cached_data.get('email')
        if not email:
            print(f"Error: Email not found in cached data for token key {reset_token_cache_key}")
            return Response({'error': 'حدث خطأ داخلي أثناء معالجة الطلب.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
        except User.DoesNotExist:
            print(f"Error: User with email {email} not found during password reset.") 
            return Response({'error': 'المستخدم المرتبط بهذا الطلب غير موجود.'},
                            status=status.HTTP_404_NOT_FOUND) 
        except Exception as e:
            print(f"Error saving user {email} after password reset: {e}")
            return Response({'error': 'حدث خطأ أثناء تحديث كلمة المرور.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {"message": "تم تغيير كلمة المرور بنجاح."},
            status=status.HTTP_200_OK
        )
        
        

class ChangePasswordView(AuthBaseView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'error': 'كلمة المرور القديمة غير صحيحة'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'تم تغيير كلمة المرور بنجاح'})

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token",None)
            print(refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return   Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

# class LogoutView(APIView):
#     def post(self, request):
#         try:
#             # استلام refresh_token من الطلب
#             refresh_token = request.data.get("refresh_token", None)
#             print( not refresh_token)
#             # التحقق من وجود refresh_token
#             if not refresh_token:
#                 return Response({'error': 'refresh_token is required'}, status=status.HTTP_400_BAD_REQUEST)

#             # طباعة refresh_token للغرض التصحيحي (يمكنك إزالته إذا لم يكن ضروريًا)
#             print(f"refresh_token: {refresh_token}")

#             # التحقق من token وإلغاء صلاحيته
#             token = RefreshToken(refresh_token)
#             token.blacklist()  # إضافة التوكن إلى القائمة السوداء

#             # إرجاع استجابة ناجحة
#             return Response({'message': 'Logged out successfully'}, status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             # إرجاع رسالة خطأ إذا حدثت مشكلة
#             return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)