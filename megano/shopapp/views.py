import datetime
import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.db.models import Count, Min, Sum
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, translate_url
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormMixin

from cart.forms import CartAddProductForm
from megano import settings
from pay.models import Order

from .comparison import Comparison
from .forms import ReviewForm
from .models import Product


class ProductDetailView(
    FormMixin,
    DetailView,
):
    """Класс детальной страницы товаров"""

    model = Product
    template_name = "shopapp/product_detail.html"
    context_object_name = "product"
    form_class = ReviewForm
    success_msg = "Отзыв успешно создан"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        if self.request.user.is_authenticated:
            ViewHistory.objects.create(user=self.request.user, product=product)
        product_sellers = product.product_sellers.filter(quantity__gt=0).order_by(
            "price"
        )
        context["product_sellers"] = product_sellers

        if product_sellers:
            min_price_product_seller = product_sellers.first()
            context["min_price_product_seller"] = min_price_product_seller

        cart_product_form = CartAddProductForm()
        context["cart_product_form"] = cart_product_form
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("shopapp:product", kwargs={"pk": self.get_object().id})

    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.product = self.get_object()
        self.object.save()
        return super().form_valid(form)


from .models import Categories, Discount, Product, ProductSeller, Seller, ViewHistory


@method_decorator(cache_page(60 * 60), name="dispatch")
class SellerDetailView(DetailView):
    model = Seller
    template_name = "shopapp/seller_detail.html"
    context_object_name = "seller"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller = self.get_object()
        top_products = get_top_products(seller)
        context["top_products"] = top_products
        return context


def get_top_products(seller):
    pass


class DiscountListView(ListView):
    template_name = "shopapp/discount_list.html"

    def get_queryset(self, **kwargs):
        discounts = Discount.objects.only(
            "name", "description", "date_start", "date_end"
        ).prefetch_related("products")
        return discounts


class DiscountDetailView(DetailView):
    model = Discount
    template_name = "shopapp/discountdetails.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = []
        for product in context["discount"].products.all():
            price = ProductSeller.objects.only("price").filter(product=product).first()
            price = getattr(price, "price")
            discounted_price = price
            discount = context["discount"]
            if discount.type == "%":
                discounted_price = price - (price * discount.value / 100)
                discounted_price = round(discounted_price, 2)
            elif discount.type == "RUB":
                discounted_price = price - discount.value
            product.price = discounted_price
            products.append(product)
        context["products"] = products
        return context


class MainPageView(TemplateView):
    template_name = "shopapp/index.html"

    def create_new_limited_discount(self):
        random_product = Product.objects.all().order_by("?")
        if random_product:
            random_product = random_product.first()
            new_discount = Discount.objects.create(
                name="Ограниченная скидка",
                date_start=datetime.datetime.today(),
                date_end=datetime.datetime.today() + timedelta(days=1),
                promocode="LIMITED",
                is_group=False,
                is_active=True,
                value=10,
            )
            random_product.discount_set.add(new_discount)
            new_discount.save()
        return random_product

    def get_limited_offer(self):
        limited_offer = Discount.objects.filter(
            promocode="LIMITED", is_active=1
        ).first()
        if limited_offer:
            if limited_offer.date_end.date() != datetime.datetime.today().date():
                limited_product = limited_offer.products.all().first()
            else:
                limited_offer.is_active = False
                limited_offer.save()
                limited_product = self.create_new_limited_discount()
        else:
            limited_product = self.create_new_limited_discount()

        if limited_offer:
            discount = limited_offer.value
        else:
            discount = Discount.objects.filter(promocode="LIMITED", is_active=1).first()
            if not discount:
                discount = None
            else:
                discount = discount.value
        return limited_product, discount

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_order_products = ProductSeller.objects.annotate(
            cnt=Count("order_items")
        ).order_by("-cnt")[:8]
        limited_product, discount = self.get_limited_offer()
        if limited_product:
            product_seller = ProductSeller.objects.filter(
                product_id=limited_product.id
            ).first()
            if product_seller and discount:
                costs = {
                    "old_cost": product_seller.sale,
                    "new_cost": int(product_seller.sale) - int(discount),
                }
                context["limited_cost"] = costs

        context["limited_product"] = limited_product
        context["top_order_products"] = top_order_products

        if self.request.user.is_authenticated:
            view_history = self.request.user.view_history.select_related(
                "product"
            ).order_by("-creation_date")[:8]

            eight_viewed = []

            if view_history:
                for history in view_history:
                    history.product.price = (
                        ProductSeller.objects.only("price")
                        .filter(product=history.product)
                        .first()
                    )
                    history.product.price = history.product.price.price
                    eight_viewed.append(history.product)
                context["eight_viewed"] = eight_viewed

        return context


class AccountDetailView(UserPassesTestMixin, DetailView):
    model = User
    template_name = "shopapp/account.html"

    def test_func(self):
        return self.request.user.is_authenticated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.request.user.profile

        view_history = self.request.user.view_history.select_related(
            "product"
        ).order_by("-creation_date")[:3]
        three_viewed = []
        if view_history:
            for history in view_history:
                history.product.price = (
                    ProductSeller.objects.only("price")
                    .filter(product=history.product)
                    .first()
                )
                history.product.price = history.product.price.price
                three_viewed.append(history.product)
            context["three_viewed"] = three_viewed

        orders = self.request.user.orders.all()
        if orders.exists():
            last_order = orders.latest("created_at")
            context["last_order"] = last_order
            last_order_item = last_order.order_items.latest("id")
            context["last_order_item"] = last_order_item

        return context


class ProfileUpdateView(UserPassesTestMixin, TemplateView):
    template_name = "shopapp/profile.html"

    def test_func(self):
        return self.request.user.is_authenticated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        user = self.request.user
        if request.method == "POST":
            if request.FILES:
                image = request.FILES["avatar"]
                fs = FileSystemStorage(
                    location=f"/uploads/users/user_{self.request.user.pk}/avatar/{image.name}"
                )
                print(fs.base_location)
                img_name = fs.save(image.name, image)
                print(img_name)
                img_url = fs.url(img_name)
                print(img_url)
                user.profile.avatar = img_url

            user.username = request.POST.get("name")
            if request.POST.get("password") == request.POST.get("passwordReply"):
                user_p = User.objects.get(username=user.username)
                user_p.set_password = request.POST.get("password")
                user_p.save()
            user.email = request.POST.get("mail")
            user.profile.phone = request.POST.get("phone")
            user.profile.phone = request.POST.get("phone")
            user.save()
            user.profile.save()
        return redirect(request.path)


class HistoryOrder(ListView):
    """
    This page displays all customer's orders
    """

    model = Order
    template_name = "shopapp/historyorder.html"

    def test_func(self):
        return self.request.user.is_authenticated

    def get_context_data(self, **kwargs):
        context = {}
        history_orders = self.request.user.orders.order_by("-created_at")
        for order in history_orders:
            context[order] = order.order_items.only("price").aggregate(Sum("price"))
            context[order] = context[order]["price__sum"]
        return {"history_orders": context}


class OrderDetailView(DetailView):
    """
    This page displays the details of the chosen order
    """

    model = Order
    template_name = "shopapp/oneorder.html"

    def test_func(self):
        return self.request.user.is_authenticated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        context["items"] = self.object.order_items.prefetch_related("product").all()
        context.update(self.object.order_items.only("price").aggregate(Sum("price")))
        return context


class LastOrderDetailView(DetailView):
    """
    This page displays the details of the last user's order
    """

    model = User
    template_name = "shopapp/oneorder.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            order = Order.objects.latest()
            context["items"] = order.order_items.prefetch_related("product")
            context.update(order.order_items.only("price").aggregate(Sum("price")))
        except Order.DoesNotExist:
            order = None
            context["items"] = None
        context["order"] = order
        return context


@method_decorator(csrf_exempt, name="dispatch")
class CompareManager(TemplateView):
    template_name = "shopapp/comparison.html"

    def get_context_data(self, **kwargs):
        context = super(CompareManager, self).get_context_data(**kwargs)
        products = tuple(product for product in Comparison(self.request))
        similar = Comparison.get_similar(products)
        for product in products:
            product_id = product.get("id")
            sim = similar.get(str(product_id))
            product["similar"] = sim
        context["products"] = products
        return context

    def post(self, request, *args, **kwargs):
        body_data = json.loads(request.body)
        pk = body_data["product_pk"]
        product = (
            ProductSeller.objects.filter(product_id=pk)
            .prefetch_related("product")
            .first()
        )
        Comparison(request).add(product)
        return JsonResponse({"status": "ok"})
        # return render(request, self.request.META.get("HTTP_REFERER"))

    def delete(self, request, *args, **kwargs):
        body_data = json.loads(request.body)
        pk = body_data["product_pk"]
        product = (
            ProductSeller.objects.filter(product_id=pk)
            .prefetch_related("product")
            .first()
        )
        Comparison(request).remove(product)
        return JsonResponse({"status": "ok"})
        # return render(request, self.request.META.get('HTTP_REFERER'))


class CatalogView(ListView):
    def get(self, request, pk, *args, **kwargs):
        category = Categories.objects.filter(pk=pk).first()
        sort = request.GET.get("param")
        products = Product.objects.filter(category=category).annotate(
            min_price=Min("product_sellers__price"),
            pop=Count("product_sellers__order_items"),
            reviews=Count("reviews_product"),
        )

        price_from = request.GET.get("priceFrom")
        price_to = request.GET.get("priceTo")
        name_filter = request.GET.get("nameFilter")
        descriptionFilter = request.GET.get("descriptionFilter")

        if price_from and price_to:
            products = products.filter(
                min_price__gte=price_from, min_price__lte=price_to
            )
        if name_filter:
            products = products.filter(name__icontains=name_filter)
        if descriptionFilter:
            products = products.filter(description__icontains=descriptionFilter)

        if sort == "price":
            products = products.order_by("min_price")
        elif sort == "popularity":
            products = products.order_by("-pop")
        elif sort == "novelty":
            products = products.order_by("-created_at")
        elif sort == "reviews":
            products = products.order_by("-reviews")
        else:
            products = products.order_by("id")

        paginator = Paginator(products, 3)

        seller = ProductSeller.objects.all()

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        if pk:
            cache_key = f"catalog_{pk}"
            products = cache.get(cache_key)
            if not products:
                cache.set(cache_key, products, timeout=86400)
        else:
            cache_key = "catalog_all"
            products = cache.get(cache_key)
            if not products:
                cache.set(cache_key, products, timeout=86400)

        context = {
            "category": category,
            "page_obj": page_obj,
            "seller": seller,
        }
        return render(request, "shopapp/catalog.html", context)


@login_required
def set_language(request):
    next_url = request.META.get("HTTP_REFERER")
    response = HttpResponseRedirect(next_url)
    lang_code = request.GET.get("l")
    next_trans = translate_url(next_url, lang_code)
    if next_trans != next_url:
        response = HttpResponseRedirect(next_trans)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response
