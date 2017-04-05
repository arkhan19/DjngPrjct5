from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
# Create your views here.
from posts.models import Posts  # model class
from Products.models import ProductFeatured


def home(request):
    homies = Posts.objects.order_by('pub_date')
    featured_image = ProductFeatured.objects.first()

    return render(request, 'posts/home.html', {'post_obj_for_html': homies, 'featured_image':featured_image}) # Context


@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['u_r_l']:
            email = EmailMessage('Registered on DJNG PRJCT 3', 'Confirmation Mail of Registration',
                                 to=[request.POST['u_r_l']])
            post_object = Posts()
            post_object.title = request.POST['title']
            post_object.url = request.POST['u_r_l']
            post_object.author = request.user
            post_object.pub_date = timezone.datetime.now()
            post_object.save(request)
            # send_mail(
            #     'Subject is here',
            #     'Here is the message.',
            #     settings.EMAIL_HOST_USER,
            #     [request.POST['u_r_l']],
            #     fail_silently=True,
            # )
            email.send()
            return redirect('home')
        else:
            return render(request, 'posts/create.html', {'error': 'Enter Title Please, Post not created, try again.'})
    else:
        return render(request, 'posts/create.html')


def __str__(self):
    return '%s' % self.title


@login_required
def c_up(request, pk):
    if request.method == 'POST':
        #  model's primary key
        counter = Posts.objects.get(pk=pk)
        counter.commends +=1
        counter.save()
        return redirect('home')

@login_required
def c_down(request, pk):
    #  model's primary key
    if request.method == 'POST':
        counter = Posts.objects.get(pk=pk)
        counter.commends -=1
        counter.save()
        return redirect('home')

@login_required
def auser(request, fk):
    bar = Posts.objects.order_by('pub_date').filter(author_id=fk)
    # bar = use.author.filter(name__contains=str(fk))
    return render(request, 'posts/author.html', {'foo': bar}, {'ray': fk})












