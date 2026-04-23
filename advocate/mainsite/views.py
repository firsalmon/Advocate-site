from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from django.contrib import messages
from .models import Review, ThankfulLetter, Questions
from .forms import LeadForm
import time

@require_GET
def static_page(request, template_name, title, description):
    page = f"mainsite/{template_name}.html"
    data = {
        "title": title,
        "description": description
    }
    if template_name == "home":
        data["reviews"] = Review.objects.filter(is_published=True).order_by("-created_at")[:4]
        data["thankful"] = ThankfulLetter.objects.filter(is_published=True).order_by("-created_at")[:4]
        data["questions"] = Questions.objects.filter(is_published=True)

    return render(request, page, data)



@require_POST
def leadForm(request):
    referer = request.META.get('HTTP_REFERER', 'mainsite:home')

    if request.POST.get("website"):
        return redirect(referer)

    last_submit = request.session.get('last_lead_submit', 0)
    if time.time() - last_submit < 900:
        messages.error(request, "⏳ Пожалуйста, подождите 15 минут перед повторной отправкой.")
        return redirect(referer)


    form = LeadForm(request.POST)
    if form.is_valid():
        form.save()
        request.session['last_lead_submit'] = time.time()  # Фиксируем время
        messages.success(request, "✅ Заявка отправлена. Я свяжусь с вами в ближайшее время.")
        return redirect(referer)
    else:
        messages.error(request, "❌ Некорректные данные или пропущены обязательные к заполнению поля")
        return redirect(referer)
