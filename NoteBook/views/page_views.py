from django.shortcuts import render,redirect,get_object_or_404
from apps.Note.models import NoteModel,CateogryModel
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
import string
import secrets
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator

@login_required
def index(request):
    return render(request,"index.html")

@login_required
def notes(request):
    notes = NoteModel.objects.filter(owner=request.user).order_by("-created_at")
    category = CateogryModel.objects.all()

    search = request.GET.get("search","").strip()
    category_search = request.GET.get("category_search", "")

    
    if search:
        notes = notes.filter(Q(title__icontains = search)|Q(author__icontains=search)|Q(category__name__icontains=search)|Q(description__icontains=search))

    if category_search:
        notes = notes.filter(category_id = category_search) 

    paginator = Paginator(notes,6)
    page_number = request.GET.get('page')
    product_page = paginator.get_page(page_number)

    context = {
        'notes':notes,
        'category':category,
        'cat_search':category_search,
        'note_pagination':product_page,
        'search':search,
    }
    return render(request,"notes.html",context)

@login_required
def note_create(request):
    category = CateogryModel.objects.all()
    if request.method == 'POST':
        product = NoteModel.objects.create(
            title = request.POST.get("title"),
            author = request.POST.get("author"),
            category_id = request.POST.get("category"),
            description = request.POST.get('description'),
            Text = request.POST.get("Text"),
            owner = request.user,
        )
        product.save()
        return redirect("notes")

    context = {
        'category':category
    }

    return  render(request,'note_create.html',context)

@login_required
def notes_details(request,noteid):
    notes = get_object_or_404(NoteModel, id=noteid, owner=request.user)

    context = {
        'notes':notes,
    }
    
    return render(request,'notes_details.html',context)

@login_required
def note_update(request,noteid):
    notes = get_object_or_404(NoteModel, id=noteid, owner=request.user)
    category = CateogryModel.objects.all()
    if request.method == 'POST':
        notes.title = request.POST.get("title")
        notes.author = request.POST.get("author")
        notes.Text = request.POST.get("Text")
        notes.description = request.POST.get("description")
        notes.category_id = request.POST.get("category")
        notes.save()
        return redirect("notes")

    context = {
        'notes':notes,
        'category':category
    }

    return render(request,'note_update.html',context)

@login_required
def note_delete(request,noteid):
    note = get_object_or_404(NoteModel, id=noteid, owner=request.user)
    note.delete()
    return redirect("notes")


def register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        conf_password = request.POST.get("confirm_password")

        if password != conf_password:
            messages.warning(request, "Password does not match")

        if User.objects.filter(username = username).exists():
            messages.warning(request, 'User already exists')
            return redirect("register")
        else:
            alphabet = string.ascii_uppercase + string.digits 
            otp = ''.join(secrets.choice(alphabet) for i in range(6))

            request.session['reg_data'] = {
                "user":username,
                'useremail':email,
                'password':password,
                'otp':otp
            }

            send_mail (
                'Your varification Code',
                f"Your OTP is {otp}",
                settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False
            )
            messages.success(request,'Verification code send successfully')
            return redirect("otp")

    return render(request,'register.html')


def otp_verification(request):
    if 'reg_data' not in request.session:
        messages.error("Error Please try again")
        return redirect("register") 
    
    if request.method == 'POST':
        user_otp = request.POST.get("otp")
        reg_data = request.session.get("reg_data")

        if user_otp == reg_data['otp']:
            user = User.objects.create_user(
                username = reg_data['user'],
                email = reg_data['useremail'],
                password = reg_data['password'],
            )
            del request.session['reg_data']
            messages.success(request,'Registered successfully')
            return redirect("login")

        else:
            messages.error(request,"OTP code is wrong")


    return render(request,'otp_verification.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username = username,password = password)

        if user is not None:
            login(request,user)
            messages.success(request,"Login Successfully")
            return redirect("index")
        else:
            messages.warning(request,"Invalid email or password")
            return redirect("login")
        
    return render(request,'login.html')

def user_logout(request):
    logout(request)
    messages.success(request,"Logout Successful!")
    return redirect("login")

def page_not_found(request):
    return render(request, "404.html")
