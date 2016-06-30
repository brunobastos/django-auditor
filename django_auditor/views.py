# coding: utf-8
from django.shortcuts import render, redirect
from .models import Auditor
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

def admin(request, template_name='auditor/admin.html'):

    auditor_list = Auditor.objects.all()

    paginator = Paginator(auditor_list, 15)

    page = request.GET.get('page')
    try:
        audits = paginator.page(page)
    except PageNotAnInteger:
        audits = paginator.page(1)
    except EmptyPage:
        audits = paginator.page(paginator.num_pages)

    if 'tenant' in settings.AUDITOR:
        tenant = True
    else:
        tenant = False
    return render(request, template_name, {"audits": audits, "tenant": tenant})