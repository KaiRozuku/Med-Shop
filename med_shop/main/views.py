from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView


from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .forms import ProfilePictureForm
from .models import Drug, Cart, Category, Profile


def index(request, category_id=None):
    context = {
        'drugs': Drug.objects.all(),
        'categories': Category.objects.all()
    }
    if category_id:
        context.update({'drugs': Drug.objects.filter(category_id=category_id)})
    else:
        context.update({'drugs': Drug.objects.all()})

    return render(request, 'main/index.html', context=context)


def about(request):
    return render(request, "main/about.html")


def logout_user(request):
    logout(request)
    return redirect('home')


def brown(request):
    return render(request, 'main/brown.html')


def show_drug(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)
    other_drugs = get_object_or_404(Drug, id=drug_id)[:2]

    context = {
        'drug': drug,
        'title': drug.name,
        'dr_select': drug_id,
        'other_drugs': other_drugs
    }
    return render(request, 'main/drug.html', context=context)


def show_cart(request):
    carts = Cart.objects.filter(user=request.user)
    total_quantity = sum(cart.quantity for cart in carts)
    total_price = sum(cart.sum for cart in carts)

    context = {
        'carts': carts,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }

    return render(request, 'main/cart.html', context=context)


def cart_add(request, drug_id):
    current_page = request.META.get('HTTP_REFERER')
    drug = Drug.objects.get(id=drug_id)
    carts = Cart.objects.filter(user=request.user, drug=drug)

    if not carts.exists():
        Cart.objects.create(user=request.user, drug=drug, quantity=1)
        return HttpResponseRedirect(current_page)
    else:
        cart = carts.first()
        cart.quantity += 1
        cart.save()
        return HttpResponseRedirect(current_page)


def cart_delete(request, drug_id):
    cart = Cart.objects.get(id=drug_id)
    cart.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DrugDetailView(DetailView):
    model = Drug
    template_name = 'main/drug-view.html'
    context_object_name = 'drug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Отримуємо поточний ліки
        drug = self.get_object()
        # Отримуємо список інших ліків, виключаючи поточний
        other_drugs = Drug.objects.exclude(pk=drug.pk)[:6]
        context['other_drugs'] = other_drugs
        return context


class LoginView(TemplateView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return render(request, self.template_name)

        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is None:
                context = {
                    "error": "Логін чи пароль неправильні"
                }
                return render(request, self.template_name, context)

            login(request, user)
            return redirect("profile")


class ProfilePage(TemplateView):
    template_name = "registration/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile, created = Profile.objects.get_or_create(user=self.request.user)
            context['profile_form'] = ProfilePictureForm(instance=profile)
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile_form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profile')
        return self.get(request, *args, **kwargs)


class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password == password2:
                try:
                    validate_password(password)
                except ValidationError as e:
                    # Якщо пароль не відповідає вимогам, повертаємо помилку користувачу
                    return render(request, self.template_name, {'error_message': e})

                User.objects.create_user(username, email, password)
                return redirect("login")
            else:
                return render(request, self.template_name, {'error_message': "Паролі не співпадають"})

        return render(request, self.template_name)


class Search(ListView):
    template_name = 'main/index.html'
    context_object_name = 'drug'

    def get_queryset(self):
        return Drug.objects.filter(name__iregex=self.request.GET.get('search'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drugs'] = self.get_queryset()
        context['search'] = self.request.GET.get('search')
        return context


def drug_view(request):
    sort_by = request.GET.get('sort_by')  # Отримайте параметр сортування з запиту GET
    if sort_by:
        if sort_by == 'name':
            drugs = Drug.objects.all().order_by('name')
        elif sort_by == 'price':
            drugs = Drug.objects.all().order_by('price')
        else:
            drugs = Drug.objects.all()
    else:
        drugs = Drug.objects.all()

    categories = Category.objects.all()  # Імпортуйте та отримайте категорії, якщо вони потрібні

    return render(request, 'main.html', {'drugs': drugs, 'categories': categories})


def search_view(request):
    query = request.GET.get('search')
    sort = request.GET.get('sort')
    drugs = Drug.objects.all()

    if query:
        drugs = drugs.filter(name__icontains=query)

    if sort == 'price-asc':
        drugs = drugs.order_by('price')
    elif sort == 'price-desc':
        drugs = drugs.order_by('-price')

    categories = Category.objects.all()  # Якщо у вас є категорії, додайте їх

    context = {
        'drugs': drugs,
        'search': query,
        'categories': categories
    }

    return render(request, 'main/template.html', context)
