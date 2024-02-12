from django.shortcuts import render,redirect,get_object_or_404
from.models import Venue,Booking,Order
from.forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .forms import BookingForm,RatingForm
from datetime import datetime
import razorpay
import random
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

# Create your views here.

def index(request):
    venues = Venue.objects.all()
    first_three_venues = Venue.objects.all()[:3]

    # Query the next three venues from the database
    next_three_venues = Venue.objects.all()[3:6]
    # locations = venue.objects.filter()
    context = {
        "venue": venues,
        "first_three_venues": first_three_venues,
        "next_three_venues": next_three_venues,
    }

    return render(request, "index.html", context)
 
def viewDetails(request,vid):
    venues=Venue.objects.filter(vid=vid)
    print(venues)
    c={"first_three_venues":venues,
       "next_three_venues":venues
       
       }
    """ c['first_three_venues']= venues """
    return render(request,'viewDetails.html',c)




def viewVenue(request):
    if request.method == "GET":
        return redirect("/")
    else:
        loc = request.POST.get("loc")
        if loc:
            queryset = Venue.prod.get_location(loc)
            print(queryset)
            context = {
                "venues": queryset,
                "loc": loc,
            }
            return render(request, "viewVenue.html", context)
        
            
        else:
            return redirect("/")

     
def book_venue(request, vid):
    venue = get_object_or_404(Venue, pk=vid)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Access the booking_date directly from request.POST and validate manually
            date = request.POST.get('date')
            try:
                date = datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, 'Invalid date format. Please select a valid date.')
                return render(request, 'book_venue.html', {'form': form, 'venue': venue})
            
            # Check if the venue is already booked on this date
            if Booking.objects.filter(venue=venue, date=date).exists():
                messages.error(request, 'This venue is already booked on this date. Please select another date.')
                return render(request, 'book_venue.html', {'form': form, 'venue': venue})
            
            booking = form.save(commit=False)
            booking.user = request.user
            booking.venue = venue
            booking.date = date  # Set the booking_date manually
            booking.save()
            
            return redirect('payment.html')  # Adjust the redirect as needed

    else:
        form = BookingForm()
    
    return render(request, 'book_venue.html', {'form': form, 'venue': venue})

    
    
      
def register_user(request):
    form= CreateUserForm() 
    if request.method == "POST":
        form= CreateUserForm(request.POST)
        if form.is_valid(): #checking if data is valid
            form.save() # saving into the db
            print("USer created successfully")
            messages.success(request,("user created Successfully"))
            return redirect("/")
        
        else:
            print("Error")
            messages.error(request,("""Your password canÃ¢â‚¬â„¢t be too similar to your other personal information.
                                   Your password must contain at least 8 characters.
                                   Your password canÃ¢â‚¬â„¢t be a commonly used password.
                                   Your password canÃ¢â‚¬â„¢t be entirely numeric."""))
    c={'form':form}
    return render(request,"register.html",c)        




def login_user(request):
    
    if request.method=="POST":
        username=request.POST['username']
        password= request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            print("User Logged in Successfully")
            messages.success(request,("user login created Successfully"))
            return redirect("/")
        else:
            messages.error(request,("There was an error ,Try Again !!"))
            return redirect("login_user/")
    else:
        return render(request,"login.html")    


def logout_user(request):
    logout(request)
    messages.success(request,("Logged Out Successfully"))
    return redirect("/")

# Initialize Razorpay client
""" client = razorpay.Client(auth=("rzp_test_NrRhkRo3jmQAld", "bRhdIMqipkByzTXcIkfMc9bW")) """
"""  booking = Booking.objects.filter(user=request.user,is_completed=False) """

""" def payment(request):
    venue = get_object_or_404(Venue, pk=vid,user=request.user,is_completed=False)
    
    
    total_price=0
    for x in venue:
        total_price+=(x.venue.price * x.quantity)
        vid=x.vid 

    client = razorpay.Client(auth=("rzp_test_NrRhkRo3jmQAld", "bRhdIMqipkByzTXcIkfMc9bW"))  
    data={"amount": total_price * 100,
          "currency": "INR",
          "receipt": "vid"
          }   
    payment=client.booking.create(data = data)
    context={}
    context['data']=payment
    context['amount']=payment['amount']
    c=Booking.objects.filter(user=request.user) 
    venue.delete()  
    venue.update(is_completed=True)
    return render(request,"payment.html",context)  """
def makePayment(request):
    c=Venue.objects.filter(user=request.user)
    
    oid=random.randrange(1000,9999)
    for x in c:
        Order.objects.create(order_id=oid,vid=x.venue.vid,quantity=x.quantity,user=request.user)
    orders=Order.objects.filter(user=request.user,is_completed=False)
    
    total_price=0
    for x in orders:
        total_price+=(x.venue.price * x.quantity)
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_NrRhkRo3jmQAld", "bRhdIMqipkByzTXcIkfMc9bW"))
    data={"amount": total_price * 100,
          "currency": "INR",
          "receipt": "oid"}
    payment=client.order.create(data = data)
    context={}
    context['data']=payment
    context['amount']=payment['amount']
    c=Booking.objects.filter(user=request.user)
    c.delete()
    orders.update(is_completed=True)
    return render(request,"payment.html",context)

    
""" def payment(request, bid):
    # Assuming each booking is for a single venue and the price is fixed per booking
    booking = get_object_or_404(Booking, pk=bid, user=request.user, is_completed=False)
    
    # Since booking is a single object (due to get_object_or_404), no need to loop through
    total_price = booking.venue.price

    client = razorpay.Client(auth=("rzp_test_NrRhkRo3jmQAld", "bRhdIMqipkByzTXcIkfMc9bW"))  
    data = {
        "amount": total_price * 100,  # Razorpay expects the amount in the smallest currency unit (paisa for INR)
        "currency": "INR",
        "receipt": f"bid-{bid}"  # Modified to include bid for unique receipt identifier
    }
    payment = client.order.create(data=data)  # Assuming you meant client.order.create instead of client.booking.create
    context = {
        'data': payment,
        'amount': total_price
    }
    booking.is_completed = True  # Mark the booking as completed
    booking.save()  # Save the updated booking

    return render(request, "payment.html", context) """
    # Assuming 'amount' is in rupees, multiply by 100 to convert to paise
    # Razorpay expects the amount in the smallest currency unit (paise)
    
    
    
 
    
    
    
    
      
 
 
@login_required  # Ensure that only authenticated users can submit ratings
def rating(request, vid):
    venue = get_object_or_404(Venue, pk=vid)
    already_rated = venue.ratings.filter(user=request.user).exists()

    if request.method == 'POST':
        if already_rated:
            # Handle the case where the user has already rated this venue
            # For example, by showing an error message or redirecting
            return redirect('already_rated', vid=venue.vid)

        form = RatingForm(request.POST)
        if form.is_valid():
            try:
                rating = form.save(commit=False)
                rating.venue = venue
                rating.user = request.user
                rating.save()
                return redirect('rating.html', vid=venue.vid)
            except IntegrityError:
                # Handle the unlikely case of a race condition
                return redirect('error_page')
    else:
        form = RatingForm()

    return render(request, 'rating.html', {
        'venue': venue,
        'form': form,
        'already_rated': already_rated,
    })
 
 
 
 
 
 
 
 
 
 
 
""" def thank_you(request):
    return render(request, 'thankyou.html')   """  