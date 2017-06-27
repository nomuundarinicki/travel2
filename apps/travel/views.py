from django.shortcuts import render, redirect
from .models import Place, Trip, Review
from ..loginreg.models import User
from django.core.urlresolvers import reverse
# Create your views here.

def index(request):
    if not 'id' in request.session:
        return redirect(reverse('login:index'))
    if not 'errors' in request.session:
        request.session['errors'] = []
    context = {
        'user': User.manager.get(id=request.session['id']),
        'reviews': Review.objects.all().order_by('-created_at')[:5],
        'Trips': Trip.objects.all().order_by('title')
    }
    return render(request, 'travel/index.html', context)

def show(request, id):
    if not 'id' in request.session:
        return redirect(reverse('login:index'))
    if not 'errors' in request.session:
        request.session['errors'] = []
    reviews = Review.objects.all().filter(Trip_id=id)
    context = {
        'reviews': reviews,
        'Trip': reviews[0].Trip
    }
    return render(request, 'travel/show.html', context)

def add(request):
    if not 'id' in request.session:
        return redirect(reverse('login:index'))
    if not 'errors' in request.session:
        request.session['errors'] = []
    context = {
        'places': Place.objects.all().order_by('name'),
        'errors': request.session.pop('errors')
    }
    return render(request, 'travel/add.html', context)

def addtoexisting(request, id):
    if not 'id' in request.session:
        return redirect(reverse('login:index'))
    if not request.method=='POST':
        return redirect(reverse('Trips:show', kwargs={'id':id}))
    if len(request.POST['review']) == 0:
        request.session.errors.append('Must have a review!')
        return redirect(reverse('Trips:show', kwargs={'id':id}))

    b = Trip.objects.get(id=id)
    Review.objects.create(user=User.manager.get(id=request.session['id']), Trip=b, rating=request.POST['rating'], review=request.POST['review'])
    return redirect(reverse('Trips:show', kwargs={'id':id}))

def create(request):
    if not 'id' in request.session:
        return redirect(reverse('login:index'))
    if not request.method=='POST':
        return redirect(reverse('Trips:add'))
    if len(request.POST['title']) == 0 or len(request.POST['review']) == 0:
        request.session.errors.append('Must have a title and a review!')
        return redirect(reverse('Trip:add'))

    if len(request.POST['']) == 0:
        b = Trip.objects.create(title=request.POST['title'], place=Place.objects.get(id=request.POST['placeselect']))
        Review.objects.create(user=User.manager.get(id=request.session['id']), Trip=b, rating=request.POST['rating'], review=request.POST['review'])
    else:
        a = Place.objects.create(name=request.POST[''])
        b = Trip.objects.create(title=request.POST['title'], place=a)
        Review.objects.create(user=User.manager.get(id=request.session['id']), Trip=b, rating=request.POST['rating'], review=request.POST['review'])
    return redirect(reverse('Trips:show', kwargs={'id':b.id}))

def delete(request, id):
    r = Review.objects.get(id=id)
    if request.session['id']==r.user.id:
        r.delete()
    return redirect(reverse('Trips:index'))
