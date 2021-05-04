from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Order, Orderitem, Profile, BillingAddress,SubscribeRecipients,Category,Review
from django.utils import timezone
from django.views.generic import View
from .forms import CheckoutForm,SubscribeForm,ReviewForm
from .emails import send_welcome_email


def index(request):
    return render(request, 'index.html')


def products(request):
    items = Item.objects.all()
    categories = Category.get_category()
    return render(request, 'shop.html', {"items": items, 'categories':categories})


def product_category(request, category):
    items = Item.filter_by_category(category)
    categories = Category.get_category()
    context = {
        'items':items,
        'categories':categories
    }
    return render(request, 'shop.html', context)


def product_details(request, id):
    product_item = Item.objects.filter(id=id)
  
    return render(request, "product_details.html", {"product_item": product_item})


def shippingpolicy(request):
    return render(request, "shippingpolicy.html")


class OrderSummary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "order_summary.html", context)
        except ObjectDoesNotExist:
            messages.error(request, "You do not have an active order")
            return redirect("/")


def my_profile(request):
    current_user = request.user
    return render(request, 'profile.html')


@login_required
def add_to_cart(request, id):
    item = get_object_or_404(Item, id=id)
    order_item, created = Orderitem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        # check if order item is in the order
        if order.items.filter(item_id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order_summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item  was added to your cart.")
            return redirect("order_summary")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item  was added to your cart.")
        return redirect("order_summary")


@login_required
def remove_from_cart(request, id):
    item = get_object_or_404(Item, id=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in the order
        if order.items.filter(item_id=item.id).exists():
            order_item = Orderitem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item  was removed from your cart.")
            return redirect("order_summary")
        else:
            messages.info(request, "This item  was not in your cart.")
            return redirect("order_summary")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("order_summary")


def search_item(request):
    if 'title' in request.GET and request.GET["title"]:
        search_term = request.GET.get("title")
        search_item = Item.search_by_title(search_term)
        message = f"{search_term}"
        return render(request, "search.html", {"message": message, "items": search_item})
    else:
        messages.info(request, "You haven't searched for any term")
        return render(request, 'search.html')


def remove_single_item(request, id):
    item = get_object_or_404(Item, id=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in the order
        if order.items.filter(item_id=item.id).exists():
            order_item = Orderitem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            # if quantity is  0
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()

            else:
                order.items.remove(order_item)

            messages.info(request, "This item  quantity was updated.")
            return redirect("order_summary")
        else:
            messages.info(request, "This item  was not in your cart.")
            return redirect("product", id=id)
    else:
        messages.info(request, "You don't have an active order")
        return redirect("product", id=id)

# def add_review(request, item_id):
#     current_user = request.user
#     product_items = Item.objects.filter(id=item_id).first()
#     if request.method == 'POST':
#         form = ReviewForm(request.POST, request.FILES)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.reviewer = current_user
#             review.review_title = product_items
#             review.review_body = product_items
#             review.save()
#             return HttpResponseRedirect(request.path_info)
    
#     else:
#         form = ReviewForm()
#     return render(request, 'product_details.html', {"form":form, "item_id":item_id})        


class CheckoutView(View):
    def get(self, *args, **kwargs):
        # form
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            city = form.cleaned_data.get('city')
            country = form.cleaned_data.get('country')
            zipcode = form.cleaned_data.get('zipcode')
            phone = form.cleaned_data.get('phone')
            # TODO: add functionalities to this fields
            # same_billing_address = form.cleaned_data.get(
            #     'same_billing_address')
            # save_info = form.cleaned_data.get('save_info')
            payment_option = form.cleaned_data.get('payment_option')

            billing_address = BillingAddress(
                user=self.request.user,
                firstname=firstname,
                lastname=lastname,
                street_address=street_address,
                apartment_address=apartment_address,
                city=city,
                country=country,
                zipcode=zipcode,
                phone=phone,
            )
            billing_address.save()
            order.billing_address = billing_address
            order.save()
            return redirect('checkout')
        except ObjectDoesNotExist:
            messages.error(request, "You do not have an active order")
            return redirect("order_summary")

        messages.warning(self.request, "Failed checkout")
        return redirect('checkout')


def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']
            recipient = SubscribeRecipients(name=name,email=email)
            recipient.save()
            HttpResponseRedirect('subscribe')
        else:
            form = SubscribeForm()
        return render(request, "subscribe.html")        