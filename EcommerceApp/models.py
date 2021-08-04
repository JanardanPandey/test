from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import AutoField, CharField, DateTimeField, TextField
from django.db.models.fields.files import FileField
from django.dispatch import receiver
from django.db.models.signals import post_save



# Create your models here.


class CustomUser(AbstractUser):
    user_type_choices = ((1,"Admin"),(2,"Staff"),(3,"Marchent"),(4,"Customer"))
    user_type=models.CharField(max_length=255,choices=user_type_choices, default=1)


class AdminUser(models.Models):
    auth_user_id=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic=models.FileField(default="")
    created_at =models.DateTimeField(auto_now_add=True)

class StaffUser(models.Model):
    auth_user_id=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic=models.FileField(default="")
    created_at=models.DateTimeField(auto_now_add=True)

class MarchantUser(models.Model):
    auth_user_id=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic=models.FileField(default="")
    company_name=models.CharField(max_length=255)
    gst_details=models.CharField(max_length=255)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

class CustomerUser(models.Model):
    auth_user_id=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic=models.FileField(default="")
    created_at=models.DateTimeField(auto_now_add=True)

class Categories(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    url_slug=models.CharField(max_length=255)
    thumbnail=models.FileField()
    description=models.TextField()
    is_active=models.IntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=Ture)

class SubCategories(models.Model):
    id=models.AutoField(primary_key=True)
    category_id=models.ForeignKey(Categories, on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    url_slug=models.CharField(max_length=255)
    thumbnail=models.FileField()
    description=models.TextField()
    is_active=models.IntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    id=models.AutoField(primary_key=True)
    url_slug=models.CharField(max_length=255)
    SubCategories_id=models.ForeignKey(SubCategories, on_delete=models.CASCADE)
    product_name=models.CharField(max_length=255)
    brand=models.CharField(max_length=255)
    product_max_price=models.CharField(max_length=255)
    product_discount_price=models.CharField(max_length=255)
    product_discription=models.TextField()
    product_long_discription=models.TextField()
    added_by_marchant=models.ForeignKey(MarchantUser, on_delete=models.CASCADE)
    in_stock_total=models.IntegerField(default=1)
    is_active=models.IntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)

class ProductMedia(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE)
    media_type_choice=((1,"Image"),(2,"Video"))
    media_type=models.CharField(max_length=255)
    media_content=models.FileField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductTransaction(models.Model):
    id=models.AutoField(primary_key=True)
    transaction_type_choices=((1,"BUY"),(2,"sell"))
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction_product_count=models.IntegerField(default=1)
    trasaction_type=models.CharField(choices=transaction_type_choices, max_length=255)
    transaction_description=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

class ProductDetails(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE)
    title_details=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductAbout(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at=models.DateTimeField()
    is_active=models.IntegerField(default=1)

class ProductTags(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id=models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    question=models.TextField()
    answer=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductReviews(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id=models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    reviews_images=models.FileField()
    rating=models.CharField(default="5")
    reviews=models.TextField(default="")
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductReviewVoting(models.Model):
    id=models.AutoField(primary_key=True)
    product_review_id=models.ForeignKey(ProductReviews, on_delete=models.CASCADE)
    user_id_voting= models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductVarient(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

class ProductVartientItems(models.Model):
    id=models.AutoField(primary_key=True)
    product_variant_id=models.ForeignKey(ProductVarient, on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    
class CustomerOrders(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    purchase_price=models.CharField(max_length=255)
    coupon_code=models.CharField(max_length=255)
    discount_amt=models.CharField(max_length=255)
    product_status=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

class OrderDeliveryStatus(models.Model):
    id=models.AutoField(primary_key=True)
    order_id=models.ForeignKey(CustomerOrders,on_delete=models.CASCADE)
    status=models.CharField(max_length=255)
    status_message=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)     

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender,instance, created, **kwargs):
    if created:
        if instance.user_type==1:
            AdminUser.objects.create(auth_user_id=instance)
        if instance.user_type==2:
            StaffUser.objects.create(auth_user_id=instance)
        if instance.user_type==1:
            MarchantUser.objects.create(auth_user_id=instance, company_name="", gst_details="", address="")
        if instance.user_type==1:
            CustomerOrders.objects.create(auth_user_id=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender,instance, **kwargs):
    if instance.user_type==1:
        instance.adminuser.save()
    if instance.user_type==2:
        instance.staffuser.save()
    if instance.user_type==3:
        instance.marchantuser.save()
    if instance.user_type==4:
        instance.customeruseruser.save()


