from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Category Name")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class City(models.Model):
    name = models.CharField(max_length=255, verbose_name="City Name")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

class Area(models.Model):
    name = models.CharField(max_length=255, verbose_name="Area Name")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Area"
        verbose_name_plural = "Areas"
        
        
class Metro(models.Model):
    name = models.CharField(max_length=255, verbose_name="Metro Name")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Metro"
        verbose_name_plural = "Metros"
        
        

class Sight(models.Model):
    name = models.CharField(max_length=255, verbose_name="Sight Name")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Sight"
        verbose_name_plural = "Sights"
    
class Street(models.Model):
    name = models.CharField(max_length=255, verbose_name="Street Name")   
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Street"
        verbose_name_plural = "Streets"
        
        

class Location(models.Model):
    name = models.CharField(max_length=255, verbose_name="Location Name")
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="streets", verbose_name="Area")
    metro = models.ForeignKey(Metro, on_delete=models.CASCADE, related_name="streets", verbose_name="Metro")
    sight = models.ForeignKey(Sight, on_delete=models.CASCADE, related_name="streets", verbose_name="Sight")    
    street = models.ForeignKey(Street, on_delete=models.CASCADE, related_name="streets", verbose_name="Street")
    
    def __str__(self):
        return f"{self.name} - {self.street.name}"
    
    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        
        
class PropertySource(models.Model):
    source_name = models.CharField(max_length=100)
    source_url = models.URLField()
        
    def __str__(self):
        return self.source_name
        
class Property(models.Model):
    title = models.CharField(max_length=255, verbose_name="Property Title")
    description = models.TextField(verbose_name="Property Description")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Property Price")
    room_count = models.IntegerField(verbose_name="Room Count")
    is_sale = models.BooleanField(default=False, verbose_name="Is Sale?")
    is_rent = models.BooleanField(default=False, verbose_name="Is Rent?")
    property_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Property Area")
    is_documented = models.BooleanField(default=False, verbose_name="Documented?")
    have_things = models.BooleanField(default=False, verbose_name="Have things?")
    communal = models.BooleanField(default=False, verbose_name="Communal?")
    floor = models.IntegerField(null=True, blank=True, verbose_name="Floor")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name="properties", verbose_name="Property Location")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="properties", verbose_name="Preferred Category")
    location_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Property Area")
    
    source = models.ForeignKey(PropertySource, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"  
        indexes = [
            models.Index(fields=["price"]),
            models.Index(fields=["room_count"]),
            models.Index(fields=["is_sale"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["location"]),
            models.Index(fields=["category"]),
            models.Index(fields=["is_rent"]),
        ]
        
        
        
class Notification(models.Model):
    account = models.ForeignKey("accounts.Account",on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=50)
    retry_count = models.IntegerField(default=0)
    error_message = models.TextField(null=True, blank=True)
    score = models.IntegerField(default=0)
    also_sendto_customer = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notification for {self.account.email} - Property: {self.property.title}"
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        indexes = [
            models.Index(fields=["account"]),
            models.Index(fields=["property"]),
            models.Index(fields=["is_sent"]),
            models.Index(fields=["sent_at"]),
        ]