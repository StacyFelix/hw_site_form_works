from pprint import pprint

from django import http
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Product, Review
from .forms import ReviewForm


def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()
    # request.session.clear()

    context = {
        'product_list': products,
    }

    return render(request, template, context)


def product_view(request, pk):
    template = 'app/product_detail.html'
    product = get_object_or_404(Product, id=pk)
    reviews = Review.objects.filter(product=product)
    form = ReviewForm()
    if not request.session.get('reviewed_products'):
        list_reviews = []
    else:
        list_reviews = request.session['reviewed_products']
    # print(f"ЛИСТ ИЗ СЕССИИИ {list_reviews}")

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        # print(form.data['text'])
        if form.is_valid():
            list_reviews.append(pk)
            request.session['reviewed_products'] = list_reviews
            # form.save()
            # ругается на отсутствие внешнего ключа на таблицу product:
            # NOT NULL constraint   failed: app_review.product_id
            # поэтому сделала так:
            Review.objects.create(text=form.data['text'], product=product)
            # print(f"СЕССИЯ ИЗ ЛИСТА {request.session['reviewed_products']}")
            return http.HttpResponseRedirect('')

    is_review_exist = False
    if request.session.get('reviewed_products'):
        if request.session['reviewed_products'].count(pk) > 0:
            is_review_exist = True

    context = {
        'form': form,
        'product': product,
        'reviews': reviews,
        'is_review_exist': is_review_exist
    }

    return render(request, template, context)
