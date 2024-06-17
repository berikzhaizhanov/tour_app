from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User
from .models import Member, Tour, OrderTour, Customer, Hotel, OrderHotel,Comment
from .forms import TourForm, CustomerForm, HotelForm,CommentForm,ReservationForm,ReservationHotelForm

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required



# --------- Site Pages ----------------

def index(request):
    tours = Tour.objects.all()
    todaysDate = datetime.today()
    print( todaysDate)
    return render(request, 'blog/index.html', {'tours': tours, 'todaysDate': todaysDate})


def search_tours(request):
    tours = Tour.objects.all()
    searched_tours = {}

    if request.method == 'POST':
        tourName = request.POST["tourName"]
        tourTravellers = request.POST["tourTravellers"]
        tourDate = request.POST["tourDate"]
        print(tourName)
        print(tourDate)
        if tourName == "none":
            print("with none")
            searched_tours = tours.filter(started__gt=tourDate) #Больше чем, >
        else:
            print("without none")
            searched_tours = tours.filter(name__contains=tourName) | tours.filter(started__gt=tourDate)

    return render(request, 'blog/tours.html', {'tours': tours, 'searched_tours': searched_tours})


def contact(request):
    members = Member.objects.all()

    return render(request, 'blog/contact.html', {'team': team_members, 'members': members})


def about(request):
    if request.method == 'POST':
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        text = request.POST["text"]

        subject = 'Welcome to Tour-de-Qaz!'
        message = f'Hi {name}, we are nice to see you! Your number - {phone}, Your email - {email}, Your text - {text}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list)
    return render(request, 'blog/about.html', {'team': team_members})


def services(request):
    hotels = Hotel.objects.all()
    context = {'hotels':hotels}
    return render(request, 'blog/services.html', context)



def checkout(request):
    return render(request, 'blog/checkout.html')

# ------------- Tour operations -----------------
@login_required(login_url='blog:login')
def addTour(request):
    # create object of form
    form = TourForm(request.POST or None, request.FILES or None)

    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        form.save()
        messages.info(request, "The tour added successfully!")
        return HttpResponseRedirect("/tours_list")

    return render(request, 'blog/../../templates/admin/add_tour.html', {'form': form})


@login_required(login_url='blog:login')
def tour_edit(request, id):
    tour = Tour.objects.get(id=id)
    form = TourForm(instance=tour)

    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            form.save()
            messages.info(request, "The tour updated successfully!")
            return HttpResponseRedirect("/tours_list")

    return render(request, 'blog/../../templates/admin/tour_edit.html', {'form': form})


def detail_view(request, id):
    tour = Tour.objects.get(id = id)
    comments = Comment.objects.filter(tour_id = id)
    new_comment = None
    if request.method == 'POST':
        comments_form = CommentForm(request.POST)
        if comments_form.is_valid():
            new_comment = comments_form.save(commit = False)
            new_comment.tour_id = tour
            new_comment.save()
            return redirect("blog:detail_view", id=id)
    else:
        comments_form = CommentForm()

    return render(request, "blog/detail_view.html", {'tour':tour, 'comments':comments,'comments_form':comments_form})

@login_required(login_url='blog:login')
def reservation_view(request,id):
    tour = Tour.objects.get(id = id)
    if request.method == 'POST':
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid():
            reservation_comment = reservation_form.save(commit = False)
            reservation_comment.tour_id = tour
            reservation_comment.save()
            messages.info(request, "Сіз турды сәтті брондадыңыз")
            return redirect("blog:detail_view", id=id)
    else:
        reservation_form = ReservationForm()
    return render(request, "blog/reservation_view.html", {'reservation_form':reservation_form})


def tour_detail(request, id):
    tour = Tour.objects.get(id = id)
    return render(request, "admin/tour_detail.html", {'tour':tour})


@login_required(login_url='blog:login')
def tour_delete(request, id):
    context = {'id':id}

    # fetch the object related to passed id
    obj = get_object_or_404(Tour, id=id)

    if request.method == "POST":
        if request.POST.get('submit') == 'Yes':
            obj.delete()
            messages.info(request, "The tour Deleted successfully!")
            return HttpResponseRedirect("/tours_list")
        else:
            return HttpResponseRedirect("/tours_list")

    return render(request, "blog/../../templates/admin/tour_delete.html", context)


def tours(request):
    tours = Tour.objects.all()
    # tours.count()
    return render(request, 'blog/tours.html', {'tours': tours})


def tours_list(request):
    context = {'tours': Tour.objects.all()}
    return render(request, 'admin/tours_list.html', context)

# ------------ Login / Sign UP operations -----------------
def signUp_view (request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:tours')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/sign_up.html', {'form':form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('blog:tours')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('blog:index')


@login_required(login_url='blog:login')
def base_admin_view(request):
    return render(request, 'admin/base_admin.html')


@login_required(login_url='blog:login')
def add_to_cart(request, id):
    tour = get_object_or_404(Tour, id=id)
    # tour = Tour.objects.filter(id=id)

    order_item, created = OrderTour.objects.get_or_create(
        tour=tour,
        customer=request.user,
        ordered=True,
    )
    if created:
        messages.info(request, "сәтті қосылды")
        return redirect("blog:tours")
    else:
        order_item.save()
        messages.info(request, "сәтті қосылды")
        return redirect("blog:tours")


@login_required
def order(request):
    orders = OrderTour.objects.filter(customer=request.user)
    context = {
        'orders': orders,

    }
    return render(request, 'admin/user/user_order.html', context)


@login_required
def users_list(request):
    orders = OrderTour.objects.filter(customer=request.user, ordered=True)
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'admin/user/users_list.html', context)


@login_required
def user_detail(request, id):
    user = User.objects.filter(id=id)
    user_orders = user[0].ordertour_set.all()
    context = {
        'users': user,
        'user_orders': user_orders,
    }
    return render(request, 'admin/user/user_detail.html', context)


@login_required
def order_delete(request, id):
    context = {'id':id}
    order = get_object_or_404(OrderTour, id=id)

    if request.method == "POST":
        order.delete()
        messages.info(request, "Тур сәтті жойылды!")
        return HttpResponseRedirect("/order")

    return render(request, 'admin/user/user_order_delete.html')


# ----------- Hotel views --------------------
@login_required(login_url='blog:login')
def addHotel(request):
    form = HotelForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.info(request, "Қонақ үй сәтті қосылды!")
            return HttpResponseRedirect("hotels_list")

    return render(request, 'admin/hotel/add_hotel.html', {'form': form})


@login_required(login_url='blog:login')
def hotel_edit(request, id):
    hotel = Hotel.objects.get(id=id)
    form = HotelForm(instance=hotel)

    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            messages.info(request, "The "+hotel.name+" edited successfully!")
            return HttpResponseRedirect("/hotel/" + id)

    return render(request, 'admin/hotel/hotel_edit.html', {'form': form})


@login_required(login_url='blog:login')
def hotel_delete(request, id):
    context = {'id':id}

    # fetch the object related to passed id
    obj = get_object_or_404(Hotel, id=id)

    if request.method == "POST":
        if request.POST.get('submit') == 'Yes':
            obj.delete()
            messages.info(request, "Қонақ үй сәтті жойылды!")
            return HttpResponseRedirect("/hotel/hotels_list")
        else:
            return HttpResponseRedirect("/hotel/hotels_list")

    return render(request, "admin/hotel/hotel_delete.html", context)


def hotels_list(request):
    hotels = Hotel.objects.all()
    return render(request, "admin/hotel/hotels_list_admin.html", {'hotels': hotels})


def hotel_detail_admin(request, id):
    hotel = Hotel.objects.get(id=id)
    return render(request, "admin/hotel/hotel_detail_admin.html",{'hotel':hotel})


def hotel_detail(request, id):
    hotel = Hotel.objects.get(id=id)
    return render(request, "admin/hotel/hotel_detail.html",{'hotel': hotel})

@login_required(login_url='blog:login')
def reservation_hotel_view(request,id):
    hotel = Hotel.objects.get(id=id)
    if request.method == 'POST':
        reservation_form = ReservationHotelForm(request.POST)
        if reservation_form.is_valid():
            reservation_comment = reservation_form.save(commit = False)
            reservation_comment.hotel_id = hotel
            reservation_comment.save()
            messages.info(request, "Сіз қонақүйді сәтті брондадыңыз")
            return redirect("blog:hotel_detail", id=id)
    else:
        reservation_form = ReservationHotelForm()
    return render(request, "blog/reservation_hotel_view.html", {'reservation_form':reservation_form})


# ----------- Hotel Orders -------------
@login_required(login_url='blog:login')
def orderHotel(request, id):
    hotel = get_object_or_404(Hotel, id=id)

    order_item = OrderHotel.objects.get_or_create(
        hotel=hotel,
        customer=request.user,
    )
    if order_item:
        messages.info(request, "себетіңізге қосылды")
        return redirect("blog:services")


@login_required(login_url='blog:login')
def myHotelOrders(request):
    orders = OrderHotel.objects.filter(customer=request.user)
    print("222")
    context = {'orders': orders}
    return render(request, "admin/hotel/hotel_orders_admin.html", context)


@login_required
def orderHotelDelete(request, id):
    order = get_object_or_404(OrderHotel, id=id)

    if request.method == "POST":
        order.delete()
        messages.info(request, "Қонақ үй сәтті жойылды!")
        return HttpResponseRedirect("/myHotelOrders")

    return render(request, 'admin/hotel/hotel_order_delete.html')

