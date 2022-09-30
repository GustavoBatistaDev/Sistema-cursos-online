from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth
from django.db.models import Q
import re    


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'GET':
        return render(request, 'cadastro.html')

    elif request.method == 'POST':
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        repetir_senha = request.POST.get('repetir_senha')

        if len(usuario.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or len(repetir_senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Nenhum campo pode ser nulo.')
            return render(request, 'cadastro.html',{'usuario':usuario, 'email': email, 'senha':senha, 'repetir_senha': repetir_senha})


   
        query = Q(
            Q(email=email)|Q(username=usuario)
               )
        user = User.objects.filter(query)

        if len(user) > 0:
            messages.add_message(request, constants.ERROR, 'Usuário já cadastrado.')
            return render(request, 'cadastro.html',{'usuario':usuario, 'email': email, 'senha':senha, 'repetir_senha': repetir_senha})

        elif not usuario.isalpha():
            messages.add_message(request, constants.ERROR, 'Insira um nome válido.')
            return render(request, 'cadastro.html',{'usuario':usuario, 'email': email, 'senha':senha, 'repetir_senha': repetir_senha})
        
        elif not re.search('[0-9]', senha):
            messages.add_message(request, constants.ERROR, 'Sua senha precisa ter caracteres numéricos.')
            return render(request, 'cadastro.html',{'usuario':usuario, 'email': email, 'senha':senha, 'repetir_senha': repetir_senha})

        elif not re.search('[A-Z]', senha):
            messages.add_message(request, constants.ERROR, 'Sua senha precisa ter letras maiúsculas.')
            return render(request, 'cadastro.html',{'usuario':usuario, 'email': email, 'senha':senha, 'repetir_senha': repetir_senha})

        elif not re.search('[a-z]', senha):
            messages.add_message(request, constants.ERROR, 'Sua senha precisa ter letras minúsculas.')
            return render(request, 'cadastro.html',{'usuario':usuario, 'email': email, 'senha':senha, 'repetir_senha': repetir_senha})
        
        elif len(senha) < 8 or len(senha) > 15:
            messages.add_message(request, constants.ERROR, 'Sua senha precisa ter no mínimo 8 caracteres e no máximo 15.')
            return render(request, 'cadastro.html',{'usuario':usuario, 'email': email, 'senha':senha, 'repetir_senha': repetir_senha})

        elif senha != repetir_senha:
            messages.add_message(request, constants.ERROR, 'Senhas não conferem.')
            return render(request, 'cadastro.html',{'usuario':usuario, 'email': email, 'senha':senha, 'repetir_senha': repetir_senha})
    
        try:
            user = User.objects.create_user(username=usuario, email=email, password=senha)
            user.save()
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso.')
            return redirect('login')

        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema.')
            return render(request, 'cadastro.html', {'usuario':usuario, 'email': email, 'senha':senha, 'repetir_senha': repetir_senha})


        
def login(request):

    status = request.GET.get('status')

    if status == '3':
        messages.add_message(request, constants.ERROR, 'Faça login para acessar a aula.')
        return redirect('login')

    if status == '2':
        messages.add_message(request, constants.ERROR, 'Faça login para acessar as aulas.')
        return redirect('login')
    
    if status == '1':
        messages.add_message(request, constants.ERROR, 'Faça login para acessar a plataforma.')
        return redirect('login')
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        usuario = request.POST.get('usuario')

        senha = request.POST.get('senha')

        user = auth.authenticate(username=usuario, password=senha)
        if user:
            auth.login(request, user)
            return redirect('home')

        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos.')
            return redirect('login')

        
def logout(request):
    auth.logout(request)
    return redirect('login')


        

