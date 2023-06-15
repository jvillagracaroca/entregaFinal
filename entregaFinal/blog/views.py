from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import PerfilUsuarioForm, PublicacionForm, RegistrarForm
from .models import Comentario, Publicacion


def home(request):
    login_error = request.COOKIES.get('login_error')
    if login_error:
        context = {'login_error': login_error}
    else:
        context = {}
    return render(request, 'home.html', context)


def registrar(request):
    if request.method == 'POST':
        form = RegistrarForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('Home')  # Redireccionar a la página de inicio
        else:
            # Agregar mensaje de error al campo de confirmación de contraseña
            form.add_error('password2', 'Las contraseñas no coinciden')
    else:
        form = RegistrarForm()
    return render(request, 'registrar.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url) 
            else:
                return redirect('Home')
        else:
            return HttpResponseRedirect(reverse('Home') + '?login_error=Credenciales inválidas. Inténtalo de nuevo.')

    return JsonResponse({'success': False, 'message': 'Acceso no permitido.'})


def logout_view(request):
    logout(request)
    return redirect('Home')  # Redireccionar al inicio

@login_required
def crearPublicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            cuerpo = form.cleaned_data['cuerpo']
            imagen_portada = form.cleaned_data['imagen_portada']
            publicacion = Publicacion(titulo=titulo, cuerpo=cuerpo, autor=request.user, imagen_portada=imagen_portada)
            publicacion.save()
            return redirect('Home')
    else:
        form = PublicacionForm(initial={'csrfmiddlewaretoken': get_token(request)})
    
    return render(request, 'publicacion.html')



def mostrarPublicaciones(request):
    publicaciones = Publicacion.objects.all()
    return render(request, 'publicaciones.html', {'publicaciones': publicaciones})


def detallePublicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    return render(request, 'detallePublicacion.html', {'publicacion': publicacion})

@login_required
def agregarComentario(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    contenido = request.POST.get('contenido')
    autor = request.user

    if contenido:
        comentario = Comentario(publicacion=publicacion, autor=autor, contenido=contenido)
        comentario.save()

    next_url = request.POST.get('next')
    if next_url:
        return redirect(next_url)
    else:
        publicaciones = Publicacion.objects.all()
        return render(request, 'publicaciones.html', {'publicaciones': publicaciones})


@login_required
def eliminarComentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    if comentario.autor == request.user:
        comentario.delete()
        messages.success(request, 'Comentario eliminado correctamente.')
    else:
        messages.error(request, 'No tienes permiso para eliminar este comentario.')
    
    return redirect(request.META.get('HTTP_REFERER', 'Home'))

@login_required
def editarComentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)

    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        if contenido:
            comentario.contenido = contenido
            comentario.save()
            messages.success(request, 'Comentario actualizado correctamente.')
        else:
            messages.error(request, 'El contenido del comentario no puede estar vacío.')

    return redirect('detallePublicacion', pk=comentario.publicacion.pk)


def filtrarPublicaciones(request):
    query = request.GET.get('q') 
    if query:
        publicaciones = Publicacion.objects.filter(titulo__icontains=query) | Publicacion.objects.filter(cuerpo__icontains=query) | Publicacion.objects.filter(autor__username__icontains=query)
    else:
        publicaciones = Publicacion.objects.all()
    return render(request, 'publicaciones.html', {'publicaciones': publicaciones})

@login_required
def perfil(request):
    user = request.user

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redireccionar al perfil después de guardar los cambios
    else:
        form = PerfilUsuarioForm(instance=user)

    return render(request, 'perfil.html', {'form': form})

@login_required
def actualizarPerfil(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        email = request.POST['email']
        password = request.POST['password1']

        # Actualizar los datos del usuario
        user = request.user
        user.email = email
        if password:
            user.set_password(password)
        user.save()

        messages.success(request, 'Los cambios del perfil han sido guardados exitosamente.')

    return redirect('perfil')

def eliminar_publicacion(request, publicacion_id):
    publicacion = Publicacion.objects.get(id=publicacion_id)
    if request.user == publicacion.autor:
        publicacion.delete()
        messages.success(request, 'Publicación eliminada.')
    else:
        messages.error(request, 'No tienes permiso para eliminar esta publicación.')
    
    return redirect(request.META.get('HTTP_REFERER', 'Home'))