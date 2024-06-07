from django.db import models
from smart_selects.db_fields import ChainedManyToManyField





# Create your models here
class PresionManometrica(models.Model):
    
    unidades_choices=[
        ("kPa", "kPa"),
        ("Lb*f/in2", "Lb*f/in2"),
        ("kg*f/cm2","kg*f/cm2"),
      
        
    ]
    fecha_asignacion = models.DateField()
    responsable = models.CharField(max_length=512)
    #Datos del certificado 
    solicitud_servicio = models.CharField(max_length=100,blank=True, null=True)
    lugar_de_calibracion = models.CharField(max_length=100,blank=True, null=True)
    procedimiento_utilizado = models.CharField(max_length=512,blank=True, null=True)
    magnitud = models.CharField(max_length=100,blank=True, null=True)
    metodo = models.CharField(max_length=100,blank=True, null=True)
    fecha_recepcion = models.DateField(blank=True, null=True)
    fecha_calibracion =models.DateField(blank=True, null=True)
    fecha_emision = models.DateField(blank=True, null=True)
    fecha_entrega_IBC = models.DateField(blank=True, null=True)
    #Datos cliente
    cliente_nombre_razon_social = models.CharField(max_length=100,blank=True, null=True)
    cliente_direccion = models.CharField(max_length=100,blank=True, null=True)
    cliente_telefono = models.CharField(max_length=12,blank=True, null=True)
    cliente_correo = models.CharField(max_length=100, blank=True, null=True)
    #Datos del instrumento
    instrumento_descripcion = models.CharField(max_length=100,blank=True, null=True)
    instrumento_marca = models.CharField(max_length=100,blank=True, null=True)
    instrumento_modelo = models.CharField(max_length=100,blank=True, null=True)
    instrumento_numero_serie = models.CharField(max_length=100,blank=True, null=True)
    instrumento_otra_identificacion = models.CharField(max_length=100,blank=True, null=True)
    instrumento_intervalo_de_medida=models.CharField(max_length=100,blank=True, null=True)
    instrumento_incertidumbre_requerida=models.CharField(max_length=100,blank=True, null=True)
    instrumento_accesorios_incluidos=models.CharField(max_length=100,blank=True, null=True)
    instrumento_condicion_recepcion_del_IBC=models.CharField(max_length=100,blank=True, null=True)
    instrumento_especificaciones_particulares_manejo=models.CharField(max_length=100,blank=True, null=True)
    instrumento_especificaciones_particulares_transporte=models.CharField(max_length=100,blank=True, null=True)
    instrumento_especificaciones_particulares_proteccion=models.CharField(max_length=100,blank=True, null=True)
    instrumento_especificaciones_particulares_almacenaje=models.CharField(max_length=100,blank=True, null=True)
    instrumento_especificaciones_particulares_conservacion=models.CharField(max_length=100,blank=True, null=True)
    instrumento_resolucion=models.CharField(max_length=100,blank=True, null=True)
    C_E=models.CharField(max_length=100,blank=True, null=True)
    coeficiente_termico=models.CharField(max_length=100,blank=True, null=True)
    temperatura_referencia_IBC=models.CharField(max_length=100,blank=True, null=True)
    unidades=models.CharField(max_length=100,blank=True, null=True)
    servicio=models.CharField(max_length=100,blank=True, null=True)
    ubicacion=models.CharField(max_length=100,blank=True, null=True)
    #Datos del patron de medida
    patron_id_presion_manometrica = models.ForeignKey(
        'PatronesPresionManometrica',
        on_delete=models.CASCADE,
        related_name='presion_diferencial_set',  # Example related_name
        blank=True,
        null=True
    )
   #Condiciones Ambientales 
    ambientales_temperatura_inicial = models.FloatField (blank=True, null=True)
    ambientales_temperatura_final = models.FloatField (blank=True, null=True)
    ambientales_presion_barometrica_inicial = models.FloatField(blank = True, null = True)
    ambientales_presion_barometrica_final = models.FloatField(blank = True, null = True)
    ambientales_humedad_relativa_inicial = models.FloatField(blank = True, null = True)
    ambientales_humedad_relativa_final = models.FloatField(blank = True, null = True)
    ambientales_altura_patron = models.FloatField(blank = True, null = True)
    ambientales_altura_IBC = models.FloatField(blank = True, null = True)
    #Datos del Sitio 
    sitio_lat_degrees = models.FloatField(blank = True, null = True)
    sitio_lat_minutes = models.FloatField(blank = True, null = True)
    sitio_lat_seconds = models.FloatField(blank = True, null = True)
    sitio_altura = models.FloatField(blank = True, null = True)
    #Toma de Datos 
   
    unidades_toma_datos=models.CharField(choices=unidades_choices, max_length=20, blank = True, null = True)
    #Desviacion en 0
    desviacion_ciclo1_patron = models.FloatField(blank = True, null = True)
    desviacion_ciclo1_IBC = models.FloatField(blank = True, null = True)
    desviacion_ciclo2_patron = models.FloatField(blank = True, null = True)
    desviacion_ciclo2_IBC = models.FloatField(blank = True, null = True)
    #Toma de Datos valores nominales
    valor_nominal1= models.FloatField(blank = True, null = True)
    valor_nominal2= models.FloatField(blank = True, null = True)
    valor_nominal3= models.FloatField(blank = True, null = True)
    valor_nominal4= models.FloatField(blank = True, null = True)
    valor_nominal5= models.FloatField(blank = True, null = True)
    #valor nominal 1
    valor_nominal1_ciclo1_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal1_ciclo1_lectura_patron_descenso = models.FloatField(blank = True, null = True)
    valor_nominal1_ciclo1_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal1_ciclo1_lectura_IBC_descenso = models.FloatField(blank = True, null = True)
    valor_nominal1_ciclo2_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal1_ciclo2_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
    #valor nominal 2
    valor_nominal2_ciclo1_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal2_ciclo1_lectura_patron_descenso = models.FloatField(blank = True, null = True)
    valor_nominal2_ciclo1_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal2_ciclo1_lectura_IBC_descenso = models.FloatField(blank = True, null = True)
    valor_nominal2_ciclo2_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal2_ciclo2_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
    #valor nominal 3 
    valor_nominal3_ciclo1_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal3_ciclo1_lectura_patron_descenso = models.FloatField(blank = True, null = True)
    valor_nominal3_ciclo1_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal3_ciclo1_lectura_IBC_descenso = models.FloatField(blank = True, null = True)
    valor_nominal3_ciclo2_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal3_ciclo2_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
   #valor nominal 4
    valor_nominal4_ciclo1_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal4_ciclo1_lectura_patron_descenso = models.FloatField(blank = True, null = True)
    valor_nominal4_ciclo1_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal4_ciclo1_lectura_IBC_descenso = models.FloatField(blank = True, null = True)
    valor_nominal4_ciclo2_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal4_ciclo2_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
   #valor nominal 5
    valor_nominal5_ciclo1_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal5_ciclo1_lectura_patron_descenso = models.FloatField(blank = True, null = True)
    valor_nominal5_ciclo1_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal5_ciclo1_lectura_IBC_descenso = models.FloatField(blank = True, null = True)
    valor_nominal5_ciclo2_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal5_ciclo2_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
   
    def __str__(self):
     return f"{self.responsable} {self.fecha_asignacion}"



 
class PatronesPresionDiferencial(models.Model):
    
    patron_identificacion = models.CharField(max_length=10)
    patron_descripcion = models.CharField(max_length=100)
    patron_intervalo_medida = models.CharField(max_length=100)
    patron_marca= models.ForeignKey("PatronesMarcas",related_name='patrones_pd_marca',
                                                      on_delete=models.CASCADE,blank=True, null=True)
    patron_modelo= models.CharField(max_length=50)
    patron_no_serie= models.CharField(max_length=50)
    patron_certificado= models.CharField(max_length=50)
    patron_vigencia= models.DateField()
    patron_trazabilidad= models.CharField(max_length=100)
    patron_reproducibilidad = models.FloatField(blank = True, null = True)
    
    # Curvas de ajuste de los patrones ERROR
    ca_x10 = models.FloatField(blank = True, null = True)
    ca_x9 = models.FloatField(blank = True, null = True)
    ca_x8 = models.FloatField(blank = True, null = True)
    ca_x7 = models.FloatField(blank = True, null = True)
    ca_x6 = models.FloatField(blank = True, null = True)
    ca_x5 = models.FloatField(blank = True, null = True)    
    ca_x4 = models.FloatField(blank = True, null = True)
    ca_x3 = models.FloatField(blank = True, null = True)
    ca_x2 = models.FloatField(blank = True, null = True)
    ca_x = models.FloatField(blank = True, null = True)
    ca_B= models.FloatField(blank = True, null = True)    
    ca_residuales = models.FloatField(blank = True, null = True)  
    
     # Curvas de ajuste de los patrones INCERTIDUMBRE
    ca_i_x10 = models.FloatField(blank = True, null = True)
    ca_i_x9 = models.FloatField(blank = True, null = True)
    ca_i_x8 = models.FloatField(blank = True, null = True)
    ca_i_x7 = models.FloatField(blank = True, null = True)
    ca_i_x6 = models.FloatField(blank = True, null = True)
    ca_i_x5 = models.FloatField(blank = True, null = True)    
    ca_i_x4 = models.FloatField(blank = True, null = True)
    ca_i_x3 = models.FloatField(blank = True, null = True)
    ca_i_x2 = models.FloatField(blank = True, null = True)
    ca_i_x = models.FloatField(blank = True, null = True)
    ca_i_B= models.FloatField(blank = True, null = True)    
    ca_i_residuales = models.FloatField(blank = True, null = True)  
    #DERIVA
    deriva = models.FloatField(blank = True, null = True) 
    #REPRODUCIBILIDAD 
    reproducibilidad = models.FloatField(blank = True, null = True) 
 
 
    

class PatronesPresionManometrica(models.Model):
    
    patron_identificacion = models.CharField(max_length=10)
    patron_descripcion = models.CharField(max_length=100)
    patron_intervalo_medida = models.CharField(max_length=100)
    patron_marca= models.ForeignKey("PatronesMarcas",related_name='patrones_pm_marca',
                                                      on_delete=models.CASCADE,blank=True, null=True)
    patron_modelo= models.CharField(max_length=50)
    patron_no_serie= models.CharField(max_length=50)
    patron_certificado= models.CharField(max_length=50)
    patron_vigencia= models.DateField()
    patron_trazabilidad= models.CharField(max_length=100)
    patron_reproducibilidad = models.FloatField(blank = True, null = True)
    
    # Curvas de ajuste de los patrones ERROR
    ca_x10 = models.FloatField(blank = True, null = True)
    ca_x9 = models.FloatField(blank = True, null = True)
    ca_x8 = models.FloatField(blank = True, null = True)
    ca_x7 = models.FloatField(blank = True, null = True)
    ca_x6 = models.FloatField(blank = True, null = True)
    ca_x5 = models.FloatField(blank = True, null = True)    
    ca_x4 = models.FloatField(blank = True, null = True)
    ca_x3 = models.FloatField(blank = True, null = True)
    ca_x2 = models.FloatField(blank = True, null = True)
    ca_x = models.FloatField(blank = True, null = True)
    ca_B= models.FloatField(blank = True, null = True)    
    ca_residuales = models.FloatField(blank = True, null = True)  
    
     # Curvas de ajuste de los patrones INCERTIDUMBRE
    ca_i_x10 = models.FloatField(blank = True, null = True)
    ca_i_x9 = models.FloatField(blank = True, null = True)
    ca_i_x8 = models.FloatField(blank = True, null = True)
    ca_i_x7 = models.FloatField(blank = True, null = True)
    ca_i_x6 = models.FloatField(blank = True, null = True)
    ca_i_x5 = models.FloatField(blank = True, null = True)    
    ca_i_x4 = models.FloatField(blank = True, null = True)
    ca_i_x3 = models.FloatField(blank = True, null = True)
    ca_i_x2 = models.FloatField(blank = True, null = True)
    ca_i_x = models.FloatField(blank = True, null = True)
    ca_i_B= models.FloatField(blank = True, null = True)    
    ca_i_residuales = models.FloatField(blank = True, null = True)  
    #DERIVA
    deriva = models.FloatField(blank = True, null = True) 
    #REPRODUCIBILIDAD 
    reproducibilidad = models.FloatField(blank = True, null = True) 
    

    
    def __str__(self):
     return f"{self.patron_identificacion}"
    
    
class PatronesMarcas(models.Model):  
    nombre= models.CharField(max_length=50)
    def __str__(self):
     return f"{self.nombre}"
class PresionDiferencial(models.Model):
    unidades_choices=[
        ("kPa", "kPa"),
        ("Lb*f/in2", "Lb*f/in2"),
        ("kg*f/cm2","kg*f/cm2"),
        ("inH2O","inH2O"),
        
        
    ]
    fecha_asignacion = models.DateField()
    responsable = models.CharField(max_length=512)
    #Datos del certificado 
    solicitud_servicio = models.CharField(max_length=100,blank=True, null=True)
    lugar_de_calibracion = models.CharField(max_length=100,blank=True, null=True)
    procedimiento_utilizado = models.CharField(max_length=512,blank=True, null=True)
    magnitud = models.CharField(max_length=100,blank=True, null=True)
    metodo = models.CharField(max_length=100,blank=True, null=True)
    fecha_recepcion = models.DateField(blank=True, null=True)
    fecha_calibracion =models.DateField(blank=True, null=True)
    fecha_emision = models.DateField(blank=True, null=True)
    fecha_entrega_IBC = models.DateField(blank=True, null=True)
    #Datos cliente
    cliente_nombre_razon_social = models.CharField(max_length=100,blank=True, null=True)
    cliente_direccion = models.CharField(max_length=100,blank=True, null=True)
    cliente_telefono = models.CharField(max_length=12,blank=True, null=True)
    cliente_correo = models.CharField(max_length=100, blank=True, null=True)
    #Datos del instrumento
    instrumento_descripcion = models.CharField(max_length=100,blank=True, null=True)
    instrumento_marca = models.CharField(max_length=100,blank=True, null=True)
    instrumento_modelo = models.CharField(max_length=100,blank=True, null=True)
    instrumento_numero_serie = models.CharField(max_length=100,blank=True, null=True)
    instrumento_otra_identificacion = models.CharField(max_length=100,blank=True, null=True)
    instrumento_intervalo_de_medida=models.CharField(max_length=100,blank=True, null=True)
    instrumento_incertidumbre_requerida=models.CharField(max_length=100,blank=True, null=True)
    instrumento_accesorios_incluidos=models.CharField(max_length=100,blank=True, null=True)
    instrumento_condicion_recepcion_del_IBC=models.CharField(max_length=100,blank=True, null=True)
    instrumento_especificaciones_particulares_manejo=models.CharField(max_length=100,blank=True, null=True)
    instrumento_especificaciones_particulares_transporte=models.CharField(max_length=100,blank=True, null=True)
    instrumento_especificaciones_particulares_proteccion=models.CharField(max_length=100,blank=True, null=True)
    instrumento_especificaciones_particulares_almacenaje=models.CharField(max_length=100,blank=True, null=True)
    instrumento_especificaciones_particulares_conservacion=models.CharField(max_length=100,blank=True, null=True)
    instrumento_resolucion=models.CharField(max_length=100,blank=True, null=True)
    C_E=models.CharField(max_length=100,blank=True, null=True)
    coeficiente_termico=models.CharField(max_length=100,blank=True, null=True)
    temperatura_referencia_IBC=models.CharField(max_length=100,blank=True, null=True)
    unidades=models.CharField(max_length=100,blank=True, null=True)
    servicio=models.CharField(max_length=100,blank=True, null=True)
    ubicacion=models.CharField(max_length=100,blank=True, null=True)
    #Datos del patron de medida
    patron_id_presion_manometrica = models.ForeignKey(
        'PatronesPresionManometrica',
        on_delete=models.CASCADE,
        related_name='presion_manometrica_set',  # Example related_name
        blank=True,
        null=True
    )
   #Condiciones Ambientales 
    ambientales_temperatura_inicial = models.FloatField (blank=True, null=True)
    ambientales_temperatura_final = models.FloatField (blank=True, null=True)
    ambientales_presion_barometrica_inicial = models.FloatField(blank = True, null = True)
    ambientales_presion_barometrica_final = models.FloatField(blank = True, null = True)
    ambientales_humedad_relativa_inicial = models.FloatField(blank = True, null = True)
    ambientales_humedad_relativa_final = models.FloatField(blank = True, null = True)
    ambientales_altura_patron = models.FloatField(blank = True, null = True)
    ambientales_altura_IBC = models.FloatField(blank = True, null = True)
    #Datos del Sitio 
    sitio_lat_degrees = models.FloatField(blank = True, null = True)
    sitio_lat_minutes = models.FloatField(blank = True, null = True)
    sitio_lat_seconds = models.FloatField(blank = True, null = True)
    sitio_altura = models.FloatField(blank = True, null = True)
    #Toma de Datos 
   
    unidades_toma_datos=models.CharField(choices=unidades_choices, max_length=20, blank = True, null = True)
    #Desviacion en 0
    desviacion_ciclo1_patron = models.FloatField(blank = True, null = True)
    desviacion_ciclo1_IBC = models.FloatField(blank = True, null = True)
    desviacion_ciclo2_patron = models.FloatField(blank = True, null = True)
    desviacion_ciclo2_IBC = models.FloatField(blank = True, null = True)
    #Toma de Datos valores nominales
    valor_nominal1= models.FloatField(blank = True, null = True)
    valor_nominal2= models.FloatField(blank = True, null = True)
    valor_nominal3= models.FloatField(blank = True, null = True)
    valor_nominal4= models.FloatField(blank = True, null = True)
    valor_nominal5= models.FloatField(blank = True, null = True)
    #valor nominal 1
    valor_nominal1_ciclo1_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal1_ciclo1_lectura_patron_descenso = models.FloatField(blank = True, null = True)
    valor_nominal1_ciclo1_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal1_ciclo1_lectura_IBC_descenso = models.FloatField(blank = True, null = True)
    valor_nominal1_ciclo2_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal1_ciclo2_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
    #valor nominal 2
    valor_nominal2_ciclo1_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal2_ciclo1_lectura_patron_descenso = models.FloatField(blank = True, null = True)
    valor_nominal2_ciclo1_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal2_ciclo1_lectura_IBC_descenso = models.FloatField(blank = True, null = True)
    valor_nominal2_ciclo2_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal2_ciclo2_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
    #valor nominal 3 
    valor_nominal3_ciclo1_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal3_ciclo1_lectura_patron_descenso = models.FloatField(blank = True, null = True)
    valor_nominal3_ciclo1_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal3_ciclo1_lectura_IBC_descenso = models.FloatField(blank = True, null = True)
    valor_nominal3_ciclo2_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal3_ciclo2_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
   #valor nominal 4
    valor_nominal4_ciclo1_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal4_ciclo1_lectura_patron_descenso = models.FloatField(blank = True, null = True)
    valor_nominal4_ciclo1_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal4_ciclo1_lectura_IBC_descenso = models.FloatField(blank = True, null = True)
    valor_nominal4_ciclo2_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal4_ciclo2_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
   #valor nominal 5
    valor_nominal5_ciclo1_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal5_ciclo1_lectura_patron_descenso = models.FloatField(blank = True, null = True)
    valor_nominal5_ciclo1_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal5_ciclo1_lectura_IBC_descenso = models.FloatField(blank = True, null = True)
    valor_nominal5_ciclo2_lectura_patron_ascenso = models.FloatField(blank = True, null = True)
    valor_nominal5_ciclo2_lectura_IBC_ascenso = models.FloatField(blank = True, null = True)
   
    def __str__(self):
     return f"{self.responsable} {self.fecha_asignacion}"


class Temperatura(models.Model):
    fecha_asignacion = models.DateField()
    responsable = models.CharField(max_length=512)
    archivos_asociado = models.FileField(upload_to="uploads/")


#class Densidad(models.Model):
    #folio_asignado = models.AutoField(primary_key=True)
    #fecha_asignacion = models.DateField()
    #responsable = models.CharField(max_length=512)

class FlujoVolumetricoDinamico(models.Model):
    fecha_asignacion = models.DateField()
    responsable = models.CharField(max_length=512)

class PlacaDeOrificio(models.Model):
    fecha_asignacion = models.DateField()
    responsable = models.CharField(max_length=512)

class FlujoMasicoDinamico(models.Model):
    fecha_asignacion = models.DateField()
    responsable = models.CharField(max_length=10)
    


