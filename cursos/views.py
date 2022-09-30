from pyexpat.errors import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Aulas, Cursos, Comentarios, NotasAulas
from django.contrib.auth.models import User
import json
from django.contrib.messages import constants
from django.contrib import messages


@login_required(login_url='/auth/login?status=1')
def home(request):
    if request.method == 'GET':
        cursos = Cursos.objects.all()
        return render(request, 'home.html', {'cursos':cursos})

    

@login_required(login_url='/auth/login?status=2')
def aulas(request, id_curso):

    aulas = Aulas.objects.filter(curso_id=id_curso)
    return render(request, 'aulas.html', {'aulas':aulas})


@login_required(login_url='/auth/login?status=3')
def ver_aula(request, id):

    id_usuario = request.user.id
    comentarios = Comentarios.objects.filter(aula_id=id).order_by('-data')
    avaliacao_usuario = NotasAulas.objects.filter(aula_id=id).filter(usuario_id=id_usuario)
    avaliacoes_all = NotasAulas.objects.filter(aula_id=id)
    print(avaliacoes_all)
    aula = Aulas.objects.get(id=id)

    return render(request, 'aula.html',
                            {
                            'id_usuario':id_usuario,
                            'comentarios':comentarios,
                            'aula':aula,
                            'avaliacao_usuario':avaliacao_usuario,
                            'avaliacao_all':avaliacoes_all
                            })
@login_required(login_url='/auth/login?status=1')
def comentarios(request):
    if request.method == 'POST':
        usuario = int(request.POST.get('id_usuario'))
        comentario = request.POST.get('comentario')
        aula=int(request.POST.get('aula_id'))

        if len(comentario.strip()) == 0:
            return 
        try:
            comentario = Comentarios(
                                    usuario_id=usuario,
                                    comentario=comentario,
                                    aula_id=aula,
                                    )   
            comentario.save()

            
            comentarios = Comentarios.objects.filter(aula_id = aula).order_by('-data')
            somente_nomes = [i.usuario.username for i in comentarios]
            somente_comentarios = [i.comentario for i in comentarios]
                       
            comentarios = list(zip(somente_nomes, somente_comentarios))
           
        

            return HttpResponse(json.dumps({'status': '1', 'comentarios': comentarios }))
        

            
        except:
            return HttpResponse(json.dumps({'status': '2'}))
   
   
@login_required(login_url='/auth/login')
def processa_avaliacao(request):

    avaliacao = request.POST.get('avaliacao')
    aula_id = request.POST.get('aula_id')
    
    usuario_id = request.user.id

    usuario_avaliou = NotasAulas.objects.filter(aula_id = aula_id).filter(usuario_id = usuario_id)

    if not usuario_avaliou:
        nota_aulas = NotasAulas(aula_id = aula_id,
                                nota = avaliacao,
                                usuario_id = usuario_id,
                                )
        nota_aulas.save()
        return redirect(f'/cursos/aulas/{aula_id}')
    else:
        messages.add_message(request, constants.ERROR, 'Você já avaliou essa aula.')
        return redirect(f'/cursos/aulas/{aula_id}')

