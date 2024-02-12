from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User  
# Create your models here.
class CustomeManager(models.Manager):
    def get_location(self, location):
        return self.filter(location__iexact=location)
    
    """ def get_state(self, state):
        return self.filter(location__iexact=state) """
    
class Venue(models.Model):
    vid=models.IntegerField(primary_key=True)
    vname=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    price =models.IntegerField()   
    image =models.ImageField(upload_to='venuepics')
    choice=(('Maharashtra','Maharashtra'),('Goa','Goa'),('Gujarat','Gujarat'),('Andhra Pradesh','Andhra Pradesh'),('Arunachal Pradesh','Arunachal Pradesh'),('Assam','Assam'),('Himachal Pradesh','Himachal Pradesh'),('Rajasthan','Rajasthan'),('Kerala','Kerala'))
    state = models.CharField(max_length=50,choices=choice)
    desc = models.CharField(max_length=255)

    
    prod=CustomeManager() #customer manager
    objects =models.Manager() #default manager
    
    

    def proImage(self):
        return mark_safe(f"<img src= '{self.image.url}' width='300px'>")
    
    
class Booking(models.Model):
    bid=models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=100, default='Pending')
    is_completed = models.BooleanField(default=False) 
    quantity = models.PositiveIntegerField(default=0)
    
    
    def __str__(self):
        return f"{self.user.username} booking {self.venue.vname}" 

    
    
    
    
    
class CustomeManager(models.Manager):
    def get_location(self, location):
        return self.filter(location__iexact=location)



class Rating(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('venue', 'user')  # Ensure a user can only rate a venue once

    def __str__(self):
        return f"{self.score} by {self.user} for {self.venue}"




class Order(models.Model):
    order_id=models.CharField(max_length=50)
    venue=models.ForeignKey(Venue,on_delete=models.CASCADE)
    quantity= models.PositiveBigIntegerField(default=0)
    user= models.ForeignKey(User,on_delete =models.CASCADE,default=1)
    date_added =models.DateTimeField(auto_now_add = True)    
    is_completed=models.BooleanField(default="False")    
    
    
    
    
    
    

