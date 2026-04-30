from django.db import models

class Enquiry(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('done', 'Done'),
    ]
    
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=150)
    location = models.CharField(max_length=255)
    budget = models.CharField(max_length=100)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ananta_enquiry'
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"{self.name} - {self.status}"

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('kitchen', 'Kitchen'),
        ('doors', 'Doors'),
        ('furniture', 'Furniture'),
        ('decor', 'Decor'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.CharField(max_length=100) 
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ananta_products' # Changed from 'Pro' to avoid conflicts

    def __str__(self):
        return self.name

# --- NEW GALLERY MODELS ---
class GalleryProject(models.Model):
    title = models.CharField(max_length=200) # e.g., "Luxury Living"
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ananta_gallery_project'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

class GalleryImage(models.Model):
    # This connects multiple images to one project
    project = models.ForeignKey(GalleryProject, related_name='images', on_delete=models.CASCADE)
    # Corrected 'upload_with' to 'upload_to'
    image = models.ImageField(upload_to='gallery/') 
    
    class Meta:
        db_table = 'ananta_gallery_images'