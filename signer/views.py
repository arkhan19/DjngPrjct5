from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, forms
from posts import views
from django.core.mail import EmailMessage

# Create your views here.


def signup(request):
    # request's method in form html tag is equal to POST or not? Else the url will show the input data in the form. So
    # we go through method == post check first.
    if request.method == 'POST':
        # this condition will check if the password entered in both the parameters is equal else throw an error.
        if request.POST['pass1'] == request.POST['pass2']:
            # Try block to give an error if username already taken by some other user.
            try:
                # imported from User module, checks all objects from database using get function and compare them with
                # the form username.
                User.objects.get(username = request.POST['Username'])
                # if tried and found a conflict in username, throw the return, else it goes in except part
                return render(request, 'signer/signup.html', {'error': 'Username Already Taken'})
            # if User does not exist in database
            except User.DoesNotExist:
                # create a user with username and password from POST function
                user = User.objects.create_user(request.POST['Username'], password=request.POST['pass1'],
                                                email=request.POST['emaik'])
                login(request, user)
                # finally return the signup html after successfull completion
            return render(request, 'signer/signup.html')
        else:
            # if the password doesn't match.
            return render(request, 'signer/signup.html', {'error' : 'Passwords didn\'t match'})
    else:
        # if the request is GET and not POST.
        return render(request, 'signer/signup.html')


def log_in(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['Username'], password=request.POST['pass1'])
        if user is not None:
            login(request, user)
            if 'next' in request.POST:  # checks if next is in POST, so that it doesn't get stuck when no next.
                # redirecting after logging in; POST = post function not Post App.
                return redirect(request.POST['next'])
                # return render(request, 'signer/login.html', {'error': 'I WENT IN'})
            else:
                return redirect('home')
        else:
            return render(request, 'signer/login.html', {'error': 'Wrong Credentials! Try Again'})
    else:
        return render(request, 'signer/login.html')


def signout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


# def re_set(request):
#     if request.method == 'POST':
#         return render(request, 'signer/reset.html')
#     else:
#         return render(request, 'signer/reset.html')
#
#     # if request.method == 'POST':
#     #     u_r_l = request.POST['u_r_l']
#     #     if u_r_l is not None:
#     #         ux = User.objects.get(email = request.POST[u_r_l])
#     #         email = EmailMessage('Registered on DJNG PRJCT 3',
#     #                              ux,
#     #                              to=[request.POST['u_r_l']])
#     #         email.send()
#     #         if 'next' in request.POST:  # checks if next is in POST, so that it doesn't get stuck when no next.
#     #             # redirecting after logging in; POST = post function not Post App.
#     #             return redirect(request.POST['next'])
#     #         # return render(request, 'signer/reset.html')
#     #         else:
#     #             return redirect('home')
#     #     else:
#     #         return render(request, 'signer/signup.html', {'error': 'Create a new User'})
#     # else:
#     #
#
#
