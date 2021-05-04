from django.conf import settings
from django.db import models
from django_countries.fields import CountryField

class Category(models.Model):
    name = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.name

    #all categories
    @classmethod
    def get_category(cls):
        categories = Category.objects.all()
        return categories    

    def save_category(self):
        self.save()

    def delete_category(self):
        self.delete()

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to = 'profile_photos/', null=True)
    bio = models.CharField(max_length =300)

    @classmethod
    def get_profile(cls):
        all_profiles = cls.objects.all()
        return all_profiles

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete() 

    def __str__(self):
        return str(self.user)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to = 'landing_images/')
    description = models.TextField(default='')
    product_usage = models.TextField(default='')
    category = models.ForeignKey(Category,on_delete=models.CASCADE, default=1)

    #searching product by title
    @classmethod
    def search_by_title(cls,search_term):
        certain_user = cls.objects.filter(title__icontains = search_term)
        return certain_user

    def __str__(self):
        return self.title
    
    #filtering products by category
    @classmethod
    def filter_by_category(cls, category):
        product = Item.objects.filter(category__name=category).all()
        return product


class Orderitem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


    def get_total_item_price(self):
        return self.quantity * self.item.price    

    def get_final_price(self):
        return  self.get_total_item_price()

    

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(Orderitem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
  
   #references the billingaddress when order is complete
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True,null=True)


    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        total_discount = 0
        for order_item in self.items.all():
            total = total + order_item.get_final_price()
            if total >= 80000:
                total_discount = (total * 5)/100
                return total - total_discount
        
        return total  
                 


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    street_address = models.CharField(max_length=50)
    apartment_address = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    country = CountryField(multiple=False)
    zipcode = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)

    def __str__(self):

        return self.user.username

class SubscribeRecipients(models.Model):
    name = models.CharField(max_length=30, default='')
    email = models.EmailField()


class Review(models.Model):
    reviewer = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField()
    review_body = models.CharField(max_length= 200)
    review_title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True, null=True)
    product_review = models.ForeignKey(Item, on_delete=models.CASCADE,null=True)

    def save_review(self):
        self.save()

    def delete_review(self):
        self.delete()

    def __str__(self):
        return self.reviewer        