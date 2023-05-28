from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewPropertyForm, EditPropertyForm
from .models import Category, Property


def get_properties(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    properties = Property.objects.filter(is_sold=False)

    if category_id:
        properties = properties.filter(category_id=category_id)

    if query:
        properties = properties.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'property/properties.html', {
        'properties': properties,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })


def get_property_details(request, pk):
    property_object = get_object_or_404(Property, pk=pk)
    related_items = Property.objects.filter(category=property_object.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'property/detail.html', {
        'property': property_object,
        'related_items': related_items
    })


@login_required
def create_new_property(request):
    if request.method == 'POST':
        form = NewPropertyForm(request.POST, request.FILES)

        if form.is_valid():
            property_object = form.save(commit=False)
            property_object.created_by = request.user
            property_object.save()

            return redirect('property:get_property_details', pk=property_object.id)
    else:
        form = NewPropertyForm()

    return render(request, 'property/form.html', {
        'form': form,
        'title': 'New property',
    })


@login_required
def edit_property(request, pk):
    property_object = get_object_or_404(Property, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditPropertyForm(request.POST, request.FILES, instance=property_object)

        if form.is_valid():
            form.save()

            return redirect('property:get_property_details', pk=property_object.id)
    else:
        form = EditPropertyForm(instance=property_object)

    return render(request, 'property/form.html', {
        'form': form,
        'title': 'Edit property',
    })


@login_required
def delete_property(request, pk):
    property_object = get_object_or_404(Property, pk=pk, created_by=request.user)
    property_object.delete()

    return redirect('dashboard:index')
