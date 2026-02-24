from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.photo_save import logo_dir_path

class Plan(models.Model):
    name = models.CharField(max_length=255, verbose_name="Plan Name")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Plan Price")
    duration_days = models.IntegerField(verbose_name="Plan Duration (days)")
    max_notifications = models.IntegerField(verbose_name="Maximum Notifications")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"
        
        

class Account(AbstractUser):
    
    class GenderChoices(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        UNDEFINED = "undefined", "Undefined"
        
    
    image = models.ImageField(upload_to=logo_dir_path,null=True,blank=True,verbose_name="Profile photo")
    phone = models.CharField(max_length=20, blank=True, null=True,verbose_name="Phone number")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Birth date")
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="City")
    gender = models.CharField(max_length=10, 
                              default=GenderChoices.UNDEFINED,choices=GenderChoices.choices,
                              null=True, blank=True, verbose_name="Gender")
    bio = models.TextField(null=True, blank=True, verbose_name="About")
    
    otp = models.CharField(max_length=6, null=True, blank=True, verbose_name="Email Verification OTP")
    otp_created_at = models.DateTimeField(null=True, blank=True, verbose_name="OTP creation time")

    
    reset_password_otp = models.CharField(max_length=6, blank=True, null=True, verbose_name="Password Reset OTP")
    is_reset_password_otp_verified = models.BooleanField(default=False, verbose_name="'Forgot Password' OTP Verified?")
    reset_password_request_count = models.IntegerField(default=0, verbose_name="Number of password reset requests in a day")
    last_reset_password_request_date = models.DateField(null=True, blank=True, verbose_name="Last password reset request date")
    last_password_reset_date = models.DateField(null=True, blank=True, verbose_name="Last password reset date")
    reset_password_otp_created_at = models.DateTimeField(null=True, blank=True, verbose_name="Password Reset OTP creation time")
    reset_password_otp_expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Password Reset OTP expiration time")    

    is_verified = models.BooleanField(default=False, verbose_name="Verified?")
    private_account = models.BooleanField(default=False, verbose_name="Private Account?")
    rank = models.IntegerField(default=0, verbose_name="User Rank")
    


    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        
        
        
class AccountCustomers(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="customers")
    name = models.CharField(max_length=255, verbose_name="Customer Name")
    email = models.EmailField(verbose_name="Customer Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Customer Phone")
    telegram_username = models.CharField(max_length=255, blank=True, null=True, verbose_name="Customer Telegram Username")
    
    class Meta:
        verbose_name = "Account Customer"
        verbose_name_plural = "Account Customers"
        
    def __str__(self):
        return f"{self.account.username} - {self.name}"
        
        
class AccountCustomerPreferries(models.Model):
    
    ROOM_CHOICES = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5+"),
    ]
    
    customer = models.ForeignKey(AccountCustomers, on_delete=models.CASCADE, related_name="preferries")    
    min_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Minimum Area")
    max_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Maximum Area")
    min_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Minimum Price")
    max_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Maximum Price")
    room_count = models.IntegerField(null=True, blank=True, verbose_name="Room Count", choices=ROOM_CHOICES, default=1)
    want_rent = models.BooleanField(default=False, verbose_name="Looking for rent?")
    want_sale = models.BooleanField(default=False, verbose_name="Looking for sale?")
    is_documented = models.BooleanField(default=False, verbose_name="Documented?")
    is_active = models.BooleanField(default=True, verbose_name="Active?")
    have_things = models.BooleanField(default=False, verbose_name="Have things?")
    communal = models.BooleanField(default=False, verbose_name="Communal?")
    floor = models.IntegerField(null=True, blank=True, verbose_name="Floor")
    location = models.ManyToManyField("properties.Location", blank=True,related_name="customer_preferries", verbose_name="Preferred Location")
    category = models.ForeignKey("properties.Category", on_delete=models.SET_NULL, null=True, blank=True, related_name="customer_preferries", verbose_name="Preferred Category")
    
    
    class Meta:
        verbose_name = "Account Customer Preferry"
        verbose_name_plural = "Account Customer Preferries"
        
    def __str__(self):
        return f"{self.customer.name} - Preferry {self.id}"
    
    
class PreferryPriority(models.Model):
    preferry = models.OneToOneField(AccountCustomerPreferries, on_delete=models.CASCADE)
    weight_location = models.IntegerField(default=40)
    weight_price = models.IntegerField(default=30)
    weight_room = models.IntegerField(default=20)
    weight_category = models.IntegerField(default=10)
    
    class Meta:
        verbose_name = "Preferry Priority"
        verbose_name_plural = "Preferry Priorities"
    
    
class AccountFilters(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="filters")
    account_customer = models.ForeignKey(AccountCustomers, on_delete=models.CASCADE, related_name="filters", null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name="Filter Name")
    location = models.ManyToManyField("properties.Location", related_name="account_filters", verbose_name="Filter Location")
    category = models.ForeignKey("properties.Category", on_delete=models.SET_NULL, null=True, blank=True, related_name="account_filters", verbose_name="Filter Category")
    min_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Minimum Price")
    max_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Maximum Price")
    min_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Minimum Area")
    max_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Maximum Area")
    room_count = models.IntegerField(null=True, blank=True, verbose_name="Room Count")
    is_sale = models.BooleanField(default=False, verbose_name="Is Sale?")
    is_rent = models.BooleanField(default=False, verbose_name="Is Rent?")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Account Filter"
        verbose_name_plural = "Account Filters"
        
    def __str__(self):
        return f"{self.account.username} - Filter {self.name}"
    
    
    
class AccountFilterMatch(models.Model):
    account_filter = models.ForeignKey(AccountFilters, on_delete=models.CASCADE, related_name="matches")
    property = models.ForeignKey("properties.Property", on_delete=models.CASCADE, related_name="filter_matches")
    matched_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Account Filter Match"
        verbose_name_plural = "Account Filter Matches"
    
class Subscription(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    
    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        
        
        
