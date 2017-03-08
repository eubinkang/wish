from django.shortcuts import render, redirect
from .models import User, Wish
from django.contrib import messages

def index(request):
    if "id" not in request.session:
        request.session['id'] = ""
    return render(request, 'wishes/index.html')

def register(request):
    if request.method == "GET":
        return redirect('/')

    user = User.objects.validate(request.POST)

    if user[0] == True:
        request.session['id'] = user[1].id
        return redirect('/dashboard')
    else:
        for errors in user[1]:
            messages.error(request, errors)
        return redirect('/')


def login(request):
    if request.method == "GET":
        return redirect('/')

    else:
        user = User.objects.login(request.POST)
        if user[0] == True:
            request.session['id'] = user[1].id
            return redirect('/dashboard')
        else:
            for errors in user[1]:
                messages.error(request, errors)
            return redirect('/')

def dashboard(request):
    if "id" not in request.session:
        return redirect('/')
    currentuser = User.objects.get(id=request.session['id'])
    trap = Wish.objects.all().filter(share=currentuser)
    trap2 = Wish.objects.all().exclude(share=currentuser)
    try:
        context = {
            "user": currentuser,
            "trap": trap,
            "trap2": trap2
            }
        for i in trap:
            print i.wishitem, i.created_at, i.addby.name
        return render(request, 'wishes/dashboard.html', context)
    except:
        context = {
            "user": currentuser
            }
        return render(request, 'wishes/dashboard.html', context)

def create(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['id'])
        newitem = Wish.objects.additem(request.POST, user)
        if newitem[0] == True:
            print "valid"
            messages.info(request, newitem[1])
            return redirect('/dashboard')
        if newitem[0] == False:
            return redirect('/dashboard')
        else:
            for error in newitem[1]:
                messages.error(request, error)
            return redirect('/dashboard')

def delete(request, wish_id):
    if "id" not in request.session:
        messages.error(request, "Please log in to do that")
        return redirect('/')
    try:
        Wish.objects.get(id=wish_id).delete()
        messages.info(request, "Item deleted")
        return redirect('/dashboard')
    except:
        messages.error(request, "I can't do that Dave")
        return redirect('/')

def cancel(request, wish_id):
    if "id" not in request.session:
        messages.error(request, "Please log in to do that")
        return redirect('/')
    try:
        user = User.objects.get(id=request.session['id'])
        wish = Wish.objects.get(id=wish_id)
        wish.share.remove(user)
        messages.info(request, "Item cancelled")
        return redirect('/dashboard')
    except:
        messages.error(request, "I can't do that Dave")
        return redirect('/')

def logout(request):
    request.session.pop('id')
    messages.success(request, "You are now logged out!")
    return redirect('/')

def share(request, wish_id):
    if "id" not in request.session:
        messages.error(request, "Please log in to do that")
        return redirect('/')
    try:
        user = User.objects.get(id=request.session['id'])
        wish = Wish.objects.shareitem(wish_id, user)
        messages.info(request, wish[1])
        return redirect('/dashboard')
    except:
        messages.error(request, "I can't do that Dave")
        return redirect('/')

def add(request):
    if request.method == "GET":
        print "nogood"
        return redirect('/')
    if request.method == "POST":
        print 'good'
        return redirect('/additem')

def additem(request):
    if "id" not in request.session:
        messages.error(request, "Please log in to do that")
        return redirect('/')
    else:
        return render(request, 'wishes/create.html')

def wishitem(request, wish_id):
    if "id" not in request.session:
        messages.error(request, "Please log in to do that")
        return redirect('/')
    wish = Wish.objects.filter(id=wish_id)
    user = User.objects.all()

    context = {
        "wish": wish,
        "user": user
        }
    return render(request, 'wishes/wishitem.html', context)

def any(request):
    messages.error(request, 'Invalid URL')
    return redirect('/')
