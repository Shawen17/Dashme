from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import SignupForm,ContactUsForm,Profileform,SendEmailForm,GiveawayForm,TransactionForm
from .models import Profile,Give,Transaction,Charge,Response,OnDeliveryTransaction,State,DestinationCharge,GiveawayCap,ShoppingCart
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail,BadHeaderError
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django import template
from django.contrib.auth import get_user_model
import requests
from datetime import timedelta
from .fields import final_checkout
from itertools import chain



UserModel = get_user_model()



def home(request):
    user=request.user
    electronics=Give.objects.filter(gift_status='unpicked',category='electronics').order_by('-date_posted')[:12]
    natives=Give.objects.filter(gift_status='unpicked',category='natives').order_by('-date_posted')[:12]
    shoes=Give.objects.filter(gift_status='unpicked',category='shoes').order_by('-date_posted')[:12]
    clothes=Give.objects.filter(gift_status='unpicked',category='clothes').order_by('-date_posted')[:12]
    corporate=Give.objects.filter(gift_status='unpicked',category='corporate').order_by('-date_posted')[:12]
    cartItem=Give.objects.filter(gift_recipient=user, gift_status='requested').count
    premium=Give.objects.filter(product_class='premium',gift_status='unpicked').order_by('-date_posted')[:12]
    context={
        'premium':premium,
        'cartItem':cartItem,
        'electronics':electronics,
        'natives':natives,
        'shoes':shoes,
        'clothes':clothes,
        'corporate':corporate
    }
    return render(request,'givers/new_home.html',context)


def operation(request):
    return render(request,'givers/howitworks.html')

def policy(request):
    return render(request,'givers/policy.html')

def about(request):
    return render(request,'givers/about.html')


def reply_contact(request):

    shape=request.session.get('selected')

    if request.method=='POST':
        form=SendEmailForm(request.POST)
        if form.is_valid:
            new_form=form.save(commit=False)
            new_form.email=shape[0]
            new_form.replied_by=request.user.username
            new_form.comment=form.cleaned_data.get('comment')
            new_form.save()

            if len(shape)>1:
                comment=form.cleaned_data.get('comment')
                for i in shape[1:]:
                    data={
                        'email':i,
                        'comment':comment,
                        'replied_by':request.user.username
                    }
                    Response.objects.create(**data)

            msg=EmailMultiAlternatives('Dashme',form.cleaned_data.get('comment'),settings.EMAIL_HOST_USER,bcc=shape)
            msg.send()
            messages.success(request,'reply sent')
            del request.session['selected']
            return redirect('/admin/givers/contactus')




def signupuser(request):

    if request.method == 'POST':
        form = SignupForm()
        state=request.POST['state']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username Already Taken')
                return redirect('signupuser')

            elif User.objects.filter(email=email).exists():
                messages.error(request,'Email Already Exist')
                return redirect('signupuser')

            else:
                form = SignupForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    user.refresh_from_db()
                    user.first_name=form.cleaned_data.get('firstname')
                    user.last_name=form.cleaned_data.get('lastname')
                    user.profile.state=form.cleaned_data.get('state')
                    user.profile.firstname=form.cleaned_data.get('firstname')
                    user.profile.lastname=form.cleaned_data.get('lastname')
                    user.profile.email=form.cleaned_data.get('email')
                    user.profile.phone_number=  form.cleaned_data.get('phone_number')
                    if not len(str(user.profile.phone_number)) == 10:
                        messages.error(request,'invalid phone number')
                        return redirect('signupuser')
                    user.save()

                    subject = 'Activate your account.'
                    plaintext = template.loader.get_template('password/acc_activate_email.txt')
                    htmltemp = template.loader.get_template('password/acc_activate_email.html')
                    c = {
					"email":user.profile.email,
					'domain':'www.dashme.ng',
					'site_name': 'Dashme',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'https',
					}
                    text_content = plaintext.render(c)
                    html_content = htmltemp.render(c)
                    try:
                        msg = EmailMultiAlternatives(subject, text_content,settings.EMAIL_HOST_USER, [user.profile.email], headers = {'Reply-To': settings.EMAIL_HOST_USER})
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.info(request, "A verification mail has been sent to your email, kindly complete registration from there. ")
                    return redirect ("home")
                    '''username = form.cleaned_data.get('username')
                    password = form.cleaned_data.get('password1')
                    user= authenticate(username=username,password=password)
                    login(request,user)
                    return redirect('account_update')'''
                else:
                    form = SignupForm()
                    messages.error(request,'form is invalid')
                    return redirect('signupuser')

        else:
            messages.error(request,'Password does not match')
            return redirect('signupuser')

    else:
        form = SignupForm()
        return render(request, 'givers/signupuser.html',{'form':form})


def contact(request):

    if request.method=='POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            email=form.cleaned_data.get('email')
            subject = "Dashme"
            plaintext = template.loader.get_template('password/contact_response.txt')
            htmltemp = template.loader.get_template('password/contact_response.html')
            c={
                'subject':form.cleaned_data.get('subject')
            }
            text_content = plaintext.render(c)
            html_content = htmltemp.render(c)
            msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email], headers = {'Reply-To': email})
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(request,'Thanks, we will treat as urgent')
            return redirect('contact')
    else:
        form=ContactUsForm()
        return render(request,'givers/contact.html',{'form':form})


def product_class(request):
    product=Give.objects.filter(product_class='premium',gift_status='unpicked')
    title='Hottest Deals'
    p=Paginator(product,20)
    page_number=request.GET.get('page')
    try:
        page_obj=p.get_page(page_number)
    except PageNotAnInteger:
        page_obj=p.page(1)
    except EmptyPage:
        page_obj=p.page(p.num_pages)

    return render(request,'givers/productCart.html',{'page_obj':page_obj,'title':title})


def product_category(request,category):
    product=Give.objects.filter(category=category,gift_status='unpicked').order_by('-date_posted')
    if category=='shoes':
        title='Footwear'
    elif category=='corporate':
        title='Corporate Wears'
    elif category=='natives':
        title='Native wears'
    else:
        title=category

    p=Paginator(product,20)
    page_number=request.GET.get('page')
    try:
        page_obj=p.get_page(page_number)
    except PageNotAnInteger:
        page_obj=p.page(1)
    except EmptyPage:
        page_obj=p.page(p.num_pages)

    return render(request,'givers/productCart.html',{'page_obj':page_obj,'title':title})


@login_required(login_url='/login/')
def user_account(request):
    user = request.user
    if user.profile.state=='lagos':
        fit=True
    else:
        fit=False

    online_payment= Transaction.objects.filter(made_by=str(user),verified=True)
    ondelivery_payment=OnDeliveryTransaction.objects.filter(made_by=str(user))
    orders=sorted(chain(online_payment,ondelivery_payment),key=lambda order: order.made_on, reverse=True)
    picks= Give.objects.filter(Q(gift_recipient=user.profile.email) & Q(gift_status='requested'))
    cart_items=picks.count


    if user.profile.state==None or user.profile.phone_number==8000000000:
        prof = get_object_or_404(Profile,user=request.user)
        profile_form= Profileform(instance=prof)
        return render (request, 'givers/account_update.html',{'user':user, 'profile_form':profile_form})
    return render(request,'givers/user_account.html',{'user':user,'picks':picks,'form':TransactionForm(),
                    'fit':fit,'cart_items':cart_items,'orders':orders})




@login_required(login_url='/login/')
def report(request):
    user = request.user
    give=Give.objects.filter(gift_recipient=request.user.username,gift_status='redeemed')
    if len(give)==0:
        amount=''
    else:
        amt=[]
        for i in give:
            if i.gift.payment_status == 'unpaid':
                if i.gift.amount is not None:
                    amt.append(i.gift.amount)
        if sum(amt)==0:
            amount=''
        else:
            amount=sum(amt,2000)
    offered =  Give.objects.filter(user=user)
    picks= Give.objects.filter(gift_recipient=user,date_requested__isnull=False)
    return render(request,'givers/report.html',{'picks':picks,'amount':amount,'offered':offered})




@login_required(login_url='/login/')
def logoutuser(request):
    logout(request)
    return redirect('home')


def loginuser(request):

    if request.method == 'GET':
        return render(request, 'givers/loginuser.html', {'form':AuthenticationForm(),'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})
    else:
        user= authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            messages.error(request,'Username or Password Incorrect')
            return redirect('loginuser')

        else:

            recaptcha_response = request.POST.get('g-recaptcha-response')
            print(recaptcha_response)
            data = {
			'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
			'response': recaptcha_response,
			}
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            print(r)
            result = r.json()
            print(result)
            if result['success']:
                login(request,user)
                if request.session.get('first_login'):
                    return redirect('account_update')
                return redirect('giveaway')
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('loginuser')



def creategift(request):

    if request.method == 'GET':
        return render(request,'givers/creategiving.html',{'form1':GiveawayForm()})

    else:
        form1=GiveawayForm(request.POST)
        if form1.is_valid():
            form1.save()
            messages.success(request,'Thank You for the thoughful gesture')
            return redirect('home')
        else:
            messages.error(request,'form is invalid')
            return render(request,'givers/creategiving.html',{'form1':GiveawayForm()})



def giveaway(request):
    user=request.user
    if user.is_anonymous:
        cartItem=''
    else:
        cartItem=Give.objects.filter(gift_recipient=user.profile.email, gift_status='requested').count

    gift1= Give.objects.latest('date_posted')
    query = request.GET.get('q')
    if query:
        gifts = Give.objects.filter(Q(date_requested__isnull = True)&Q(category__icontains=query)).order_by('-date_posted')
    else:
        gifts=  Give.objects.filter(date_requested__isnull = True).order_by('-date_posted')
    p=Paginator(gifts,60)
    page_number=request.GET.get('page')
    try:
        page_obj=p.get_page(page_number)
    except PageNotAnInteger:
        page_obj=p.page(1)
    except EmptyPage:
        page_obj=p.page(p.num_pages)
    return render(request,'givers/giftpage.html',{'page_obj':page_obj,'user':user,'gift1':gift1,'cartItem':cartItem})


def giveaway_category(request,category):
    user=request.user
    if user.is_anonymous:
        cartItem=''
    else:
        cartItem=Give.objects.filter(gift_recipient=user.profile.email, gift_status='requested').count

    gift1= Give.objects.latest('date_posted')

    house_category=['furniture','kitchen','groceries']
    electronics_category=['electronics','mobile','laptop']
    toy_category=['toys','bicycle']

    female_items=Give.objects.filter(Q(date_requested__isnull = True)&Q(gender='female'))
    male_items=Give.objects.filter(Q(date_requested__isnull = True)&Q(gender='male'))


    if category=='female shoes':
        gifts = female_items.filter(category='shoes').order_by('-date_posted')
    elif category=='female bags':
        gifts = female_items.filter(category='bag').order_by('-date_posted')
    elif category=='female clothes':
        gifts = female_items.filter(category='clothes').order_by('-date_posted')
    elif category=='female corporate':
        gifts = female_items.filter(category='corporate').order_by('-date_posted')
    elif category=='female accessories':
        gifts = female_items.filter(category='accessories').order_by('-date_posted')
    elif category=='beauty':
        gifts = female_items.filter(category='beauty').order_by('-date_posted')
    elif category=='male clothes':
        gifts=male_items.filter(category='clothes').order_by('-date_posted')
    elif category=='male corporate':
        gifts=male_items.filter(category='corporate').order_by('-date_posted')
    elif category=='male shoes':
        gifts=male_items.filter(category='shoes').order_by('-date_posted')
    elif category=='male natives':
        gifts=male_items.filter(category='natives').order_by('-date_posted')
    elif category=='toys':
        gifts = Give.objects.filter(Q(date_requested__isnull = True)&Q(category__in=toy_category)).order_by('-date_posted')
    elif category=='books':
        gifts = Give.objects.filter(Q(date_requested__isnull = True)&Q(category='book')).order_by('-date_posted')
    elif category=='electronics':
        gifts = Give.objects.filter(Q(date_requested__isnull = True)&Q(category__in=electronics_category)).order_by('-date_posted')
    elif category=='household-items':
        gifts = Give.objects.filter(Q(date_requested__isnull = True)&Q(category__in=house_category)).order_by('-date_posted')
    else:
        gifts=  Give.objects.filter(date_requested__isnull = True).order_by('-date_posted')
    p=Paginator(gifts,60)
    page_number=request.GET.get('page')
    try:
        page_obj=p.get_page(page_number)
    except PageNotAnInteger:
        page_obj=p.page(1)
    except EmptyPage:
        page_obj=p.page(p.num_pages)
    return render(request,'givers/giftpage.html',{'page_obj':page_obj,'user':user,'gift1':gift1,'cartItem':cartItem})



def viewgift(request,gift_id):
    user=request.user
    product = get_object_or_404(Give,pk = gift_id)
    if user.is_anonymous:
        cartItem=''
    else:
        cartItem=Give.objects.filter(gift_recipient=user.profile.email, gift_status='requested').count
    return render(request,'givers/detail_page.html',{'product':product,'cartItem':cartItem})



@login_required(login_url='/login/')
def edit_profile(request):
    user=request.user
    prof = get_object_or_404(Profile,user=request.user)
    if request.method == 'GET':
        profile_form= Profileform(instance=prof)
        return render (request, 'givers/account_update.html',{'user':user, 'profile_form':profile_form})
    else:
        profile_form = Profileform(request.POST,request.FILES,instance=prof)
        if  profile_form.is_valid():
            custom_form=profile_form.save(commit=False)
            custom_form.user=request.user
            custom_form.save()
            return redirect('user_account')
        else:
            return render(request,'givers/account_update.html',{'profile_form':profile_form,'error':'info not valid'})



@login_required(login_url='/login/')
def add_to_cart(request,gift_id):
    user=request.user
    pick= get_object_or_404(Give,pk=gift_id)
    current_time=timezone.now()
    three_days_ago=timezone.now()-timedelta(days=3)
    month_ago=timezone.now()-timedelta(days=30)
    premium=ShoppingCart.objects.filter(shopper=str(user),status='in-cart')
    picked_within_three_days=Give.objects.filter(gift_recipient=user.profile.email,date_requested__isnull=False,date_requested__range=[three_days_ago,current_time]).count()
    picked_within_a_month=Give.objects.filter(gift_recipient=user.profile.email,date_requested__isnull=False,date_requested__range=[month_ago,current_time]).count()
    day_cap=GiveawayCap.objects.get(name='days')
    month_cap=GiveawayCap.objects.get(name='month')

    if request.method=='POST':
        if pick.state == user.profile.state:
        #minimize gift per user to 4 gifts in 3days
            if picked_within_three_days <= day_cap.number:
                count=0
                if pick.product_class=='premium':
                    if premium:
                        for i in premium:
                            if i.product.product_class=='premium':
                                count+=1
                        if count>=1:
                            messages.error(request,'only one premium item per order')
                            return redirect('giveaway')

                pick.date_requested=timezone.now()
                pick.gift_recipient=user.profile.email
                pick.gift_status='requested'
                pick.save()
                data={
                    'shopper':user.profile.email,
                    'product':pick
                    }
                ShoppingCart.objects.create(**data)


            else:
                messages.error(request,'you have already picked 4 gifts within 3days')
                return redirect('giveaway')
        else:
                messages.info(request,f'gift only available in {pick.state}')

    return redirect('giveaway')



@login_required(login_url='/login/')
def delivery_options(request):
    user=request.user
    if request.method=='POST':
        if 'redeem' in request.POST:
            state=State.objects.get(name=user.profile.state)
            # city=PickupCentre.objects.filter(state=state.id)
            destination=DestinationCharge.objects.filter(state=state)

            return render(request,'givers/pickup_centre.html',{'destination':destination})

    return redirect('user_account')



@login_required(login_url='/login/')
def returnpicked(request,gift_id):
    user=request.user
    view = get_object_or_404(Give,pk = gift_id)
    if request.method== 'POST':
        view.date_requested=None
        view.gift_recipient=''
        view.gift_status='unpicked'
        view.save(update_fields=['date_requested','gift_recipient','gift_status'])
        ShoppingCart.objects.get(shopper=user.profile.email,product=view).delete()
    return redirect('user_account')



@login_required(login_url='/login/')
def checkout(request):
    user=request.user
    city=request.POST.get('city')
    destination=DestinationCharge.objects.get(city=city)
    products=ShoppingCart.objects.filter(shopper=user.profile.email,status='in-cart')
    if user.profile.state=='lagos':
        fit=True
    else:
        fit=False
    if request.method=='POST':
        request.session['address']=request.POST.get('address')
        request.session['contact']=request.POST.get('contact')

    delivery=destination.charge
    request.session['delivery']=delivery
    service=Charge.objects.get(name='standard')
    service_charge=service.charge
    amount=delivery+service_charge
    cart_items=products.count()
    tested_delivery=OnDeliveryTransaction.objects.filter(made_by=user.profile.email)
    if tested_delivery.count()>=1:
        tasted=True
    else:
        tasted=False
    return render(request,'givers/checkout.html',{'fit':fit,'amount':amount,'gifts':products,'cart_items':cart_items,'delivery':delivery,'service_charge':service_charge,'tasted':tasted})




def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data)|Q(username=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					plaintext = template.loader.get_template('password/password_reset_email.txt')
					htmltemp = template.loader.get_template('password/password_reset_email.html')
					c = {
					"email":user.email,
					'domain':'www.dashme.ng',
					'site_name': 'Dashme',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'https',
					}
					text_content = plaintext.render(c)
					html_content = htmltemp.render(c)
					try:
						msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [user.email], headers = {'Reply-To': settings.EMAIL_HOST_USER})
						msg.attach_alternative(html_content, "text/html")
						msg.send()
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					messages.info(request, "Password reset instructions have been sent to the email address entered.")
					return redirect ("home")


	password_reset_form = PasswordResetForm()
	return render(request,"password/password_reset.html",{"password_reset_form":password_reset_form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Thank you for your email confirmation. Now you can login your account.')
        return redirect('loginuser')
    else:
        return HttpResponse('Activation link is invalid!')




@login_required(login_url='/login/')
def initiate_payment(request):
    cost=request.session.get('delivery')
    delivery_address=request.session.get('address')
    contact=request.session.get('contact')
    user = request.user
    trans=Transaction()
    a,b,c=final_checkout(trans,user,cost,delivery_address,contact)
    total=a['amount']
    paystack_charge=b
    service_charge=c
    transaction=Transaction.objects.create(**a)

    return render(request,'givers/make_payment.html',{'transaction':transaction,'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY,
    'logistics':cost,'charge':paystack_charge,'total':total,'service_charge':service_charge})

@login_required(login_url='/login/')
def verify_payment(request,ref):
    user=request.user
    payment = get_object_or_404(Transaction,ref=ref)
    verified = payment.verify_payment()

    if verified:
        ShoppingCart.objects.filter(shopper=user.profile.email,status='in-cart').update(status='ordered')

        give=Give.objects.filter(gift_recipient=user.profile.email,gift_status='requested')
        for i in give:
            i.gift_status='ordered'
            i.save()
        messages.success(request, 'Payment Successful,you will be contacted soon for delivery')
    else:
        messages.error(request,"Payment Failed.")
    return redirect('user_account')


def my_mail(request):
    shape=request.session.get('selected')
    if request.method=='POST':
        form=SendEmailForm(request.POST)
        if form.is_valid:
            form.save(commit=False)

        msg=EmailMultiAlternatives('Dashme',form.cleaned_data.get('comment'),settings.EMAIL_HOST_USER,bcc=shape)
        msg.send()
    messages.success(request,'message sent')
    del request.session['selected']

    return redirect('/admin/givers/profile')


@login_required(login_url='/login/')
def on_delivery_payment(request):
    user=request.user
    cost=request.session.get('delivery')
    delivery_address=request.session.get('address')
    contact=request.session.get('contact')
    trans=OnDeliveryTransaction()
    a,c=final_checkout(trans,user,cost,delivery_address,contact)
    amount=a['amount']

    OnDeliveryTransaction.objects.create(**a)
    latest_on_delivery=OnDeliveryTransaction.objects.filter(made_by=user).latest('made_on')
    ref=latest_on_delivery.ref
    messages.success(request,'you will be contacted soon for delivery')
    plaintext = template.loader.get_template('password/invoice.txt')
    vat=0.075*c
    amount=amount+vat
    c={
        'amount':amount,
        'ref':ref,
        'ordered_giveaway':a['items'],
        'service_charge':c,
        'logistics':cost,
        'vat':vat
    }
    text_content = plaintext.render(c)

    subject = "Dashme invoice"
    msg = text_content
    to = request.user.email
    send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])

    ShoppingCart.objects.filter(shopper=user.profile.email,status='in-cart').update(status='ordered')
    give=Give.objects.filter(gift_recipient=user.profile.email,gift_status='requested')
    for i in give:
        i.gift_status='ordered'
        i.save()

    return redirect('user_account')


def ad_text(request):
    return render(request,'password/ads.txt')