from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Roadmap


@login_required
def roadmap_view(request, roadmap_id):
    roadmap = get_object_or_404(
        Roadmap,
        id=roadmap_id,
        user=request.user
    )

    return render(request, 'roadmap/roadmap.html', {
        'roadmap': roadmap,
        'items': roadmap.items.all()
    })
    