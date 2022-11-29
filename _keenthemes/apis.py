from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from auth.models import Users
from projects.models import Projects
from tasks.models import Tasks
from django.shortcuts import redirect
from django.http import JsonResponse

class Viewss:
    @api_view(['POST'])
    def sign_in(request):
        email=request.POST['email']
        password=request.POST['password']
        user=Users.objects.filter(Email=email,Password=password)
        exists=user.exists()
        if exists is True:
            request.session['isAuthenticated']=True
            request.session['email']=email
            rec=user[:1].get()
            request.session['user']={
                'id':rec.id,
                'firstname':rec.FirstName,
                'lastname':rec.LastName,
            }
            if rec.Role != None:
                request.session['role']=rec.Role
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
            newUser=Users(FirstName=firstname,LastName=lastname,Email=email,Password=password,Role="Annonater")
            newUser.UpdatedDate=None
            newUser.save()
            return redirect('/signin')

        request.session['message']='Please choose unique email'
        return redirect('/signup')
    
    def delete_project(request):
        id=request.GET.get('id',None)
        if id != None:
            rec=Projects.objects.get(id=id)
            rec.delete()
        return redirect('/projects/list')

    def delete_task(request):
        id=request.GET.get('id',None)
        if id != None:
            rec=Tasks.objects.get(id=id)
            rec.delete()
        return redirect('/tasks/list')

    def task_detail(request):
        id=request.GET.get('id',None)
        if id != None:
            rec=Tasks.objects.get(id=id)
        return JsonResponse({
            'MainImageFile':str(rec.MainImageFile),
            'TextRemovedImageFile':str(rec.TextRemovedImageFile),
            'WordAnnotationList':rec.WordAnnotationList
        })
    
    def userinfo(request):
        data=request.session.get('user',None)
        email=request.session.get('email',None)
        data['email']=email
        return JsonResponse(data)