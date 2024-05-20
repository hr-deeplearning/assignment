<div dir="rtl">
برای احراز هویت از پکیج زیر استفاده شده است:

</div>

```bash
djangorestframework-simplejwt
```


<div dir="rtl">
با استفاده از این پکیج و همچنین سفارشی‌سازی مدل User در جنگو، نیازمندی تمرین برآورده شد. بدین صورت که یک مدلی توسعه داده شده است که با email, password عملیات‌های ورود و ثبت‌نام را با استفاده از APIهای انجام می‌دهد.

</div>

```python
path("auth/signup", user_singup, name="auth-signup"),
path("auth/", user_login, name="auth-login"),
```