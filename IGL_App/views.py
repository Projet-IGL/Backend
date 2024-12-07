from django.shortcuts import render, redirect
from .models import Staff
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from django.contrib.sessions.models import Session

def login_view(request):
    if request.method == 'POST':
      
        print("POST request received")  # Debug print
        email = request.POST.get('email', '').strip()  # Get and clean the email input
        password = request.POST.get('password', '').strip()  # Get and clean the password input

        # Debug: Print the input values
        print(f"Received email: {email}")
        print(f"Received password: {password}")
        print("All users in the database:")
        for user in Staff.objects.all():
         print(f"Email: {user.email}, Password: {user.mot_de_passe}")
          
              

        try:
            # Attempt to find the user by email
            user = Staff.objects.get(email=email)
            print(f"Found user with email: {user.email}")  # Debug print

            # Verify the password
            if user.mot_de_passe.strip() == password:
                print("Password matches!")  # Debug print
                # Manually set the user in the session
                request.session['user_id'] = user.id
                messages.success(request, 'Login successful!')
                return redirect('home')  # Redirect to the home page
            else:
                print("Password does not match.")  # Debug print
                messages.error(request, 'Incorrect password')
        except Staff.DoesNotExist:
            print(f"User not found with email: {email}")  # Debug print
            messages.error(request, 'User not found')

    # Render the login page if the request is not POST or if authentication fails
    return render(request, 'login.html')
def home(request):
    return render(request, 'home.html')