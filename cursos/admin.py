from django.contrib import admin
from .models import Aulas, Cursos, Comentarios, NotasAulas


admin.site.register(Comentarios)
admin.site.register(Cursos)
admin.site.register(Aulas)
admin.site.register(NotasAulas)