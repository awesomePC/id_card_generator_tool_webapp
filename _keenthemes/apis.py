from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from projects.models import Users
from django.shortcuts import redirect

class Viewss:
    @api_view(['POST'])
    def sign_in(request):
        email=request.POST['email']
        password=request.POST['password']
        user=Users.objects.filter(Email=email,Password=password)
        exists=user.exists()
        if exists is True:
            request.session['isAuthenticated']=True
            rec=user[:1].get()
            request.session['user']={
                'id':rec.id,
                'firstname':rec.FirstName,
                'lastname':rec.LastName,
            }
            if rec.Role != None:
                request.session['role']=rec.Role.Name
            return redirect('/')

        request.session['message']='Invalid username or password'
        return redirect('/signin')
    @api_view(['POST'])
    def sign_up(request):
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        password=request.POST['password']
        isUnique=Users.objects.filter(Email=email).exists() is False
        
        if isUnique is True:
            newUser=Users(FirstName=firstname,LastName=lastname,Email=email,Password=password,Role_id=1)
            newUser.UpdatedDate=None
            newUser.save()
            return redirect('/signin')

        request.session['message']='Please choose unique email'
        return redirect('/signup')