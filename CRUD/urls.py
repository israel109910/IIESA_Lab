from django.urls import path, include

from .import views 



urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),

    path('', views.main, name='main'),
    path('presion_manometrica/', views.presion_manometrica, name='presion_manometrica'),
    path('presion_manometrica/nuevo', views.crear_presion_manometrica, name='crear_presion_manometrica'),

    path('flujo_vd/', views.flujo_volumetrico_dinamico, name='flujo_volumetrico_dinamico'),
    
    path('presion_manometrica/patrones', views.patrones_presion_manometrica, name='presion_manometrica_patrones'),
    path('presion_manometrica/patrones/detalles/<int:id>', views.detalles_patrones_presion_manometrica, name='detalles_presion_manometrica_patrones'),
   
    path('presion_manometrica/detalles/<int:id>', views.detalles, name='detalles'),
    path('presion_manometrica/detalles/<int:id>/editar', views.form_update, name='editar'),
    path('presion_manometrica/detalles/<int:id>/imprimir', views.imprimir, name='imprimir'),
    path('presion_manometrica/detalles/<int:id>/toma_datos', views.form_toma_datos, name='toma_datos'),
    path('presion_manometrica/detalles/<int:id>/calculos', views.calculos_pm, name='calculos'),


    path('presion_diferencial/', views.presion_diferencial, name='presion_diferencial'),
    path('presion_diferencial/nuevo', views.crear_presion_diferencial, name='crear_presion_diferencial'),
    path('presion_diferencial/detalles/<int:id>', views.detalles_pd, name='detalles_pd'),
    path('presion_diferencial/detalles/<int:id>/editar', views.form_update_pd, name='editar_pd'),
    path('presion_diferencial/detalles/<int:id>/toma_datos', views.form_toma_datos_pd, name='toma_datos_pd'),
    path('presion_diferencial/detalles/<int:id>/calculos', views.calculos_pd, name='calculos_pd'),
    path('presion_diferencial/detalles/<int:id>/imprimir', views.imprimirPresionDiferencial, name='imprimir_pd'),


    path('temperatura/', views.temperatura, name='temperatura'),
    path('temperatura/nuevo', views.crear_temperatura, name='crear_temperatura'),


  
]
