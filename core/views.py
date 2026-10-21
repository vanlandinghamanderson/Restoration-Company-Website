from django.shortcuts import render, get_object_or_404, redirect
from .models import CarouselBackground, Post, Service, Certification, Review, Team, Project
from .forms import CustomerForm
from django.contrib import messages as message
from django.views.decorators.http import require_POST
from django.http import JsonResponse



# Home Page
def index(request):
    restoration_carousel_background = CarouselBackground.objects.filter(is_active=True).order_by('order')
    reviews = Review.objects.filter(is_active=True)
    restoration_certifications = Certification.objects.filter(is_active=True)
    projects = Project.objects.filter(is_published=True)[:3] #Slices 3
    posts = Post.objects.filter(is_published=True)[:4] #Slices 4
    return render(request, 'core/index.html', {
        'restoration_carousel_background': restoration_carousel_background,
        'reviews': reviews,
        'restoration_certifications': restoration_certifications,
        'projects': projects,
        'posts': posts, 
    })

# Gallery Page
def gallery(request):
    projects = Project.objects.filter(is_published=True)
    return render(request, 'core/gallery.html', {
        'projects':projects,
        'active_service':False,
    })

# About Us Page
def about(request):
    certifications = Certification.objects.filter(is_active=True)
    teams = Team.objects.filter(is_active=True)
    reviews = Review.objects.filter(is_active=True)
    return render(request, 'core/about.html', {
        'certifications': certifications,
        'teams': teams,
        'reviews': reviews,
    })
                  

def _contact_initial(slug):
    """Pre-fill the contact when arriving from a 'Request This Service' """
    if not slug:
        return {}
    service = Service.objects.filter(slug=slug, is_active=True).first()
    if not service:
        return {}
    return {
        'requested_service': service,
        'message': f"I'd like to request {service.name} service."
    }

# Contact Page
# 'if request.method == 'POST' is after a customer writes a message, that's for the submit button, otherwise it's an empty form
# 'form = CustomerForm(request.POST) is for a customer who fills in the form and submits it, the data is sent to the server and stored in the database
# 'if form.is_valid()' is for the server to check if the data is valid, if it is valid, it will be saved in the database
def contact(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            message.success(request, 'Thank you for your message! We will get back to you as soon as possible.')
            return redirect('contact')
    else: 
        form = CustomerForm(initial=_contact_initial(request.GET.get('requested_service')))
    return render(request, 'core/contact.html', {
        'form': form})

# Contact API
# '@required_POST' means only accept submissions (GET gets a 405)
# 'form = CustomerForm(request.POST)' same as contact view
#  If the form is valid, it saves the database prints as 200 ok, otherwise it prints as 400 bad request
@require_POST
def contact_api(request):
    form = CustomerForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'ok': True}, status=200)
    return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

# Our Services Page
def service_list(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'core/service_list.html', {
        'services': services,
    })

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(request, 'core/service_detail.html', {
        'service':service,
    })

# Blog List Page
def blog_list(request):
    service_filter = request.GET.get('service')
    restoration_posts = Post.objects.all()
    restoration_services = Service.objects.filter(is_active=True)
    active_service = None
    if service_filter:
        restoration_posts = restoration_posts.filter(related_service__slug=service_filter)
        active_service = service_filter
    return render(request, 'core/blog_list.html', {
        'restoration_posts': restoration_posts,
        'restoration_services': restoration_services,
        'active_service': active_service,
    })

# Blog Detail Page
def blog_detail(request, slug):
    """
    Render a single blog post page

    Looks up the post by its URL slug and finds a few related posts
    that share the same service
    """

    # Gets the published post matching this slug, otherwise show a 404 page
    post = get_object_or_404(Post, slug=slug, is_published=True)

    # Up to 3 other published posts about the same service
    related_posts = Post.objects.filter(
        is_published=True, related_service=post.related_service
    ).exclude(pk=post.pk)[:3]

    return render(request, 'core/blog_detail.html', {
        'restoration_post': post,
        'restoration_related_posts': related_posts,
        'page_title': post.title,
    })

