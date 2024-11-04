from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from .models import bmidata


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user_id'] = user.id
            print(request.session['user_id'])
            return redirect('main_page')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('login')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Passwords don\'t match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def main_page(request):
    if request.method == 'POST':
        print(request.session['user_id'])
        height = float(request.POST['height']) / 100  # Convert cm to meters
        weight = float(request.POST['weight'])
        height_1 = request.POST['height'] # Convert cm to meters
        weight_1 = request.POST['weight']
        age = int(request.POST['age'])
        gender = request.POST['gender']

        if height <= 0 or weight <= 0 or age <= 0 or not gender:
            return JsonResponse({'error': 'Please enter valid values for all fields.'}, status=400)

        bmi = weight / (height * height)
        bmi = round(bmi, 2)
        print("your BMI "+str(bmi))
        if not bmi or not age or not gender:
            return JsonResponse({'error': 'Please ensure all information is correctly provided before generating a diet plan.'}, status=400)

        if bmi < 18.5:
            diet_plan = 'Your BMI indicates that you are underweight. A diet rich in proteins, healthy fats, and complex carbohydrates is recommended.'
        elif 18.5 <= bmi < 24.9:
            diet_plan = 'Your BMI is normal. Maintain a balanced diet including a variety of nutrients.'
        elif 25 <= bmi < 29.9:
            diet_plan = 'Your BMI indicates that you are overweight. A diet with reduced calories, more fruits and vegetables, and regular exercise is recommended.'
        elif 30 <= bmi < 40.9:
            diet_plan = 'Your BMI indicates that you are obese. A strict diet plan under the guidance of a healthcare provider is recommended.'
        print(diet_plan)

        if bmidata.objects.filter(user_id = request.session['user_id']).count() != 0:
           last_bmi = bmidata.objects.get(user_id = request.session['user_id']).bmi 
           bmidata.objects.filter(user_id = request.session['user_id']).update(bmi = bmi)
        else:
            name =  User.objects.get(id = request.session['user_id']).username
            user = bmidata.objects.create(user_id=request.session['user_id'], name=name, height=height, weight=weight, bmi=bmi)
            user.save()
            last_bmi = bmidata.objects.get(user_id = request.session['user_id']).bmi            
        return render(request,'bmi.html',{"height":height_1,"weight":weight_1,"age":age,"gender":gender,"bmi":bmi,"text":diet_plan,"last_bmi":last_bmi})
        return JsonResponse({'diet_plan': diet_plan})

        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    return render(request, 'bmi.html')

def main_page2(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user_id'] = user.id
            return redirect('main_page')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'main.html')

    return render(request, 'main.html')
