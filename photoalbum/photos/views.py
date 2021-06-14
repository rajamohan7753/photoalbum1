from django.shortcuts import render,redirect
from .models import Category,photo
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
# Create your views here.
def loginpage(request):

    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user= authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('gallery')
    return render(request,'registration/login.html')

def logoutpage(request):
    logout(request)
    return redirect('login')

def registerpage(request):

    form=SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST)
        user=form.save()
        user.set_password(user.password)
        user.save()
        return redirect('gallery')




    context = {'form':form}
    return render(request,'registration/signup.html',context)



@login_required
def gallery(request):
    category= request.GET.get('Category')
    print('Category:', Category)
    if Category == None:
        photos=photo.objects.all()
    else:
        photos=photo.objects.filter(category__name=Category)


    categories = Category.objects.all()
    photos=photo.objects.all()
    context={'categories':categories,'photos':photos}
    return render(request,'photos/gallery.html',context)

@login_required
def viewphoto(request,pk):
    photos=photo.objects.get(id=pk)
    return render(request,'photos/photo.html',{'photos':photos})
@login_required
def addphoto (request):

    categories = Category.objects.all()

    if request.method=='POST':
        data= request.POST
        image= request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None
        photos=photo.objects.create(
                 category=category,
                 description=data['description'],
                 image=image,
        )

        return redirect('gallery')


    context={'categories':categories}
    return render(request,'photos/add.html',context)
