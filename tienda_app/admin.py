from django.contrib import admin

from .models import Inventario, Libro, Orden


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'precio')


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('libro', 'cantidad')
    list_editable = ('cantidad',)


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'libro', 'total', 'usuario', 'direccion_envio', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
