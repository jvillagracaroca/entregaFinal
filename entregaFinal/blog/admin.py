# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Publicacion, Comentario, Usuario


admin.site.register(Publicacion)
admin.site.register(Comentario)
admin.site.register(Usuario)
