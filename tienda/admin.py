from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Camiseta, Pedido, LineaPedido


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug', 'orden']
    prepopulated_fields = {'slug': ('nombre',)}
    ordering = ['orden', 'nombre']


class LineaPedidoInline(admin.TabularInline):
    model = LineaPedido
    extra = 0
    readonly_fields = ['camiseta', 'talla', 'cantidad']
    can_delete = False


@admin.register(Camiseta)
class CamisetaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'tallas_disponibles', 'activa', 'preview_imagen']
    list_filter = ['activa', 'categoria']
    search_fields = ['nombre', 'descripcion']
    list_editable = [ 'activa']
    prepopulated_fields = {}

    def preview_imagen(self, obj):
        url = obj.imagen_url or (obj.imagen_local.url if obj.imagen_local else '')
        if url:
            return format_html('<img src="{}" style="height:50px; border-radius:4px;" />', url)
        return '—'
    preview_imagen.short_description = 'Imagen'


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre_cliente', 'telefono', 'estado', 'total_articulos', 'fecha_pedido', 'resumen_corto']
    list_filter = ['estado', 'fecha_pedido']
    search_fields = ['nombre_cliente', 'telefono']
    list_editable = ['estado']
    readonly_fields = ['fecha_pedido', 'fecha_actualizacion', 'resumen_completo']
    inlines = [LineaPedidoInline]

    fieldsets = (
        ('Cliente', {
            'fields': ('nombre_cliente', 'telefono', 'notas')
        }),
        ('Estado', {
            'fields': ('estado', 'notas_admin')
        }),
        ('Info', {
            'fields': ('fecha_pedido', 'fecha_actualizacion', 'resumen_completo'),
            'classes': ('collapse',)
        }),
    )

    def resumen_corto(self, obj):
        r = obj.resumen()
        return r[:80] + '...' if len(r) > 80 else r
    resumen_corto.short_description = 'Artículos'

    def resumen_completo(self, obj):
        lineas = obj.lineas.all().select_related('camiseta')
        html = '<table style="width:100%"><tr><th>Camiseta</th><th>Talla</th><th>Cantidad</th></tr>'
        for l in lineas:
            html += f'<tr><td>{l.camiseta.nombre}</td><td>{l.talla}</td><td>{l.cantidad}</td></tr>'
        html += '</table>'
        return format_html(html)
    resumen_completo.short_description = 'Detalle del pedido'


@admin.register(LineaPedido)
class LineaPedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'camiseta', 'talla', 'cantidad']
    list_filter = ['talla']
    search_fields = ['camiseta__nombre', 'pedido__nombre_cliente']
