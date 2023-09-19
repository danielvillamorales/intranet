from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from permisos.models import Beneficios
from permisos.models import Tipodepermiso
from permisos.models import Permisos
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User,Permission,ContentType,Group
from django.contrib.auth.decorators import login_required
from permisos.forms import PermisosForm
import datetime
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from os import walk, getcwd, path
from permisos.models import UsuarioEncargado
import json
import pytz
# Create your views here.
@login_required
def permisos(request):
    user = get_object_or_404(User, username = request.user)
    encargados = UsuarioEncargado.objects.filter(encargado=user).values('usuario')
    if user.has_perm('permisos.ver_permisos_de_todos'):
        lista_permisos = Permisos.objects.all().order_by('-fechaInicial')
        usuarios = User.objects.filter(is_active=True).order_by('first_name')
    else:
        lista_permisos = Permisos.objects.filter(Q(usuariodepermiso=user.id) | Q(usuariodepermiso__in = encargados)).order_by('-fechaInicial')
        usuarios = User.objects.filter(Q(is_active=True, id = user.id) | Q(is_active = True, id__in = encargados )).order_by('first_name')   
    motivos = Tipodepermiso.objects.all()
    if request.method == 'POST':
        id_solicitado_por = request.POST.get('solicitado_por', False)
        id_estado = request.POST.get('estado', False)
        id_motivo = request.POST.get('motivo', False)
        if id_solicitado_por:
            solicitado_por = User.objects.get(pk=int(id_solicitado_por))
            print(solicitado_por)
            lista_permisos = Permisos.objects.filter(Q(usuariodepermiso=solicitado_por)).order_by('-fechaInicial')
        if user.has_perm('permisos.ver_permisos_de_todos'):
            if id_estado:
                lista_permisos = Permisos.objects.filter(estado=id_estado).order_by('-fechaInicial')
            
            if id_motivo:
                motivo = Tipodepermiso.objects.get(pk=int(id_motivo))
                lista_permisos = Permisos.objects.filter(tipopermiso=motivo).order_by('-fechaInicial')
        else:
            if id_estado:
                lista_permisos = Permisos.objects.filter(Q(usuariodepermiso=user.id) | Q(usuariodepermiso__in = encargados)).filter(estado=id_estado).order_by('-fechaInicial')
            
            if id_motivo:
                motivo = Tipodepermiso.objects.get(pk=int(id_motivo))
                lista_permisos = Permisos.objects.filter(Q(usuariodepermiso=user.id) | Q(usuariodepermiso__in = encargados)).filter(tipopermiso=motivo).order_by('-fechaInicial')
        if id_estado or id_motivo or id_solicitado_por:
             return render(request,'permisos.html',{'lista_permisos':lista_permisos,'usuarios':usuarios,'motivos':motivos})
    page = request.GET.get('page', 1)
    paginator = Paginator(lista_permisos, 20)
    try:
        lista_permisos_pg = paginator.page(page)
    except PageNotAnInteger:
        lista_permisos_pg = paginator.page(1)
    except EmptyPage:
        lista_permisos_pg = paginator.page(paginator.num_pages)
    return render(request,'permisos.html',{'lista_permisos':lista_permisos_pg,'usuarios':usuarios,'motivos':motivos})


@login_required
def agregar_permisos(request):
    format = '%Y-%m-%dT%H:%M'
    user = get_object_or_404(User, username = request.user)
    if user.has_perm('permisos.ver_permisos_de_todos'):
        usuarios = User.objects.filter(is_active=True).order_by('first_name')
    else:
        usuarios = [user,]
    motivos = Tipodepermiso.objects.all()
    beneficios = Beneficios.objects.filter(estado=1)   
    
    if request.method == 'POST':
        formulario = PermisosForm(request.POST)
        if formulario.is_valid():
            print(request.POST.get('get_fechainicial'))
            if request.POST.get('get_fechainicial') =='':
                messages.error(request,'error en las fechas dadas')
                return redirect('nuevo_permiso')
            else:
                fecha_inicial = datetime.datetime.strptime(request.POST.get('get_fechainicial'),format)
                fecha_final = datetime.datetime.strptime(request.POST.get('get_fechafinal'),format)
                evaluar = formulario.save(commit=False)
                if len(UsuarioEncargado.objects.filter(usuario=evaluar.usuariodepermiso)) == 0:
                    messages.error(request,'El usuario no tiene un encargado asignado')
                    return redirect('nuevo_permiso')
                if evaluar.tipopermiso.id  == 2 and evaluar.beneficio.id != 9:
                    buscarbeneficio = Permisos.objects.filter(usuariodepermiso = evaluar.usuariodepermiso.id).filter(beneficio = evaluar.beneficio.id).filter(fechaInicial__year = str(fecha_inicial.year)).count()
                    if buscarbeneficio > 0:
                        messages.error(request,'El beneficio ya fue montado en el año no se puede solicitar nuevamente')
                        return redirect('nuevo_permiso')
                    else:
                        post = formulario.save()
                        post.fechaInicial = fecha_inicial
                        post.fechaFinal = fecha_final
                        post.fechacreacion = datetime.datetime.now()
                        post.usuariodecreacion = user
                        post.save()                        
                else:
                    post = formulario.save()
                    post.fechaInicial = fecha_inicial
                    post.fechaFinal = fecha_final
                    post.fechacreacion = datetime.datetime.now()
                    post.usuariodecreacion = user
                    post.save()
            return redirect('permisos')
    else:
        formulario = PermisosForm()
    return render(request,'nuevo_permiso.html',{'formulario':formulario,'usuarios':usuarios,'motivos':motivos,'beneficios':beneficios})

@login_required
def aprobar_permisos(request,id):
    user = get_object_or_404(User, username = request.user)
    permiso = get_object_or_404(Permisos, pk=id)
    encargado = UsuarioEncargado.objects.filter(encargado=user, usuario=permiso.usuariodepermiso)
    if user.has_perm('permisos.aprobar_permisos'):
        if permiso:
            if permiso.estado == 1:
                messages.warning(request,'El permiso ya se encuentra aprobado')
            elif permiso.estado == 2 :
                messages.warning(request,'El permiso ya se encuentra rechazado')
            else:
                permiso.estado = 1
                permiso.usuarioaprobacion = user
                permiso.fechaaprobacion = datetime.datetime.now()
                permiso.save()
                messages.success(request,'Se aprobó el permiso')
        else:
            messages.error(request,'no se pudo realizar la operacion')
        return redirect('permisos')
    elif (len(encargado) > 0):
        if permiso:
            if permiso.estado == 1:
                messages.warning(request,'El permiso ya se encuentra aprobado')
            elif permiso.estado == 2 :
                messages.warning(request,'El permiso ya se encuentra rechazado')
            else:
                permiso.estado = 1
                permiso.usuarioaprobacion = user
                permiso.fechaaprobacion = datetime.datetime.now()
                permiso.save()
                messages.success(request,'Se aprobó el permiso')
        else:
            messages.error(request,'no se pudo realizar la operacion')
        return redirect('permisos')
    else:
        messages.error(request,'No tiene permisos suficientes para aprobar los permisos de este empleado')
        return redirect('permisos')

@login_required
def rechazar_permisos(request,id):
    user = get_object_or_404(User, username = request.user)
    permiso = get_object_or_404(Permisos, pk=id)
    encargado = UsuarioEncargado.objects.filter(encargado=user, usuario=permiso.usuariodepermiso)
    if user.has_perm('permisos.aprobar_permisos'):
        if permiso:
            if permiso.estado == 1:
                messages.error(request,'No se puede rechazar dado que su estado es aprobado')
            else:
                permiso.estado = 2
                permiso.usuarioaprobacion = user
                permiso.fechaaprobacion = datetime.datetime.now()
                permiso.save()
                messages.warning(request,'Se rechazo el permiso')
        else:
            messages.error(request,'No se pudo realizar operacion')
        return redirect('permisos')
    elif (len(encargado) > 0):
        if permiso:
            if permiso.estado == 1:
                messages.error(request,'No se puede rechazar dado que su estado es aprobado')
            else:
                permiso.estado = 2
                permiso.usuarioaprobacion = user
                permiso.fechaaprobacion = datetime.datetime.now()
                permiso.save()
                messages.warning(request,'Se rechazo el permiso')
        else:
            messages.error(request,'No se pudo realizar operacion')
        return redirect('permisos')

    else:
        messages.error(request,'No tiene permisos suficientes para aprobar')
        return redirect('permisos')

@login_required
def entrada_permisos(request, id ):
    permiso = get_object_or_404(Permisos, pk=id)
    user = get_object_or_404(User, username = request.user)
    if user.has_perm('permisos.salida_y_entrada'):
        if permiso:
            if permiso.reingreso is None:
                permiso.reingreso=datetime.datetime.now()
                permiso.save()
                messages.success(request,f'hora de reingreso {datetime.datetime.now()}')
            else:
                messages.error(request,'ya se dio una hora de reingreso')
        else:
            messages.error(request,'no se pudo actulizar la hora')
    else:
        messages.error(request,'No tienes permiso para dar la hora de de reingreso')
    return redirect('permisos')

@login_required
def salida_permisos(request,id):
    permiso = get_object_or_404(Permisos, pk=id)
    user = get_object_or_404(User, username = request.user)
    if user.has_perm('permisos.salida_y_entrada'):
        if permiso:
            if  permiso.salida is None:
                tz = pytz.timezone('America/Bogota')
                permiso.salida=datetime.datetime.now()
                permiso.save()
                messages.success(request,f'hora de salida {datetime.datetime.now()}')
            else:
                messages.error(request,'ya se dio una hora de salida')
        else:
            messages.error(request,'no se pudo actulizar la hora')
    else:
        messages.error(request,'No tienes permiso para dar la hora de salida')
    return redirect('permisos')

def normalize(s):
    replacements = (
        ('á', 'a'),
        ('é', 'e'),
        ('í', 'i'),
        ('ó', 'o'),
        ('ú', 'u'),
        ('-', ''),
        ('_', ''),
        ('*', ''),
        ('.', ''),
        (' ', ''),
        ('C:\\Users\\danie\\Desktop\\pruebadir',''),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

def contenidojson(request):
    directorio ={}
    directorio["id"]=normalize('sgc')
    directorio["parent"]='#'
    directorio["text"]='sgc'
    lista = []
    lista.append(directorio.copy())
    
    for root, dirs, files in walk('./sgc/',True):
        #print("root:%s"%normalize(str(root)))
        #print("dirs:%s"%(dirs))
        #print("files:%s"%files)
        #print("-------------------------------")
        for dir in dirs:
            directorio["id"]=normalize(dir)
            directorio["parent"]=normalize(path.basename(root))
            directorio["text"]=dir
            lista.append(directorio.copy())
    #print(lista)
    return JsonResponse(lista,safe=False)

@login_required
def sgc(request):
    lista = []
    directorio = ('sgc','#','sgc',0,'#')
    lista.append(directorio[:]) 
    root_anterior = '#'
    lista2=[]
    directorio2=[]
    contador=0 
    for root, dirs, files in walk('./static/sgc',True):
        #print("root:%s"%normalize(str(root)))
        #print("dirs:%s"%(dirs))
        #print("files:%s"%files)
        #print("-------------------------------")
        for dir in dirs:
            if root_anterior != normalize(path.basename(root)): 
                root_anterior =  normalize(path.basename(root))
            directorio = (normalize(dir),normalize(path.basename(root)),str(dir),0,root_anterior)
            lista.append(directorio[:])
        for file in files:
            if file.lower().endswith('.jpg') or file.lower().endswith('.png') or file.lower().endswith('.pdf'):
                contador=contador+1
                if root_anterior != normalize(path.basename(root)): 
                    root_anterior =  normalize(path.basename(root))
                directorio2 = ('file_'+str(contador)+'_'+str(normalize(dir)),normalize(path.basename(root)),str(file),1,str(path.join(root+'/'+file)).replace('./','').replace('static/sgc','').replace('\\','/'))
                lista2.append(directorio2[:])
    contador =0 
    for l in lista2:
        contador = contador+1
        #print(l[4], contador)
    return render(request,'sgc.html',{'lista':lista,'archivos':lista2})

@login_required
def calidad(request):
    beneficios = Beneficios.objects.filter(estado=1).order_by('id') 
    return render(request,'calidad.html',{'beneficios':beneficios})