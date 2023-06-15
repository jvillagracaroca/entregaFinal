from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

app_name='blog'

urlpatterns = [
    path('', views.home, name="Home"),
    path('registrar/', views.registrar, name='registrarUsuario'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('publicacion/', views.crearPublicacion, name='crearPublicacion' ), 
    path('publicaciones/', views.mostrarPublicaciones, name='verPublicaciones'),
    path('publicacion/<int:pk>/', views.detallePublicacion, name='detallePublicacionPK'),
    path('publicacion/<int:pk>/comentar/', views.agregarComentario, name='agregarComentario'),
    path('comentario/<int:pk>/eliminar/', views.eliminarComentario, name='eliminarComentario'),
    path('comentario/<int:pk>/editar/', views.editarComentario, name='editarComentario'),
    path('filtrarPublicaciones/', views.filtrarPublicaciones, name="filtraPublicaciones"),
    path('perfil/', views.perfil, name='perfil'),
    path('actualizarPerfil/', views.actualizarPerfil, name='actualizarPerfil'),
    path('publicacion/<int:publicacion_id>/eliminar/', views.eliminar_publicacion, name='eliminarPublicacion'),
    path('about/', views.about ,name='about'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
