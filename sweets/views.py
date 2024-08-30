from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from sweets.models import User,Product,Cart_Wishlist,Orders,Sentiment
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if request.POST['group']=='Admin Login':
            isadmin=True
        else:
            isadmin=False
        request.session['username']=username
        if User.objects.filter(username=username,password=password,isadmin=isadmin).exists():
            if isadmin:
                return redirect(reverse('_admin'))
            else:
                return redirect(reverse('home'))
        else:
            messages.info(request,"Invalid Username or Password")
            return render(request,'login.html')
    else:
        return render(request,'login.html')

def home(request):
    user=request.session['username']
    money = User.objects.get(username=user).money
    return render(request,'homepage.html',{'user':user,'money':money})

def admin(request):
    user=request.session['username']
    cust=User.objects.filter(isadmin=False)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        order = Orders.objects.filter(date1__range=[start_date, end_date])
    else:
        order = Orders.objects.all()
    prod=Product.objects.all()
    rat=[]
    cnt=0
    sum=0
    for c in cust:
        if c.rating>0:
            rat.append(c.rating)
            cnt=cnt+1
            sum=sum+c.rating
    if cnt==0:
        return render(request,'admin.html',{'admin':user,'cust':cust,'order':order,'prod':prod,'sum':sum})
    avg=sum/cnt
    return render(request,'admin.html',{'admin':user,'cust':cust,'order':order,'prod':prod,'avg':avg,'cnt':cnt})

def register_view(request):
    if request.method == 'POST':
        username=request.POST['username']
        email_id=request.POST['email_id']
        password1=request.POST['password1']
        password2=request.POST['password2']
        contact_no=request.POST['contact_no']
        address=request.POST['address']
        pincode=request.POST['pincode']

        if User.objects.filter(username=username).exists():
            messages.info(request,"USERNAME TAKEN")
            return redirect(request.META['HTTP_REFERER'])
        elif User.objects.filter(email_id=email_id).exists():
            messages.info(request,'EMAIL TAKEN')
            return redirect(request.META['HTTP_REFERER'])
        elif len(username)<5 and len(username)>12:
            messages.info(request,'MINIMUM LENGTH SHOULD BE 5')
            return redirect(request.META['HTTP_REFERER'])
        elif password1!=password2:
            messages.info(request,"PASSWORD DOES NOT MATCH")
            return redirect(request.META['HTTP_REFERER'])
        elif len(password1)<8:
            messages.info(request,"PASSWORD TOO SHORT")
            return redirect(request.META['HTTP_REFERER'])
        elif re.search(r'[a-z][A-Z][0-9]',password1):
            messages.info(request,"INVALID PASSWORD")
            return redirect(request.META['HTTP_REFERER'])
        elif not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',email_id):
            messages.info(request,"INVALID EMAIL ID")
            return redirect(request.META['HTTP_REFERER'])
        elif len(contact_no)<10:
            messages.info(request,"INVALID CONTACT NO")
            return redirect(request.META['HTTP_REFERER'])
        elif len(address)<20:
            messages.info(request,"ADDRESS TOO SHORT")
            return redirect(request.META['HTTP_REFERER'])
        elif len(pincode)!=6:
            messages.info(request,"INVALID PINCODE")
            return redirect(request.META['HTTP_REFERER'])
        else:
            user=User.objects.create(username=username,password=password1,contact_no=contact_no,email_id=email_id,address=address,pincode=pincode,money=5000,rating=0)
            user.save()
            messages.info(request,"USER CREATED")
            print('user created')
            return redirect('login')
    else:
        return render(request,'register.html')

def homepage(request,state):
    user=request.session['username']
    money = User.objects.get(username=user).money
    products = Product.objects.filter(state=state,available=True)
    wishlist = Cart_Wishlist.objects.filter(username=user,cw='w')
    a=[]
    for pname in products:
        exist=False
        for wish in wishlist:
            if pname.p_name==wish.p_id.p_name:
                a.append("+Remove from Wishlist")
                exist=True
        if not exist:
            a.append("+Add to Wishlist")
    prod=zip(products,a)
    return render(request,'products.html',{'products':prod,'user':user,'money':money,'state':state})

def user(request):
    if request.method == 'POST':
        username=request.POST['username']
        email_id=request.POST['email_id']
        password1=request.POST['password1']
        password2=request.POST['password2']
        contact_no=request.POST['contact_no']
        address=request.POST['address']
        pincode=request.POST['pincode']
        user=User.objects.get(username=username)
        if password1!=password2:
            messages.info(request,"PASSWORD DOES NOT MATCH")
            return redirect(request.META['HTTP_REFERER'])
        elif len(password1)<=4:
            messages.info(request,"PASSWORD TOO SHORT")
            return redirect(request.META['HTTP_REFERER'])
        elif len(contact_no)<10:
            messages.info(request,"INVALID CONTACT NO")
            return redirect(request.META['HTTP_REFERER'])
        else:
            user.username=username
            user.password=password1
            user.contact_no=contact_no
            user.email_id=email_id
            user.address=address
            user.pincode=pincode
            user.save()
            messages.info(request,"User Information Updated")
            return redirect(request.META['HTTP_REFERER'])
    else:
        user=request.session['username']
        userinfo = User.objects.get(username=user)
        return render(request,'userinfo.html',{'userinfo':userinfo})

def addmoney(request):
    return render(request,"addmoney.html")

def addm(request):
    if request.method=='POST':
        user=request.session['username']
        money=request.POST['money']
        row=User.objects.get(username=user)
        row.money=int(row.money)+int(money)
        row.save()
        return redirect('home')

from django.shortcuts import render, redirect
from .models import Sentiment

def blog(request, state):
    user=request.session['username']
    money = User.objects.get(username=user).money
    reviews = Sentiment.objects.filter(state=state)
    return render(request, 'blog.html', {'state': state, 'reviews': reviews,'user':user,'money':money})

def goto_cw(request,cw):
    user=request.session['username']
    money = User.objects.get(username=user).money
    items = Cart_Wishlist.objects.filter(username=user,cw=cw)
    if cw=='c':
        return render(request,'cart.html',{'items':items,'user':user,'money':money})
    else:
        return render(request,'wishlist.html',{'items':items,'user':user,'money':money})

def add_cw(request,pname):
    username=request.session['username']
    user = User.objects.get(username=username)
    id = Product.objects.get(p_name=pname)
    if request.method=='POST':
        quan=request.POST['num']
        if Cart_Wishlist.objects.filter(p_id=id,username=user,cw='c').exists():
            row=Cart_Wishlist.objects.get(p_id=id,username=user,cw='c')
            row.quantity=quan
            row.save()
            messages.info(request,"Quantity Updated")

        else:
            row=Cart_Wishlist.objects.create(username=user,p_id=id,quantity=quan,cw='c')
            row.save()
            messages.info(request,"Added to Cart")
        return redirect(request.META['HTTP_REFERER'])
    else:
        if Cart_Wishlist.objects.filter(p_id=id,username=user,cw='w').exists():
           row=Cart_Wishlist.objects.get(p_id=id,username=user,cw='w')
           row.delete()
           messages.info(request,"Removed from Wishlist")
        else:
            row=Cart_Wishlist.objects.create(username=user,p_id=id,quantity=0,cw='w')
            row.save()
            messages.info(request,"Added to Wishlist")
        return redirect(request.META['HTTP_REFERER'])
    
def remove_cw(request,pname,cw):
    username=request.session['username']
    user = User.objects.get(username=username)
    id = Product.objects.get(p_name=pname)
    row=Cart_Wishlist.objects.get(p_id=id,username=user,cw=cw)
    row.delete()
    return redirect(request.META['HTTP_REFERER'])

def order(request):
    user=request.session['username']
    items = Cart_Wishlist.objects.filter(username=user,cw='c')
    money = User.objects.get(username=user).money
    address = User.objects.get(username=user).address
    grandtotal=0
    totals=[]
    date = datetime.datetime.now()
    for item in items:
        total = item.p_id.rate * item.quantity
        totals.append(total)
        grandtotal=grandtotal+total
    itemtotal = zip(items,totals)
    cgst=int(0.06*grandtotal)
    grandtotal+=cgst
    return render(request,'order.html',{'cgst':cgst,'user':user,'money':money,'grandtotal':grandtotal,'date':date,'address':address,'itemtotal':itemtotal})

def placeorder(request,gtotal):
    if request.method=='POST':
        user=request.session['username']
        items = Cart_Wishlist.objects.filter(username=user,cw='c')
        quan=[]
        products=[]
        for item in items:
            product = item.p_id
            products.append(product.p_name)
            quant = item.quantity
            quan.append(quant)
        money = User.objects.get(username=user).money
        user = User.objects.get(username=user)
        d=datetime.datetime.now()
        date=d.date()
        time=d.time()
        if money>gtotal:
            row = Orders.objects.create(username=user,date1=date,time1=time,order_list=products,quantities=quan,price=gtotal,status='w')
            row.save()
            money=money-gtotal
            user.money=money
            user.save()
            items.delete()
            messages.info(request,"Order placed successfully")
        else:
            messages.info(request,"Could not place order, check if your wallet has enough balance")
            return render(request,"addmoney.html")
        return redirect(reverse('home'))
    else:
        return redirect(request.META['HTTP_REFERER'])

def myorders(request):
    user=request.session['username']
    username=User.objects.get(username=user)
    money=User.objects.get(username=user).money
    orders=Orders.objects.filter(username=username).order_by('-id')
    return render(request,"myorders.html",{'orders':orders,'user':user,'money':money})

def showbill(request,id):
    user=request.session['username']
    userinfo=User.objects.get(username=user)
    money = User.objects.get(username=user).money
    bill=Orders.objects.get(id=id)
    rates = []
    totals = []
    grandtotal=0
    for i,b in enumerate(bill.order_list):
        rate = Product.objects.get(p_name=b).rate
        rates.append(rate)
        total = rate * bill.quantities[i]
        totals.append(total)
        grandtotal=grandtotal+total
    cgst=int(0.06*grandtotal)
    grandtotal+=cgst
    bills = zip(bill.order_list,bill.quantities,rates,totals)
    return render(request,"showbill.html",{'bill':bill,'bills':bills,'user':user,'money':money,'userinfo':userinfo,'date':datetime.datetime.now(),'grandtotal':grandtotal,'cgst':cgst})

def download(request,id):
    user=request.session['username']
    userinfo=User.objects.get(username=user)
    bill = Orders.objects.get(id=id)
    date=datetime.datetime.now()
    rates = []
    totals = []
    grandtotal=0
    for i,b in enumerate(bill.order_list):
        rate = Product.objects.get(p_name=b).rate
        rates.append(rate)
        total = rate * bill.quantities[i]
        totals.append(total)
        grandtotal=grandtotal+total
    bills = zip(bill.order_list,bill.quantities,rates,totals)
    d=2
    template=get_template("showbill.html")
    html_content=template.render({'d':d,'bills':bills,'user':user,'date':date,'userinfo':userinfo,'bill':bill,'grandtotal':grandtotal})
    pdf_file = open('orderbill.pdf', 'w+b')
    pisa.CreatePDF(html_content, dest=pdf_file)
    pdf_file.seek(0)
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="orderbill.pdf"'
    return response

def update_product(request,pname):
    if request.method=='POST':
        rate=request.POST['rate']
        available=request.POST['available']
        image=request.POST.get('urlnew')
        if image is None:
            image=request.POST['url']
        else:
            img=image
        if available=='yes':
            a=True
        else:
            a=False
        row=Product.objects.get(p_name=pname)
        row.rate=rate
        row.available=a
        row.img=img
        row.save()
        messages.info(request,"Product Updated")
        return redirect(reverse('_admin'))   
    else:
        return redirect(request.META['HTTP_REFERER'])

def update_status(request,id):
    user=request.session['username']
    if request.method=='POST':
        status=request.POST['status']  
        row=Orders.objects.get(id=id)
        row.status=status
        row.save()
        messages.info(request,"Status Updated")
        return redirect(reverse('_admin'))   
    else:
        return redirect(request.META['HTTP_REFERER'])

def add_review(request):
    if request.method=='POST':
        user=request.session['username']
        row=User.objects.get(username=user)
        row.rating=request.POST['rating']
        row.review=request.POST['review']
        row.save()
        messages.info(request,"Thank you for Feedback")
        return redirect(reverse('home'))
    else:
        return redirect(request.META['HTTP_REFERER'])

def add_blogreview(request,state):
    if request.method=='POST':
        review = request.POST['feed']
        nltk.download('vader_lexicon')
        sid = SentimentIntensityAnalyzer()
        sentiment_scores = sid.polarity_scores(review)
        if sentiment_scores['compound'] >= 0.05:
            sentiment = 'p'
        elif sentiment_scores['compound'] <= -0.05:
            sentiment = 'b'
        else:
            sentiment = 'n'
        s=Sentiment.objects.create(state=state,userreview=review,sentment=sentiment)
        s.save()
        messages.info(request,"Thank you for feedback")
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect(request.META['HTTP_REFERER'])