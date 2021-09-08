from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import send_mail, mail_admins
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from emailuser.models import manual_create_email_user
from emailuser.models import EmailUserForm

from djangohelpers.utils import gen_url


@never_cache
def login_view(request):
    sended = False
    if request.method == "POST":
        form = EmailUserForm(request.POST)
        if form.is_valid():  # All validation rules pass
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    email=form.cleaned_data["email"],
                    username=form.cleaned_data["email"],
                    password=gen_url(20),
                )
                user.save()

            try:
                token = user.emailuser.generate_token()
            except:
                manual_create_email_user(user)
                token = user.emailuser.generate_token()
            # try:
            if settings.DEBUG:
                print("Token - %s" % token)
            auth_link = reverse(
                "userapp:auth", kwargs={"user_id": user.pk, "token": token}
            )
            # tmp_token = gen_url(5)
            msg = render_to_string(
                "user/auth-email.html",
                {
                    "site_url": settings.SITE_URL,
                    "auth_link": auth_link,
                    "support_email": settings.SERVER_EMAIL,
                    # "token": token
                },
            )
            subj = "Вход на сайт: %s" % settings.SITE_NAME
            if settings.DEBUG:
                print(subj)
                print(msg)

            send_mail(
                subj,
                msg,
                u"%s" % settings.SERVER_EMAIL,
                [email],
                fail_silently=settings.DEBUG,
            )

            sended = True
        else:
            print(form.errors)

    else:
        form = InviteForm()
    return render(
        request,
        "user/login.html",
        {"form": form, "sended": sended, "support_email": settings.SUPPORT_EMAIL},
    )


@never_cache
def auth(request, user_id, token):
    get_user = get_object_or_404(User, pk=user_id)
    user = authenticate(email=get_user.email, token=token)
    if settings.DEBUG:
        print("User: %s" % user)
        print("Email:%s, Token: %s" % (get_user.email, token))
    if user is not None:
        if user.is_active:
            if settings.DEBUG:
                print("Logging in..")
            login(request, user)
    return render(request, "user/auth.html", {"user": user})




@login_required
def logout_view(request):
    logout(request)
    return redirect("/")
