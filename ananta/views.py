from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Enquiry,Product,GalleryProject, GalleryImage

def index(request):
    products = Product.objects.all().order_by('-created_at')
    # Add this to show gallery on the home page
    projects = GalleryProject.objects.all().prefetch_related('images').order_by('-created_at')
    return render(request, 'index.html', {
        'products': products,
        'projects': projects
    })
@login_required
def admin_dashboard(request):
    enquiries = Enquiry.objects.all().order_by('-created_at')
    products = Product.objects.all().order_by('-created_at')
    # Add this so the dashboard table can see the projects
    projects = GalleryProject.objects.all().order_by('-created_at')
    
    return render(request, 'dashboard.html', {
        'enquiries': enquiries,
        'products': products,
        'projects': projects
    })

@login_required
def add_product(request):
    if request.method == "POST":
        image = request.FILES.get('image')

        # ❌ Prevent product creation without image
        if not image:
            messages.error(request, "Image is required!")
            return redirect('admin_dashboard')

        Product.objects.create(
            name=request.POST.get('name'),
            category=request.POST.get('category'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            image=image
        )

    return redirect('admin_dashboard')

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('admin_dashboard')

def update_enquiry(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    if request.method == "POST":
        enquiry.status = request.POST.get('status')
        enquiry.save()
    return redirect('admin_dashboard') # Must match name in urls.py

def delete_enquiry(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    enquiry.delete()
    return redirect('admin_dashboard') # Must match name in urls.py

def submit_enquiry(request):
    if request.method == "POST":
        Enquiry.objects.create(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            service=request.POST.get('service'),
            location=request.POST.get('location'),
            budget=request.POST.get('budget'),
            message=request.POST.get('message')
        )
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)

def staff_login(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('staff_login')
            
    return render(request, 'staff.html')

def staff_logout(request):
    logout(request)
    return redirect('index')

@login_required
def upload_gallery(request):
    if request.method == "POST":
        title = request.POST.get('title')
        files = request.FILES.getlist('images')
        
        project = GalleryProject.objects.create(title=title)
        
        for f in files:
            GalleryImage.objects.create(project=project, image=f)
            
        return redirect('admin_dashboard') # Changed from 'dashboard' to 'admin_dashboard'
    return redirect('admin_dashboard')

@login_required
def delete_gallery(request, pk):
    project = get_object_or_404(GalleryProject, pk=pk)
    # This will automatically delete associated GalleryImages if you set up 
    # models.CASCADE in your models.py
    project.delete()
    return redirect('admin_dashboard')