from django.shortcuts import render, redirect
from .models import Announcement, Video, Review
from .forms import ReviewForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse


def interactive_page(request):
    announcements = Announcement.objects.order_by('-created_at')[:5]  
    videos = Video.objects.order_by('-uploaded_at')
    reviews = Review.objects.order_by('-created_at')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('interactive_page')  
    else:
        form = ReviewForm()

    context = {
        'announcements': announcements,
        'videos': videos,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'support/interactive_page.html', context)




@user_passes_test(lambda u: u.is_staff)  
def delete_review(request, id):
    review = get_object_or_404(Review, id=id)
    review.delete()
    return redirect('interactive_page')


def submit_review(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:  
            Review.objects.create(content=content) 
        return redirect('interactive_page') 
    return HttpResponse(status=405)  
