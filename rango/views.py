from django.shortcuts import render

from django.http import HttpResponse

from rango.models import Category

from rango.models import Page

from rango.forms import CategoryForm

from django.shortcuts import redirect

from django.urls import reverse

from rango.forms import PageForm



def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    context_dict['extra'] = 'From the model solution on GitHub'

    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    
    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            form.save(commit=True)

            return redirect('/rango/')
            
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})



def add_page(request, category_name_slug):
    """
    Adds a new page to a specified category. Redirects to the app's home page if the category doesn't exist.
    On a POST request with valid form data, saves a new page under the category and redirects to the category's page.
    """
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        return redirect('/rango/')

    form = PageForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        page = form.save(commit=False)
        page.category = category  # Assign the page to the selected category
        page.views = 0  # Initialize page views
        page.save()
        return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))

    return render(request, 'rango/add_page.html', {'form': form, 'category': category})
