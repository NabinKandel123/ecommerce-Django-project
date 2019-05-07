from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.
from pdfkit import pdfkit
from rest_framework.decorators import api_view
from rest_framework.response import Response
from shop.forms import SignUpForm, ReviewForm
from shop.serializers import ProductSerializer
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
import pdfkit
import json

from ecommerce import settings
from shop.forms import ContactForm
from shop.models import Contact, Category, Product



def get_payload(request, title=""):
    return {
        "title": title,
        "categories": Category.objects.filter(active=True),
        "carts": Product.objects.filter(slug__in=request.session.get('items', []))
    }


def home(request):
    data = get_payload(request, "Home")
    data["products"] = Product.objects.filter(active=True)
    return render(request, "shop/index.html", data)


def details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    data = get_payload(request, product.title)
    data["product"] = product
    data["reviewform"] = ReviewForm()
    return render(request, "shop/details.html", data)


def review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated and request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
        return redirect('shop:detail', product.slug)
    else:
        form = SignUpForm()
        return render(request, "shop/signup.html", {"form": form})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('shop:login')
    else:
        form = SignUpForm()
    return render(request, "shop/signup.html", {"form": form})


def mylogin(request):
    if request.user.is_authenticated:
        return redirect("shop:home")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if user.is_active:
                return redirect("shop:home")
    return render(request, "shop/login.html")


def mylogout(request):
    logout(request)
    return redirect("shop:home")


def product_search(request):
    query = request.GET.get("q", "")
    data = get_payload(request, query + " - search result")
    data["products"] = Product.objects.filter(Q(title__contains=query) | Q(description__contains=query))
    return render(request, 'shop/products.html', data)


def my_cart(request):
    data = get_payload(request, "My cart")
    data["products"] = Product.objects.filter(slug__in=request.session.get('items', []))
    return render(request, 'shop/products.html', data)


def checkout(request):
    request.session['items'] = []
    request.session['cart_amount'] = 0
    return redirect("shop:home")


def categories(request, slug):
    category = get_object_or_404(Category, slug=slug)
    data = get_payload(request, category.title)
    data["products"] = Product.objects.filter(category=category)
    return render(request, "shop/products.html", data)


def products(request):
    data = get_payload(request, "Products")
    data["products"] = Product.objects.filter(active=True)
    return render(request, "shop/products.html", data)


def add_to_cart(request):
    if request.method == 'POST':
        slug = request.POST.get("slug", "")
        product = Product.objects.filter(slug=slug).first()
        if product:
            items = request.session.get('items', [])
            if slug not in items:
                items.append(product.slug)
                amount = request.session.get('cart_amount', 0.0) + float(product.price)
                request.session['items'] = items
                request.session['cart_amount'] = amount
                return JsonResponse({"status": "ok", "message": product.title + " added to cart",
                                     "count": len(items), "amount": amount})
            return JsonResponse({"status": "fail", "message": "Item already added"})
        return JsonResponse({"status": "fail", "message": "Item not found"})
    return JsonResponse({"status": "fail", "message": "Only post method allowed"})


@api_view(['GET'])
def api_products(request):
    query = request.GET.get("q", "")
    products = Product.objects.filter(Q(title__contains=query) | Q(description__contains=query))
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


class Contact1(View):
    def get(self, request):
        form  = ContactForm()
        return render(request, 'contactform.html', {'form': form})
        pass
    def post(self, request):
        form = ContactForm(request.POST)
        form.save(commit=True)
        return HttpResponseRedirect("/")
        # contact.full_name = 'Mr' + contact.full_name
        # contact.save()
        pass

class Contact2(View):
    # @login_required(login_url='/accounts/login/')
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('../%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            return render(request, 'contact.html')
    def post(self, request):
        name = request.POST.get('fname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        # data = "{name}, {email}, {address}, {message}".format(name=name, email=email, address= address, message=message)
        contact = Contact(full_name=name, email=email, address=address, phone_number=phone, message=message)
        contact.save()
        return HttpResponse("Contact is sent successfully")

def contact(request):
    if request.method == 'GET':
        return render(request, 'contact.html')
    else:
        name = request.POST.get('fname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        # data = "{name}, {email}, {address}, {message}".format(name=name, email=email, address= address, message=message)
        contact = Contact(full_name=name, email=email, address=address, phone_number=phone, message=message)
        contact.save()
        return HttpResponse("Contact is sent successfully")


def contactList(request):
    mContactList = Contact.objects.all()
    return render(request, 'contactlist.html', {'data':mContactList})

def string_to_pdf(request, data):
    filename = 'so.pdf'
    pdf = pdfkit.from_string(data, filename)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="' + filename + '"'

    return response

def pdf(request):
    # Create a URL of our project and go to the template route
    projectUrl = request.get_host()+ "/contact/list"
    pdf = pdfkit.from_url(projectUrl, False)
    # Generate download
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="ourcodeworld.pdf"'
    return response

def contactAPI(request):
    contactList = Contact.objects.all()
    response = []
    for contact in contactList :
        response.append(contact.toDict())
    return HttpResponse(json.dumps(response))



