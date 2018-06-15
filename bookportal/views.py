import braintree
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import render, redirect

from .models import Books
from .models import Profile
from .models import Purchase
from .models import Review

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id="3hrtz5z44xv9rc5h",
                                  public_key="njnd4544v5q2zd2h",
                                  private_key="604996d1b5f408541a9a34b34a18d373")


# Create your views here.

@login_required(login_url="/")
def profile(request, username):
    """
    user profile function
    """
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        profile.about = request.POST['about']
        profile.slogan = request.POST['slogan']
        profile.save()
    else:
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return redirect('/')
    return render(request, 'profile.html', {"profile": profile, })


def home(request):
    """
    home page which displays all the books
    """
    try:
        books = Books.objects.filter(status=True)
        return render(request, 'home.html', {'books': books})
    except Books.DoesNotExist:
        return redirect('/')


def book_details(request, id):
    """
    book detail page which diplays all the details of the book

    """
    if request.method == 'POST' and \
            not request.user.is_anonymous() and \
                    Purchase.objects.filter(book_id=id, buyer=request.user).count() > 0 and \
                    'content' in request.POST and \
                    request.POST['content'].strip() != '':
        Review.objects.create(content=request.POST['content'], book_id=id, user=request.user)

    try:
        book = Books.objects.get(id=id)
    except Books.DoesNotExist:
        return redirect('/')
    if request.user.is_anonymous() or \
                    Purchase.objects.filter(book=book, buyer=request.user).count() == 0 or \
                    Review.objects.filter(book=book, user=request.user).count() > 0:
        show_post_review = False
    else:
        show_post_review = Purchase.objects.filter(book=book, buyer=request.user).count() > 0

    reviews = Review.objects.filter(book=book)
    client_token = braintree.ClientToken.generate()
    return render(request, 'book_details.html', {"show_post_review": show_post_review, "reviews": reviews, "book": book,
                                                 "client_token": client_token})


@login_required(login_url="/")
def create_purchase(request):
    """
    function to purchase the product.

    """
    if request.method == 'POST':
        try:
            book = Books.objects.get(id=request.POST['book_id'])
        except Books.DoesNotExist:
            return redirect('/')

        nonce = request.POST["payment_method_nonce"]
        result = braintree.Transaction.sale({
            "amount": book.price,
            "payment_method_nonce": nonce
        })

        if result.is_success:
            Purchase.objects.create(book=book, buyer=request.user)

    return redirect('/')


@login_required(login_url="/")
def my_buyings(request):
    """
    function to list all the books user purchased

    """
    try:
        my_purchase = Purchase.objects.filter(buyer=request.user)
    except Purchase.DoesNotExist:
        return redirect('/')
    return render(request, 'my_buyings.html', {'purchases': my_purchase})


@login_required(login_url="/")
def pdf_view(request, id):
    """
    function to see the pdf file user purchased
    """

    try:
        my_purchase = Purchase.objects.get(buyer=request.user, book_id=id)
        book_id = my_purchase.book_id

        try:
            file = Books.objects.get(id=book_id)
            filename = str(file.file)
            return FileResponse(open(settings.MEDIA_ROOT + '/' + filename, 'rb'), content_type='application/pdf')
        except Books.DoesNotExist:
            return redirect('/')
            #
        return redirect('/')
    except IOError:
        raise Http404()


def search(request):
    """
    function to search the product.
    """

    books = Books.objects.filter(title__contains=request.GET['title'])
    return render(request, 'home.html', {"books": books})
