from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from property.models import Property


@login_required
def index(request):
    properties = Property.objects.filter(created_by=request.user)

    return render(request, 'dashboard/index.html', {
        'properties': properties,
    })
