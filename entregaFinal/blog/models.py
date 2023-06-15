from django.contrib.auth.models import AbstractUser, User
from django.db import models



class Usuario(AbstractUser):
    image_profile = models.ImageField(upload_to='profile_images', blank=True, null=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='usuarios'  # Agrega el related_name para evitar el conflicto
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='usuarios'  # Agrega el related_name para evitar el conflicto
    )
    def __str__(self):
        return self.username

class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    cuerpo = models.TextField()
    imagen_portada = models.ImageField(upload_to='portadas', blank=True, null=True)


class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
