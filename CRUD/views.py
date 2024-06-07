from django.http import HttpResponse
from django.template import loader
import math
import pandas as pd
import os

from .models import PresionManometrica
from .models import PresionDiferencial
from .models import Temperatura
from .models import FlujoVolumetricoDinamico
from .models import PatronesPresionManometrica


from .forms import EditarForm
from .forms import TomaDatosManometricoForm
from .forms import PatronesPresionManometricaForm
from .forms import crearPresionManometricaForm
from .forms import crearPresionDiferencialForm
from .forms import EditarFormPresionDiferencial
from .forms import TomaDatosPresionDiferencialForm

from django.shortcuts import render, redirect

from django.http import HttpResponseRedirect





def presion_manometrica(request):
  misfolios = PresionManometrica.objects.all().values().order_by('-id')
  template = loader.get_template('presion_manometrica.html')
  context = {
    'misfolios': misfolios,
  }
  return HttpResponse(template.render(context, request))
def crear_presion_manometrica(request):
  if request.method == 'POST':
        form = crearPresionManometricaForm(request.POST)
        if form.is_valid():
            # create a new `Band` and save it to the db
            folioPresionManometrica = form.save()
         
            return redirect('presion_manometrica')

  else:
        form = crearPresionManometricaForm()

  return render(request,
                'crear_presion_manometrica.html',
                {'form': form})
  
  
def presion_diferencial(request):
  misfolios = PresionDiferencial.objects.all().values()
  template = loader.get_template('presion_diferencial.html')
  context = {
    'misfolios': misfolios,
  }
  return HttpResponse(template.render(context, request))

def crear_presion_diferencial(request):
  if request.method == 'POST':
        form = crearPresionDiferencialForm(request.POST)
        if form.is_valid():
            # create a new `Band` and save it to the db
            folioPresionDiferencial = form.save()
         
            return redirect('presion_diferencial')

  else:
        form = crearPresionDiferencialForm()

  return render(request,
                'crear_presion_diferencial.html',
                {'form': form})
  

def temperatura(request):
  misfolios = Temperatura.objects.all().values()
  template = loader.get_template('temperatura.html')
  context = {
    'misfolios': misfolios,
  }
  return HttpResponse(template.render(context, request))
def flujo_volumetrico_dinamico(request):
  misfolios = FlujoVolumetricoDinamico.objects.all().values()
  template = loader.get_template('flujo_volumetrico_dinamico.html')
  context = {
    'misfolios': misfolios,
  }
  return HttpResponse(template.render(context, request))

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def detalles(request, id):
  mifolio = PresionManometrica.objects.get(id=id)
  template = loader.get_template('detalles.html')
  context = {
    'mifolio': mifolio,
  }
  return HttpResponse(template.render(context, request))

def detalles_pd(request, id):
  mifolio = PresionDiferencial.objects.get(id=id)
  template = loader.get_template('detalles_pd.html')
  context = {
    'mifolio': mifolio,
  }
  return HttpResponse(template.render(context, request))




  

def form_update(request, id):
    folio = PresionManometrica.objects.get(id=id)

    if request.method == 'POST':
        form = EditarForm(request.POST, instance=folio)
        if form.is_valid():
            # update the existing in the database
            form.save()
            # redirect to the detail page 
            return redirect('detalles', folio.id)
    else:
        form = EditarForm(instance=folio)

    return render(request,
                'editar.html',
                {'form': form})
    #form toma datos

def form_update_pd(request, id):
    folio = PresionDiferencial.objects.get(id=id)

    if request.method == 'POST':
        form = EditarFormPresionDiferencial(request.POST, instance=folio)
        if form.is_valid():
            # update the existing in the database
            form.save()
            # redirect to the detail page 
            return redirect('detalles_pd', folio.id)
    else:
        form = EditarFormPresionDiferencial(instance=folio)

    return render(request,
                'editar.html',
                {'form': form})
    #form toma datos


    
    
    
def form_toma_datos(request, id):
    folio = PresionManometrica.objects.get(id=id)

    if request.method == 'POST':
        form = TomaDatosManometricoForm(request.POST, instance=folio)
        if form.is_valid():
            # update the existing in the database
            form.save()
            # redirect to the detail page 
            return redirect('detalles', folio.id)
    else:
        form = TomaDatosManometricoForm(instance=folio)

    return render(request,
                'toma_de_datos.html',
                {'form': form}
    )
    
    
def form_toma_datos_pd(request, id):
    folio = PresionDiferencial.objects.get(id=id)

    if request.method == 'POST':
        form = TomaDatosPresionDiferencialForm(request.POST, instance=folio)
        if form.is_valid():
            # update the existing in the database
            form.save()
            # redirect to the detail page 
            return redirect('detalles_pd', folio.id)
    else:
        form = TomaDatosPresionDiferencialForm(instance=folio)

    return render(request,
                'toma_de_datos_pd.html',
                {'form': form}
    )
    
    
  #imprimir certificado  
def imprimir(request, id):
  

  mifolio = PresionManometrica.objects.get(id=id)
  template = loader.get_template('imprimir.html')
  temperatura_amb_prom = (mifolio.ambientales_temperatura_inicial + mifolio.ambientales_temperatura_final)/2

  humedad_relativa_prom = (mifolio.ambientales_humedad_relativa_inicial+mifolio.ambientales_humedad_relativa_inicial)/2
  presion_barometrica_prom = (mifolio.ambientales_presion_barometrica_inicial + mifolio.ambientales_presion_barometrica_final)/2
  mipatron = PatronesPresionManometrica.objects.select_related('patron_identificacion', 'patron_intervalo_medida','patron_marca',
                                                               'patron_modelo','patron_no_serie','patron_certificado','patron_vigencia','patron_trazabilidad'
                                                               'patron_descripcion')
    
  densidad_aceite=912
  curva_patron = PatronesPresionManometrica.objects.get(id=mifolio.patron_id_presion_manometrica_id)
  diferencia_altura = mifolio.ambientales_altura_patron-mifolio.ambientales_altura_IBC
  latitud = mifolio.sitio_lat_degrees + mifolio.sitio_lat_minutes / 60 + mifolio.sitio_lat_seconds / 3600
  gravedad_local = (9.780318*(1+(0.0053024*(math.sin(math.pi*latitud/180)**2))-0.0000058*(math.sin(2*math.pi*latitud/180)**2))-(0.000003086*mifolio.sitio_altura))
  presion_columna = (912*gravedad_local*(mifolio.ambientales_altura_patron-mifolio.ambientales_altura_IBC))/1000
  temperatura_amb_prom = (mifolio.ambientales_temperatura_inicial + mifolio.ambientales_temperatura_final)/2
    #incertidumbre
    
    
    
  instrumento_resolucion_float = float(mifolio.instrumento_resolucion)
  incertidumbre_resolucion = instrumento_resolucion_float / math.sqrt(12)
  deriva_0_ibc_c1 = float(mifolio.desviacion_ciclo1_IBC)
  deriva_0_ibc_c2 = float(mifolio.desviacion_ciclo2_IBC)
  incertidumbre_deriva_0= (deriva_0_ibc_c1-deriva_0_ibc_c2)/ math.sqrt(3)
  incertidumbre_curva_patron = (curva_patron.ca_i_residuales)/math.sqrt(12)
  incertidumbre_curva_patron_error = (curva_patron.ca_residuales)/math.sqrt(12)
  deriva_patron =float(curva_patron.deriva)
  incertidumbre_deriva_patron = (deriva_patron)/(math.sqrt(12))
  incertidumbre_deriva_0_patron = (mifolio.desviacion_ciclo1_patron - mifolio.desviacion_ciclo2_patron)/math.sqrt(3)
  u_gravedad_local=(gravedad_local*0.0001)/(math.sqrt(3))
  u_densidad=(0.02851*densidad_aceite)
  
  
  
  
  u_diferencia_altura = (diferencia_altura)/(math.sqrt(12))
  u_PCOL = (math.sqrt(
  (gravedad_local * diferencia_altura * u_densidad)**2 +
  (densidad_aceite * diferencia_altura * u_gravedad_local)**2 +
  (gravedad_local * densidad_aceite * u_diferencia_altura)**2
    ))/1000
    #calculos error 
    
    
  unidades_toma_datos=mifolio.unidades_toma_datos
   
  valores_nominales = {
    'desviacion_ciclo1_patron': mifolio.desviacion_ciclo1_patron,
    'desviacion_ciclo1_IBC': mifolio.desviacion_ciclo1_IBC,
    'desviacion_ciclo2_patron': mifolio.desviacion_ciclo2_patron,
    'desviacion_ciclo2_IBC': mifolio.desviacion_ciclo2_IBC,
    
    'valor_nominal1_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal1_ciclo1_lectura_patron_ascenso,
    'valor_nominal1_ciclo1_lectura_patron_descenso': mifolio.valor_nominal1_ciclo1_lectura_patron_descenso,
    'valor_nominal1_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal1_ciclo1_lectura_IBC_ascenso,
    'valor_nominal1_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal1_ciclo1_lectura_IBC_descenso,
    'valor_nominal1_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal1_ciclo2_lectura_patron_ascenso,
    'valor_nominal1_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal1_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal2_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal2_ciclo1_lectura_patron_ascenso,
    'valor_nominal2_ciclo1_lectura_patron_descenso': mifolio.valor_nominal2_ciclo1_lectura_patron_descenso,
    'valor_nominal2_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal2_ciclo1_lectura_IBC_ascenso,
    'valor_nominal2_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal2_ciclo1_lectura_IBC_descenso,
    'valor_nominal2_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal2_ciclo2_lectura_patron_ascenso,
    'valor_nominal2_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal2_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal3_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal3_ciclo1_lectura_patron_ascenso,
    'valor_nominal3_ciclo1_lectura_patron_descenso': mifolio.valor_nominal3_ciclo1_lectura_patron_descenso,
    'valor_nominal3_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal3_ciclo1_lectura_IBC_ascenso,
    'valor_nominal3_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal3_ciclo1_lectura_IBC_descenso,
    'valor_nominal3_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal3_ciclo2_lectura_patron_ascenso,
    'valor_nominal3_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal3_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal4_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal4_ciclo1_lectura_patron_ascenso,
    'valor_nominal4_ciclo1_lectura_patron_descenso': mifolio.valor_nominal4_ciclo1_lectura_patron_descenso,
    'valor_nominal4_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal4_ciclo1_lectura_IBC_ascenso,
    'valor_nominal4_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal4_ciclo1_lectura_IBC_descenso,
    'valor_nominal4_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal4_ciclo2_lectura_patron_ascenso,
    'valor_nominal4_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal4_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal5_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal5_ciclo1_lectura_patron_ascenso,
    'valor_nominal5_ciclo1_lectura_patron_descenso': mifolio.valor_nominal5_ciclo1_lectura_patron_descenso,
    'valor_nominal5_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal5_ciclo1_lectura_IBC_ascenso,
    'valor_nominal5_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal5_ciclo1_lectura_IBC_descenso,
    'valor_nominal5_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal5_ciclo2_lectura_patron_ascenso,
    'valor_nominal5_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal5_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal1_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal1_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal1_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal1_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal1_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal1_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal1_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal1_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal1_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal1_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal1_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal1_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,
    
    'valor_nominal2_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal2_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal2_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal2_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal2_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal2_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal2_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal2_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal2_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal2_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal2_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal2_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,

    'valor_nominal3_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal3_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal3_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal3_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal3_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal3_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal3_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal3_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal3_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal3_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal3_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal3_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,

    'valor_nominal4_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal4_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal4_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal4_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal4_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal4_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal4_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal4_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal4_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal4_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal4_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal4_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,

    'valor_nominal5_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal5_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal5_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal5_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal5_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal5_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal5_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal5_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal5_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal5_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal5_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal5_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,

}

# Diccionario para almacenar los resultados
  resultados = {}

# Convertir los valores nominales según la unidad de medida
  for key, valor_nominal in valores_nominales.items():
      if unidades_toma_datos == "Lb*f/in2":
        resultado = round(valor_nominal * 6.89476, 8)
      elif unidades_toma_datos == "kg*f/cm2":
        resultado = round(valor_nominal * 98.0665, 8)
      else:
        resultado = valor_nominal  # Mantener el valor nominal si son kPa

      resultados[key] = resultado

# Crear un diccionario para almacenar los valores promedio por valor nominal
  promedios_por_valor_nominal = {}

# Iterar sobre el diccionario de resultados
  for key, value in resultados.items():
    # Verificar si la medida tiene "IBC" en el nombre y "_ajuste_a_0" al final
       if "IBC" in key and "_ajuste_a_0" in key:
        # Obtener el valor nominal
        valor_nominal = key.split('_')[1]
        # Verificar si el valor nominal ya está en el diccionario de promedios
        if valor_nominal not in promedios_por_valor_nominal:
            # Si no está, inicializar una lista con el valor actual
            promedios_por_valor_nominal[valor_nominal] = [value]
        else:
            # Si está, agregar el valor a la lista existente
            promedios_por_valor_nominal[valor_nominal].append(value)

# Calcular el promedio para cada valor nominal y almacenarlo en un nuevo diccionario
  promedios_finales = {}
  for valor_nominal, medidas in promedios_por_valor_nominal.items():
      promedio = sum(medidas) / len(medidas)
      promedios_finales[valor_nominal] = promedio

  resultados_con_presion_columna = {}

# Itera sobre los elementos del diccionario original
  for key, value in resultados.items():
  # Resta presion_columna al valor actual y almacena el resultado en el nuevo diccionario
      resultados_con_presion_columna[key] = value - presion_columna

# Crea un nuevo diccionario para almacenar los errores del patrón
  error_patron = {}

# Itera sobre cada par clave-valor en el diccionario `resultados_con_presion_columna`
  for key, number in resultados_con_presion_columna.items():
    # Calcula la expresión polinómica usando los coeficientes de la curva del patrón
      error_patron[key] = (((number**10) * curva_patron.ca_x10) + ((number**9) * curva_patron.ca_x9) + ((number**8) * curva_patron.ca_x8) + ((number**7) * curva_patron.ca_x7) +
                      ((number**6) * curva_patron.ca_x6) + ((number**5) * curva_patron.ca_x5) + ((number**4) * curva_patron.ca_x4) + ((number**3) * curva_patron.ca_x3) +
                      ((number**2) * curva_patron.ca_x2) + (number * curva_patron.ca_x) + curva_patron.ca_B)
    
  correccion_temp= {}
    
  for key, number in resultados.items():
   # Convertir las cadenas a números flotantes si es necesario
        temperatura_amb_prom = float(temperatura_amb_prom)
        mifolio.coeficiente_termico = float(mifolio.coeficiente_termico)
        mifolio.temperatura_referencia_IBC = float(mifolio.temperatura_referencia_IBC)

# Realizar la operación corregida
        correccion_temp[key] = number * (1 + (mifolio.coeficiente_termico * (temperatura_amb_prom - mifolio.temperatura_referencia_IBC)))



# Crear un diccionario para almacenar los valores promedio por valor nominal
  promedios_lcp = {}

# Iterar sobre el diccionario de resultados
  for key, value in resultados_con_presion_columna.items():
     if "patron" in key and "_ajuste_a_0" in key:
        # Obtener el valor nominal
      valor_nominal = key.split('_')[1]
        # Verificar si el valor nominal ya está en el diccionario de promedios
      if valor_nominal not in promedios_lcp:
            # Si no está, inicializar una lista con el valor actual
            promedios_lcp[valor_nominal] = [value]
      else:
            # Si está, agregar el valor a la lista existente
          promedios_lcp[valor_nominal].append(value)

# Calcular el promedio para cada valor nominal y almacenarlo en un nuevo diccionario
  promedios_finales_lcp = {}
  for valor_nominal, medidas in promedios_lcp.items():
    promedio = sum(medidas) / len(medidas)
    promedios_finales_lcp[valor_nominal] = promedio
      
      
      # Crear un diccionario para almacenar los valores promedio por valor nominal
  promedios_lcetibc = {}

# Iterar sobre el diccionario de resultados
  for key, value in correccion_temp.items():
     if "IBC" in key and "_ajuste_a_0" in key:
        # Obtener el valor nominal
      valor_nominal = key.split('_')[1]
        # Verificar si el valor nominal ya está en el diccionario de promedios
      if valor_nominal not in promedios_lcetibc:
            # Si no está, inicializar una lista con el valor actual
          promedios_lcetibc[valor_nominal] = [value]
      else:
            # Si está, agregar el valor a la lista existente
          promedios_lcetibc[valor_nominal].append(value)

# Calcular el promedio para cada valor nominal y almacenarlo en un nuevo diccionario
  promedios_finales_lcetibc = {}
  for valor_nominal, medidas in promedios_lcetibc.items():
    promedio = sum(medidas) / len(medidas)
    promedios_finales_lcetibc[valor_nominal] = promedio
      
    promedios_ep = {}

# Iterar sobre el diccionario de resultados
  for key, value in error_patron.items():
     if "patron" in key and "_ajuste_a_0" in key:
        # Obtener el valor nominal
      valor_nominal = key.split('_')[1]
        # Verificar si el valor nominal ya está en el diccionario de promedios
      if valor_nominal not in promedios_ep:
            # Si no está, inicializar una lista con el valor actual
          promedios_ep[valor_nominal] = [value]
      else:
            # Si está, agregar el valor a la lista existente
          promedios_ep[valor_nominal].append(value)

# Calcular el promedio para cada valor nominal y almacenarlo en un nuevo diccionario
  promedios_finales_ep = {}
  for valor_nominal, medidas in promedios_ep.items():
    promedio = sum(medidas) / len(medidas)
    promedios_finales_ep[valor_nominal] = promedio
      
      
  E_values = {}
  for i in range(1, 6):  # Suponiendo que tienes 5 valores nominales
     nominal_key = f'nominal{i}'
     lcp = promedios_finales_lcp.get(nominal_key)
     lcetibc = promedios_finales_lcetibc.get(nominal_key)
     ep = promedios_finales_ep.get(nominal_key)
     E = lcetibc - (lcp - ep)
     E_values[nominal_key] = E
 # Crear un nuevo diccionario para almacenar los resultados de las restas
  histeresis_IBC = {}

# Iterar sobre el diccionario de valores nominales
  for key, value in correccion_temp.items():
    # Verificar si la clave contiene "IBC_ascenso" y "ciclo1"
     if "IBC_ascenso" in key and "ciclo1" in key:
        # Crear la clave correspondiente para "descenso"
         descenso_key = key.replace("ascenso", "descenso")
         if descenso_key in correccion_temp:
          # Realizar la resta y almacenar el resultado en el diccionario
          histeresis_IBC[key] = value - correccion_temp[descenso_key]
  histeresis_patron = {}

# Iterar sobre el diccionario de valores nominales
  for key, value in resultados_con_presion_columna.items():
    # Verificar si la clave contiene "IBC_ascenso" y "ciclo1"
     if "patron_ascenso" in key and "ciclo1" in key:
        # Crear la clave correspondiente para "descenso"
         descenso_key = key.replace("ascenso", "descenso")
         if descenso_key in resultados_con_presion_columna:
            # Realizar la resta y almacenar el resultado en el diccionario
          histeresis_patron[key] = value - resultados_con_presion_columna[descenso_key]
    
  incertidumbre_histererisis_ibc = {}
    
  for key, value in histeresis_IBC.items():
    incertidumbre_histererisis_ibc[key] = value/math.sqrt(12)
      

  incertidumbre_repetibilidad_IBC = {}
  for valor_nominal in range(1, 6):
      valores = [v for k, v in correccion_temp.items() if f'valor_nominal{valor_nominal}' in k and 'IBC' in k and '_ajuste_a_0' in k]
      suma = sum(valores)
      media = suma / len(valores)
      suma_cuadrados = sum((valor - media) ** 2 for valor in valores)
      desviacion = (math.sqrt(suma_cuadrados / (len(valores) - 1))) / math.sqrt(3)

      incertidumbre_repetibilidad_IBC[valor_nominal] = desviacion
  incertidumbre_cal_patron = {}

# Itera sobre cada par clave-valor en el diccionario `resultados_con_presion_columna`
  for key, number in promedios_finales_lcp.items():
  # Calcula la expresión polinómica usando los coeficientes de la curva del patrón
      incertidumbre_cal_patron[key] = ((((number**10) * curva_patron.ca_i_x10) + ((number**9) * curva_patron.ca_i_x9) + ((number**8) * curva_patron.ca_i_x8) + ((number**7) * curva_patron.ca_i_x7) +
                      ((number**6) * curva_patron.ca_i_x6) + ((number**5) * curva_patron.ca_i_x5) + ((number**4) * curva_patron.ca_i_x4) + ((number**3) * curva_patron.ca_i_x3) +
                      ((number**2) * curva_patron.ca_i_x2) + (number * curva_patron.ca_i_x) + curva_patron.ca_i_B))/2
  incertidumbre_repetibilidad_patron = {}

  for valor_nominal in range(1, 6):
    # Filtrar solo los valores correspondientes al valor nominal actual, lectura del patrón y ajuste a cero
     valores = [v for k, v in resultados_con_presion_columna.items() if f'valor_nominal{valor_nominal}' in k and 'lectura_patron' in k and 'ajuste_a_0' in k]
    
    # Calcular la media
     suma = round(sum(valores),6)
     media = round(suma / len(valores), 6)
    
    # Calcular la desviación estándar
     suma_cuadrados = round(sum((valor - media) ** 2 for valor in valores),6)
     desviacion = (math.sqrt(suma_cuadrados / (len(valores) - 1))) / math.sqrt(3)

     incertidumbre_repetibilidad_patron[valor_nominal] = desviacion
      
  max_key = max(histeresis_patron, key=histeresis_patron.get)
  max_value_hp = histeresis_patron[max_key]
 
  incertidumbre_hp =  (max_value_hp)/math.sqrt(12)
    
  u_total={
      'u_1': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[1]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal1']**2 +
    incertidumbre_repetibilidad_IBC[1]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal1_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
),
        'u_2': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[2]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal2']**2 +
    incertidumbre_repetibilidad_IBC[2]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal2_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
),
          'u_3': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[3]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal3']**2 +
    incertidumbre_repetibilidad_IBC[3]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal3_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
),  'u_4': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[4]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal4']**2 +
    incertidumbre_repetibilidad_IBC[4]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal4_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
),  'u_5': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[5]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal5']**2 +
    incertidumbre_repetibilidad_IBC[5]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal5_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
)
    }
    
  u_total_duplicado = {k: v * 2 for k, v in u_total.items()}
      
  context = {
      
        'u_total_duplicado' : u_total_duplicado,
        'u_total' : u_total,
        'incertidumbre_hp' : incertidumbre_hp,
        'max_value_hp' : max_value_hp,
        'incertidumbre_repetibilidad_patron' : incertidumbre_repetibilidad_patron,
        'incertidumbre_cal_patron' : incertidumbre_cal_patron,
        'incertidumbre_repetibilidad_IBC' : incertidumbre_repetibilidad_IBC,
        'incertidumbre_histererisis_ibc':incertidumbre_histererisis_ibc,
        'histeresis_patron' : histeresis_patron,
        'histeresis_IBC' : histeresis_IBC,
        'E_values':E_values,
        'promedios_finales_ep':promedios_finales_ep,
        'promedios_finales_lcetibc':promedios_finales_lcetibc,
        'correccion_temp' : correccion_temp,
        'error_patron' : error_patron,
        'resultados_con_presion_columna':resultados_con_presion_columna,
        'promedios_finales':promedios_finales,
        'resultados': resultados,
        'presion_columna' : presion_columna,
        'gravedad_local': gravedad_local,
        'latitud' : latitud,
        'mifolio': mifolio,
        'temperatura_amb_prom':temperatura_amb_prom,
        'promedios_finales_lcp': promedios_finales_lcp,
        
        'curva' : curva_patron,
        'ca_x10': curva_patron.ca_x10,
        'ca_x9': curva_patron.ca_x9,
        'ca_x8': curva_patron.ca_x8,
        'ca_x7': curva_patron.ca_x7,
        'ca_x6': curva_patron.ca_x6,
        'ca_x5': curva_patron.ca_x5,
        'ca_x4': curva_patron.ca_x4,
        'ca_x3': curva_patron.ca_x3,
        'ca_x2': curva_patron.ca_x2,
        'ca_x': curva_patron.ca_x,
        'ca_B': curva_patron.ca_B,
        
        'ca_i_x10': curva_patron.ca_i_x10,
        'ca_i_x9': curva_patron.ca_i_x9,
        'ca_i_x8': curva_patron.ca_i_x8,
        'ca_i_x7': curva_patron.ca_i_x7,
        'ca_i_x6': curva_patron.ca_i_x6,
        'ca_i_x5': curva_patron.ca_i_x5,
        'ca_i_x4': curva_patron.ca_i_x4,
        'ca_i_x3': curva_patron.ca_i_x3,
        'ca_i_x2': curva_patron.ca_i_x2,
        'ca_i_x': curva_patron.ca_i_x,
        'ca_i_B': curva_patron.ca_i_B,
        'incertidumbre_curva_patron' : incertidumbre_curva_patron,
        'incertidumbre_curva_patron_error' : incertidumbre_curva_patron_error,
        'incertidumbre_resolucion' : incertidumbre_resolucion,
        'incertidumbre_deriva_0': incertidumbre_deriva_0,
        'incertidumbre_deriva_patron' : incertidumbre_deriva_patron,
        'incertidumbre_deriva_0_patron' : incertidumbre_deriva_0_patron,
        'u_gravedad_local' : u_gravedad_local,
        'u_densidad' : u_densidad,
        'u_diferencia_altura' : u_diferencia_altura,
        'u_PCOL':u_PCOL,
        'u_reproducibilidad': curva_patron.reproducibilidad,
        

    }
  
  return HttpResponse(template.render(context, request))
  

def imprimirPresionDiferencial(request, id):
  
    template = loader.get_template('imprimir_pd.html')

    mifolio = PresionDiferencial.objects.get(id=id)
    
    
    temperatura_amb_prom = (mifolio.ambientales_temperatura_inicial + mifolio.ambientales_temperatura_final)/2

    
    humedad_relativa = (mifolio.ambientales_humedad_relativa_inicial + mifolio.ambientales_humedad_relativa_final)/2
    EC_p = (
        (0.000012378847 * ((temperatura_amb_prom +273.15)** 2)) +
        (-0.019121316 * (temperatura_amb_prom+273.15)) +
        33.93711047 +
        (-6343.1645 / (temperatura_amb_prom + 273.15))
    )
    presion_vapor_s= 1 * math.exp(
        (0.000012378847 * ((temperatura_amb_prom +273.15)** 2)) +
        (-0.019121316 * (temperatura_amb_prom+273.15)) +
        33.93711047 +
        (-6343.1645 / (temperatura_amb_prom + 273.15))
    )
    
    factor_fugacidad = 1.00062 + (0.0000000314 * mifolio.ambientales_presion_barometrica_inicial) + (0.00000056 * (temperatura_amb_prom ** 2))
    
    factor_molar_vapor = (factor_fugacidad*(humedad_relativa/100))*(presion_vapor_s/mifolio.ambientales_presion_barometrica_inicial)
    
    factor_compresibilidad = 1 - (mifolio.ambientales_presion_barometrica_inicial / (temperatura_amb_prom + 273.15)) * (
            (((0.00000158123 + (-0.000000029331 * temperatura_amb_prom) + (0.00000000011043 * temperatura_amb_prom**2)) +
              ((0.000005707 + (-0.00000002051 * temperatura_amb_prom))) * factor_molar_vapor) +
            (0.00019898 + (-0.000002376 * 0.00000158123) * factor_molar_vapor**2) +
            ((mifolio.ambientales_presion_barometrica_inicial**2) / ((temperatura_amb_prom + 273.15)**2)) * (
                0.0000000000183 + 0.00000000765 * factor_molar_vapor**2
            )
    )
    )

    
    pma= 0.02896351244*mifolio.ambientales_presion_barometrica_inicial
    zrt = factor_compresibilidad*(8.31451)*(temperatura_amb_prom + 273.15)
    mv_ma= 0.018015/0.02896351244
    L=pma/zrt
    
    densidad_aire= L*(1-(factor_molar_vapor*(1-mv_ma)))

    curva_patron = PatronesPresionManometrica.objects.get(id=mifolio.patron_id_presion_manometrica_id)
    diferencia_altura = mifolio.ambientales_altura_patron-mifolio.ambientales_altura_IBC
    latitud = mifolio.sitio_lat_degrees + mifolio.sitio_lat_minutes / 60 + mifolio.sitio_lat_seconds / 3600
    gravedad_local = (9.780318*(1+(0.0053024*(math.sin(math.pi*latitud/180)**2))-0.0000058*(math.sin(2*math.pi*latitud/180)**2))-(0.000003086*mifolio.sitio_altura))
    presion_columna = (densidad_aire*gravedad_local*(mifolio.ambientales_altura_patron-mifolio.ambientales_altura_IBC))/1000
    #incertidumbre
    instrumento_resolucion_float = float(mifolio.instrumento_resolucion)
    unidades_toma_datos = mifolio.unidades_toma_datos
    
    # Condicional para convertir el valor nominal
    if unidades_toma_datos == "Lb*f/in2":
        resultado = float(instrumento_resolucion_float * 6.89476)
    elif unidades_toma_datos == "kg*f/cm2":
        resultado = float(instrumento_resolucion_float * 98.0665)
    elif unidades_toma_datos == "inH2O":
        resultado = float(instrumento_resolucion_float * 0.2490889)
    else:
        resultado = instrumento_resolucion_float

    # Calcular la incertidumbre de resolución
    instrumento_resolucion_float = resultado
    
    
    incertidumbre_resolucion = instrumento_resolucion_float / math.sqrt(12)
    
    
    deriva_0_ibc_c1 = float(mifolio.desviacion_ciclo1_IBC)
    deriva_0_ibc_c2 = float(mifolio.desviacion_ciclo2_IBC)
    incertidumbre_deriva_0= (deriva_0_ibc_c1-deriva_0_ibc_c2)/ math.sqrt(3)
    incertidumbre_curva_patron = (curva_patron.ca_i_residuales)/math.sqrt(12)
    incertidumbre_curva_patron_error = (curva_patron.ca_residuales)/math.sqrt(12)
    deriva_patron =float(curva_patron.deriva)
    incertidumbre_deriva_patron = (deriva_patron)/(math.sqrt(12))
    incertidumbre_deriva_0_patron = (mifolio.desviacion_ciclo1_patron - mifolio.desviacion_ciclo2_patron)/math.sqrt(3)
  
    u_gravedad_local=(gravedad_local*0.0001)/(math.sqrt(3))
 
    dPsv_dt =  math.exp(EC_p) * (
    (2 * 0.000012378847 * (temperatura_amb_prom + 273.15)) +
    -0.019121316 -
    (-6343.1645 / ((temperatura_amb_prom + 273.15) ** 2))  # Corrigiendo la temperatura en el denominador
)
    
    df_dp = 0.0000000314
    df_dt = 2*(0.00000056)*temperatura_amb_prom
    dXv_dh =(presion_vapor_s)*(factor_fugacidad)/(mifolio.ambientales_presion_barometrica_inicial)
    dXv_df = 50/100*presion_vapor_s/mifolio.ambientales_presion_barometrica_inicial
    dxv_dp = -50/100*factor_fugacidad*presion_vapor_s/mifolio.ambientales_presion_barometrica_inicial**2
    dXv_dPsv = 50/100*factor_fugacidad/mifolio.ambientales_presion_barometrica_inicial
    dZ_dp = (-1/(temperatura_amb_prom+273.15))*(((0.00000158123+(-0.000000029331*temperatura_amb_prom)+(0.00000000011043*temperatura_amb_prom**2))+((0.000005707+(-0.00000002051*0.00000158123)))*factor_molar_vapor)+(0.00019898+(-0.000002376*temperatura_amb_prom))*factor_molar_vapor**2)+(2*mifolio.ambientales_presion_barometrica_inicial/(temperatura_amb_prom+273.15)**2)*(0.0000000000183+-0.00000000765*factor_molar_vapor**2)
    zrt_2=factor_compresibilidad*(8.31451)*((temperatura_amb_prom + 273.15)**2)
    zr_2t=factor_compresibilidad*((8.31451)**2)*(temperatura_amb_prom + 273.15)   
    dZ_dT= (mifolio.ambientales_presion_barometrica_inicial/(temperatura_amb_prom+273.15)**2)*(((0.00000158123+(-0.000000029331*temperatura_amb_prom)+(0.00000000011043*temperatura_amb_prom**2))+((0.000005707+(-0.00000002051*temperatura_amb_prom)))*factor_molar_vapor)+(0.00019898+(-0.000002376*temperatura_amb_prom))*factor_molar_vapor**2)-(2*mifolio.ambientales_presion_barometrica_final**2/(temperatura_amb_prom+273.15)**3)*(0.0000000000183+-0.00000000765*factor_molar_vapor**2)
    dZ_dt = (-mifolio.ambientales_presion_barometrica_inicial/(temperatura_amb_prom+273.15))*(-0.000000029331 + 2*0.00000000011043*temperatura_amb_prom+(-0.00000002051)*factor_molar_vapor+(-0.000002376)*factor_molar_vapor**2)
    dZ_dXv = (-mifolio.ambientales_presion_barometrica_inicial/(temperatura_amb_prom+273.15))*(0.000005707+(-0.00000002051)*0.00000158123+2*0.00019898*factor_molar_vapor+2*-0.000002376*temperatura_amb_prom*factor_molar_vapor)+(2*mifolio.ambientales_presion_barometrica_final**2*-0.00000000765*factor_molar_vapor/(temperatura_amb_prom+273.15)**2) 
    dp_dp =(0.02896351244/zrt)*(1-factor_molar_vapor*(1- mv_ma))
    dp_dz = (-pma/zrt)*(1-factor_molar_vapor*((1-mv_ma)))
    dp_dt =(-pma/zrt_2)*(1-factor_molar_vapor*(1-mv_ma))
    dp_dXV= (-pma/zrt)*(1-mv_ma)
    dp_dR =(-pma/zr_2t)*(1-factor_molar_vapor*(1-mv_ma))
    
    coeficiente_s_presion =(dp_dp+(dp_dz*dZ_dp)+(dp_dz*dZ_dXv*dXv_df*df_dp)+(dp_dz*dZ_dXv*dxv_dp)+(dp_dXV*dXv_df*df_dp)+(dp_dXV*dxv_dp))
    coeficiente_s_temperatura=(dp_dz*dZ_dT*1)+(dp_dz*dZ_dt)+(dp_dz*dZ_dXv*dXv_df*df_dt)+(dp_dz*dZ_dXv*dXv_dPsv*dPsv_dt*1)+(dp_dt*1)+(dp_dXV*dXv_df*df_dt)+(dp_dXV*dXv_dPsv*dPsv_dt*1)
    coeficiente_s_humedad_rel = (dp_dz*dZ_dXv*dXv_dh)+(dp_dXV*dXv_dh)
    coeficiente_s_constante = dp_dR
    incertidumbre_densidad_sum_cuadrados=(12.86*coeficiente_s_presion)**2+(0.455*coeficiente_s_temperatura)**2+(0.015*coeficiente_s_humedad_rel)**2+(0.0000084*coeficiente_s_constante)**2+(0.000095*1)**2
    incertidumbre_densidad_aire =2*( math.sqrt(incertidumbre_densidad_sum_cuadrados))

    u_diferencia_altura = (0.005)/(math.sqrt(12)) #norma tal parece equipo medicion nivel
    u_PCOL = (math.sqrt(
    (gravedad_local * diferencia_altura * incertidumbre_densidad_aire)**2 +
    (densidad_aire * diferencia_altura * u_gravedad_local)**2 +
    (gravedad_local * densidad_aire * u_diferencia_altura)**2
    ))/1000
    #calculos error 
    
    unidades_toma_datos=mifolio.unidades_toma_datos
   
    valores_nominales = {
    'desviacion_ciclo1_patron': mifolio.desviacion_ciclo1_patron,
    'desviacion_ciclo1_IBC': mifolio.desviacion_ciclo1_IBC,
    'desviacion_ciclo2_patron': mifolio.desviacion_ciclo2_patron,
    'desviacion_ciclo2_IBC': mifolio.desviacion_ciclo2_IBC,
    
    'valor_nominal1_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal1_ciclo1_lectura_patron_ascenso,
    'valor_nominal1_ciclo1_lectura_patron_descenso': mifolio.valor_nominal1_ciclo1_lectura_patron_descenso,
    'valor_nominal1_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal1_ciclo1_lectura_IBC_ascenso,
    'valor_nominal1_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal1_ciclo1_lectura_IBC_descenso,
    'valor_nominal1_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal1_ciclo2_lectura_patron_ascenso,
    'valor_nominal1_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal1_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal2_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal2_ciclo1_lectura_patron_ascenso,
    'valor_nominal2_ciclo1_lectura_patron_descenso': mifolio.valor_nominal2_ciclo1_lectura_patron_descenso,
    'valor_nominal2_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal2_ciclo1_lectura_IBC_ascenso,
    'valor_nominal2_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal2_ciclo1_lectura_IBC_descenso,
    'valor_nominal2_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal2_ciclo2_lectura_patron_ascenso,
    'valor_nominal2_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal2_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal3_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal3_ciclo1_lectura_patron_ascenso,
    'valor_nominal3_ciclo1_lectura_patron_descenso': mifolio.valor_nominal3_ciclo1_lectura_patron_descenso,
    'valor_nominal3_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal3_ciclo1_lectura_IBC_ascenso,
    'valor_nominal3_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal3_ciclo1_lectura_IBC_descenso,
    'valor_nominal3_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal3_ciclo2_lectura_patron_ascenso,
    'valor_nominal3_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal3_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal4_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal4_ciclo1_lectura_patron_ascenso,
    'valor_nominal4_ciclo1_lectura_patron_descenso': mifolio.valor_nominal4_ciclo1_lectura_patron_descenso,
    'valor_nominal4_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal4_ciclo1_lectura_IBC_ascenso,
    'valor_nominal4_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal4_ciclo1_lectura_IBC_descenso,
    'valor_nominal4_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal4_ciclo2_lectura_patron_ascenso,
    'valor_nominal4_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal4_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal5_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal5_ciclo1_lectura_patron_ascenso,
    'valor_nominal5_ciclo1_lectura_patron_descenso': mifolio.valor_nominal5_ciclo1_lectura_patron_descenso,
    'valor_nominal5_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal5_ciclo1_lectura_IBC_ascenso,
    'valor_nominal5_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal5_ciclo1_lectura_IBC_descenso,
    'valor_nominal5_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal5_ciclo2_lectura_patron_ascenso,
    'valor_nominal5_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal5_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal1_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal1_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal1_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal1_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal1_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal1_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal1_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal1_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal1_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal1_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal1_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal1_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,
    
    'valor_nominal2_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal2_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal2_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal2_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal2_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal2_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal2_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal2_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal2_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal2_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal2_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal2_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,

    'valor_nominal3_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal3_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal3_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal3_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal3_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal3_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal3_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal3_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal3_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal3_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal3_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal3_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,

    'valor_nominal4_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal4_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal4_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal4_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal4_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal4_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal4_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal4_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal4_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal4_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal4_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal4_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,

    'valor_nominal5_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal5_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal5_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal5_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal5_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal5_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal5_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal5_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal5_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal5_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal5_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal5_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,

}

# Diccionario para almacenar los resultados
    resultados = {}

# Convertir los valores nominales según la unidad de medida
    for key, valor_nominal in valores_nominales.items():
      if unidades_toma_datos == "Lb*f/in2":
        resultado = round(valor_nominal * 6.89476, 8)
      elif unidades_toma_datos == "kg*f/cm2":
        resultado = round(valor_nominal * 98.0665, 8)
      elif unidades_toma_datos == "inH2O":
        resultado = round(valor_nominal * 0.2490889, 8)
      else:
        resultado = valor_nominal
      resultados[key] = resultado

# Crear un diccionario para almacenar los valores promedio por valor nominal
    promedios_por_valor_nominal = {}

# Iterar sobre el diccionario de resultados
    for key, value in resultados.items():
    # Verificar si la medida tiene "IBC" en el nombre y "_ajuste_a_0" al final
       if "IBC" in key and "_ajuste_a_0" in key:
        # Obtener el valor nominal
        valor_nominal = key.split('_')[1]
        # Verificar si el valor nominal ya está en el diccionario de promedios
        if valor_nominal not in promedios_por_valor_nominal:
            # Si no está, inicializar una lista con el valor actual
            promedios_por_valor_nominal[valor_nominal] = [value]
        else:
            # Si está, agregar el valor a la lista existente
            promedios_por_valor_nominal[valor_nominal].append(value)

# Calcular el promedio para cada valor nominal y almacenarlo en un nuevo diccionario
    promedios_finales = {}
    for valor_nominal, medidas in promedios_por_valor_nominal.items():
      promedio = sum(medidas) / len(medidas)
      promedios_finales[valor_nominal] = promedio

    resultados_con_presion_columna = {}

# Itera sobre los elementos del diccionario original
    for key, value in resultados.items():
    # Resta presion_columna al valor actual y almacena el resultado en el nuevo diccionario
        resultados_con_presion_columna[key] = value - presion_columna


#resultados de kpa inH2O para el error patron 
    resultados_inh2o_presion_colum = {}
    for key, value in resultados_con_presion_columna.items():
    # Resta presion_columna al valor actual y almacena el resultado en el nuevo diccionario
        resultados_inh2o_presion_colum[key] = value / 0.2490889








    error_patron = {}

# Itera sobre cada par clave-valor en el diccionario `resultados_con_presion_columna`
    for key, number in resultados_inh2o_presion_colum.items():
    # Calcula la expresión polinómica usando los coeficientes de la curva del patrón
        error_patron[key] = ((((number**10) * curva_patron.ca_x10) + ((number**9) * curva_patron.ca_x9) + ((number**8) * curva_patron.ca_x8) + ((number**7) * curva_patron.ca_x7) +
                      ((number**6) * curva_patron.ca_x6) + ((number**5) * curva_patron.ca_x5) + ((number**4) * curva_patron.ca_x4) + ((number**3) * curva_patron.ca_x3) +
                      ((number**2) * curva_patron.ca_x2) + (number * curva_patron.ca_x) + curva_patron.ca_B))*0.2490889
    
    correccion_temp= {}
    
    for key, number in resultados.items():
   # Convertir las cadenas a números flotantes si es necesario
        temperatura_amb_prom = float(temperatura_amb_prom)
        mifolio.coeficiente_termico = float(mifolio.coeficiente_termico)
        mifolio.temperatura_referencia_IBC = float(mifolio.temperatura_referencia_IBC)

# Realizar la operación corregida
        correccion_temp[key] = number * (1 + (mifolio.coeficiente_termico * (temperatura_amb_prom - mifolio.temperatura_referencia_IBC)))



# Crear un diccionario para almacenar los valores promedio por valor nominal
    promedios_lcp = {}

# Iterar sobre el diccionario de resultados
    for key, value in resultados_con_presion_columna.items():
       if "patron" in key and "_ajuste_a_0" in key:
        # Obtener el valor nominal
        valor_nominal = key.split('_')[1]
        # Verificar si el valor nominal ya está en el diccionario de promedios
        if valor_nominal not in promedios_lcp:
            # Si no está, inicializar una lista con el valor actual
            promedios_lcp[valor_nominal] = [value]
        else:
            # Si está, agregar el valor a la lista existente
            promedios_lcp[valor_nominal].append(value)

# Calcular el promedio para cada valor nominal y almacenarlo en un nuevo diccionario
    promedios_finales_lcp = {}
    for valor_nominal, medidas in promedios_lcp.items():
      promedio = sum(medidas) / len(medidas)
      promedios_finales_lcp[valor_nominal] = promedio
      
      
      # Crear un diccionario para almacenar los valores promedio por valor nominal
    promedios_lcetibc = {}

# Iterar sobre el diccionario de resultados
    for key, value in correccion_temp.items():
       if "IBC" in key and "_ajuste_a_0" in key:
        # Obtener el valor nominal
        valor_nominal = key.split('_')[1]
        # Verificar si el valor nominal ya está en el diccionario de promedios
        if valor_nominal not in promedios_lcetibc:
            # Si no está, inicializar una lista con el valor actual
            promedios_lcetibc[valor_nominal] = [value]
        else:
            # Si está, agregar el valor a la lista existente
            promedios_lcetibc[valor_nominal].append(value)

# Calcular el promedio para cada valor nominal y almacenarlo en un nuevo diccionario
    promedios_finales_lcetibc = {}
    for valor_nominal, medidas in promedios_lcetibc.items():
      promedio = sum(medidas) / len(medidas)
      promedios_finales_lcetibc[valor_nominal] = promedio
      
      promedios_ep = {}

# Iterar sobre el diccionario de resultados
    for key, value in error_patron.items():
       if "patron" in key and "_ajuste_a_0" in key:
        # Obtener el valor nominal
        valor_nominal = key.split('_')[1]
        # Verificar si el valor nominal ya está en el diccionario de promedios
        if valor_nominal not in promedios_ep:
            # Si no está, inicializar una lista con el valor actual
            promedios_ep[valor_nominal] = [value]
        else:
            # Si está, agregar el valor a la lista existente
            promedios_ep[valor_nominal].append(value)

# Calcular el promedio para cada valor nominal y almacenarlo en un nuevo diccionario
    promedios_finales_ep = {}
    for valor_nominal, medidas in promedios_ep.items():
      promedio = sum(medidas) / len(medidas)
      promedios_finales_ep[valor_nominal] = promedio
      
      
    E_values = {}
    for i in range(1, 6):  # Suponiendo que tienes 5 valores nominales
       nominal_key = f'nominal{i}'
       lcp = promedios_finales_lcp.get(nominal_key)
       lcetibc = promedios_finales_lcetibc.get(nominal_key)
       ep = promedios_finales_ep.get(nominal_key)
       E = lcetibc - (lcp - ep)
       E_values[nominal_key] = E
 # Crear un nuevo diccionario para almacenar los resultados de las restas
    histeresis_IBC = {}

# Iterar sobre el diccionario de valores nominales
    for key, value in correccion_temp.items():
    # Verificar si la clave contiene "IBC_ascenso" y "ciclo1"
       if "IBC_ascenso" in key and "ciclo1" in key:
        # Crear la clave correspondiente para "descenso"
           descenso_key = key.replace("ascenso", "descenso")
           if descenso_key in correccion_temp:
            # Realizar la resta y almacenar el resultado en el diccionario
            histeresis_IBC[key] = value - correccion_temp[descenso_key]
    histeresis_patron = {}

# Iterar sobre el diccionario de valores nominales
    for key, value in resultados_con_presion_columna.items():
    # Verificar si la clave contiene "IBC_ascenso" y "ciclo1"
       if "patron_ascenso" in key and "ciclo1" in key:
        # Crear la clave correspondiente para "descenso"
           descenso_key = key.replace("ascenso", "descenso")
           if descenso_key in resultados_con_presion_columna:
            # Realizar la resta y almacenar el resultado en el diccionario
            histeresis_patron[key] = value - resultados_con_presion_columna[descenso_key]
    
    incertidumbre_histererisis_ibc = {}
    
    for key, value in histeresis_IBC.items():
      incertidumbre_histererisis_ibc[key] = value/math.sqrt(12)
      

    incertidumbre_repetibilidad_IBC = {}
    for valor_nominal in range(1, 6):
        valores = [v for k, v in correccion_temp.items() if f'valor_nominal{valor_nominal}' in k and 'IBC' in k and '_ajuste_a_0' in k]
        suma = sum(valores)
        media = suma / len(valores)
        suma_cuadrados = sum((valor - media) ** 2 for valor in valores)
        desviacion = (math.sqrt(suma_cuadrados / (len(valores) - 1))) / math.sqrt(3)

        incertidumbre_repetibilidad_IBC[valor_nominal] = desviacion
    incertidumbre_cal_patron = {}

# Itera sobre cada par clave-valor en el diccionario `resultados_con_presion_columna`
    for key, number in promedios_finales_lcp.items():
    # Calcula la expresión polinómica usando los coeficientes de la curva del patrón
        incertidumbre_cal_patron[key] = ((((number**10) * curva_patron.ca_i_x10) + ((number**9) * curva_patron.ca_i_x9) + ((number**8) * curva_patron.ca_i_x8) + ((number**7) * curva_patron.ca_i_x7) +
                      ((number**6) * curva_patron.ca_i_x6) + ((number**5) * curva_patron.ca_i_x5) + ((number**4) * curva_patron.ca_i_x4) + ((number**3) * curva_patron.ca_i_x3) +
                      ((number**2) * curva_patron.ca_i_x2) + (number * curva_patron.ca_i_x) + curva_patron.ca_i_B))/2
    incertidumbre_repetibilidad_patron = {}

    for valor_nominal in range(1, 6):
    # Filtrar solo los valores correspondientes al valor nominal actual, lectura del patrón y ajuste a cero
       valores = [v for k, v in resultados_con_presion_columna.items() if f'valor_nominal{valor_nominal}' in k and 'lectura_patron' in k and 'ajuste_a_0' in k]
    
    # Calcular la media
       suma = round(sum(valores),6)
       media = round(suma / len(valores), 6)
    
    # Calcular la desviación estándar
       suma_cuadrados = round(sum((valor - media) ** 2 for valor in valores),6)
       desviacion = (math.sqrt(suma_cuadrados / (len(valores) - 1))) / math.sqrt(3)

       incertidumbre_repetibilidad_patron[valor_nominal] = desviacion
      
    max_key = max(histeresis_patron, key=histeresis_patron.get)
    max_value_hp = histeresis_patron[max_key]
 
    incertidumbre_hp =  (max_value_hp)/math.sqrt(12)
    
    u_total={
      'u_1': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[1]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal1']**2 +
    incertidumbre_repetibilidad_IBC[1]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal1_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
),
        'u_2': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[2]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal2']**2 +
    incertidumbre_repetibilidad_IBC[2]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal2_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
),
          'u_3': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[3]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal3']**2 +
    incertidumbre_repetibilidad_IBC[3]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal3_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
),  'u_4': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[4]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal4']**2 +
    incertidumbre_repetibilidad_IBC[4]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal4_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
),  'u_5': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[5]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal5']**2 +
    incertidumbre_repetibilidad_IBC[5]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal5_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
)
    }
    
    u_total_duplicado = {k: v * 2 for k, v in u_total.items()}
      
    context = {
        'incertidumbre_densidad_aire' : incertidumbre_densidad_aire,
        'densidad_aire':densidad_aire,
        'u_total_duplicado' : u_total_duplicado,
        'u_total' : u_total,
        'incertidumbre_hp' : incertidumbre_hp,
        'max_value_hp' : max_value_hp,
        'incertidumbre_repetibilidad_patron' : incertidumbre_repetibilidad_patron,
        'incertidumbre_cal_patron' : incertidumbre_cal_patron,
        'incertidumbre_repetibilidad_IBC' : incertidumbre_repetibilidad_IBC,
        'incertidumbre_histererisis_ibc':incertidumbre_histererisis_ibc,
        'histeresis_patron' : histeresis_patron,
        'histeresis_IBC' : histeresis_IBC,
        'E_values':E_values,
        'promedios_finales_ep':promedios_finales_ep,
        'promedios_finales_lcetibc':promedios_finales_lcetibc,
        'correccion_temp' : correccion_temp,
        'error_patron' : error_patron,
        'resultados_con_presion_columna':resultados_con_presion_columna,
        'promedios_finales':promedios_finales,
        'resultados': resultados,
        'presion_columna' : presion_columna,
        'gravedad_local': gravedad_local,
        'latitud' : latitud,
        'mifolio': mifolio,
        'temperatura_amb_prom':temperatura_amb_prom,
        'promedios_finales_lcp': promedios_finales_lcp,
        
        'curva' : curva_patron,
        'ca_x10': curva_patron.ca_x10,
        'ca_x9': curva_patron.ca_x9,
        'ca_x8': curva_patron.ca_x8,
        'ca_x7': curva_patron.ca_x7,
        'ca_x6': curva_patron.ca_x6,
        'ca_x5': curva_patron.ca_x5,
        'ca_x4': curva_patron.ca_x4,
        'ca_x3': curva_patron.ca_x3,
        'ca_x2': curva_patron.ca_x2,
        'ca_x': curva_patron.ca_x,
        'ca_B': curva_patron.ca_B,
        
        'ca_i_x10': curva_patron.ca_i_x10,
        'ca_i_x9': curva_patron.ca_i_x9,
        'ca_i_x8': curva_patron.ca_i_x8,
        'ca_i_x7': curva_patron.ca_i_x7,
        'ca_i_x6': curva_patron.ca_i_x6,
        'ca_i_x5': curva_patron.ca_i_x5,
        'ca_i_x4': curva_patron.ca_i_x4,
        'ca_i_x3': curva_patron.ca_i_x3,
        'ca_i_x2': curva_patron.ca_i_x2,
        'ca_i_x': curva_patron.ca_i_x,
        'ca_i_B': curva_patron.ca_i_B,
        'incertidumbre_curva_patron' : incertidumbre_curva_patron,
        'incertidumbre_curva_patron_error' : incertidumbre_curva_patron_error,
        'incertidumbre_resolucion' : incertidumbre_resolucion,
        'incertidumbre_deriva_0': incertidumbre_deriva_0,
        'incertidumbre_deriva_patron' : incertidumbre_deriva_patron,
        'incertidumbre_deriva_0_patron' : incertidumbre_deriva_0_patron,
        'u_gravedad_local' : u_gravedad_local,
        'u_diferencia_altura' : u_diferencia_altura,
        'u_PCOL':u_PCOL,
        'u_reproducibilidad': curva_patron.reproducibilidad,
        

    }
  
    return HttpResponse(template.render(context, request))



    
  

  
  
def calculos_pm(request, id):

    template = loader.get_template('calculos_pm.html')

    mifolio = PresionManometrica.objects.get(id=id)
    
    densidad_aceite=912
    curva_patron = PatronesPresionManometrica.objects.get(id=mifolio.patron_id_presion_manometrica_id)
    diferencia_altura = mifolio.ambientales_altura_patron-mifolio.ambientales_altura_IBC
    latitud = mifolio.sitio_lat_degrees + mifolio.sitio_lat_minutes / 60 + mifolio.sitio_lat_seconds / 3600
    gravedad_local = (9.780318*(1+(0.0053024*(math.sin(math.pi*latitud/180)**2))-0.0000058*(math.sin(2*math.pi*latitud/180)**2))-(0.000003086*mifolio.sitio_altura))
    presion_columna = (912*gravedad_local*(mifolio.ambientales_altura_patron-mifolio.ambientales_altura_IBC))/1000
    temperatura_amb_prom = (mifolio.ambientales_temperatura_inicial + mifolio.ambientales_temperatura_final)/2
    #incertidumbre
    instrumento_resolucion_float = float(mifolio.instrumento_resolucion)
    incertidumbre_resolucion = instrumento_resolucion_float / math.sqrt(12)
    deriva_0_ibc_c1 = float(mifolio.desviacion_ciclo1_IBC)
    deriva_0_ibc_c2 = float(mifolio.desviacion_ciclo2_IBC)
    incertidumbre_deriva_0= (deriva_0_ibc_c1-deriva_0_ibc_c2)/ math.sqrt(3)
    incertidumbre_curva_patron = (curva_patron.ca_i_residuales)/math.sqrt(12)
    incertidumbre_curva_patron_error = (curva_patron.ca_residuales)/math.sqrt(12)
    deriva_patron =float(curva_patron.deriva)
    incertidumbre_deriva_patron = (deriva_patron)/(math.sqrt(12))
    incertidumbre_deriva_0_patron = (mifolio.desviacion_ciclo1_patron - mifolio.desviacion_ciclo2_patron)/math.sqrt(3)
    u_gravedad_local=(gravedad_local*0.0001)/(math.sqrt(3))
    u_densidad=(0.02851*densidad_aceite)
    u_diferencia_altura = (diferencia_altura)/(math.sqrt(12))
    u_PCOL = (math.sqrt(
    (gravedad_local * diferencia_altura * u_densidad)**2 +
    (densidad_aceite * diferencia_altura * u_gravedad_local)**2 +
    (gravedad_local * densidad_aceite * u_diferencia_altura)**2
    ))/1000
    #calculos error 
    
    unidades_toma_datos=mifolio.unidades_toma_datos
   
    valores_nominales = {
    'desviacion_ciclo1_patron': mifolio.desviacion_ciclo1_patron,
    'desviacion_ciclo1_IBC': mifolio.desviacion_ciclo1_IBC,
    'desviacion_ciclo2_patron': mifolio.desviacion_ciclo2_patron,
    'desviacion_ciclo2_IBC': mifolio.desviacion_ciclo2_IBC,
    
    'valor_nominal1_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal1_ciclo1_lectura_patron_ascenso,
    'valor_nominal1_ciclo1_lectura_patron_descenso': mifolio.valor_nominal1_ciclo1_lectura_patron_descenso,
    'valor_nominal1_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal1_ciclo1_lectura_IBC_ascenso,
    'valor_nominal1_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal1_ciclo1_lectura_IBC_descenso,
    'valor_nominal1_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal1_ciclo2_lectura_patron_ascenso,
    'valor_nominal1_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal1_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal2_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal2_ciclo1_lectura_patron_ascenso,
    'valor_nominal2_ciclo1_lectura_patron_descenso': mifolio.valor_nominal2_ciclo1_lectura_patron_descenso,
    'valor_nominal2_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal2_ciclo1_lectura_IBC_ascenso,
    'valor_nominal2_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal2_ciclo1_lectura_IBC_descenso,
    'valor_nominal2_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal2_ciclo2_lectura_patron_ascenso,
    'valor_nominal2_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal2_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal3_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal3_ciclo1_lectura_patron_ascenso,
    'valor_nominal3_ciclo1_lectura_patron_descenso': mifolio.valor_nominal3_ciclo1_lectura_patron_descenso,
    'valor_nominal3_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal3_ciclo1_lectura_IBC_ascenso,
    'valor_nominal3_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal3_ciclo1_lectura_IBC_descenso,
    'valor_nominal3_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal3_ciclo2_lectura_patron_ascenso,
    'valor_nominal3_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal3_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal4_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal4_ciclo1_lectura_patron_ascenso,
    'valor_nominal4_ciclo1_lectura_patron_descenso': mifolio.valor_nominal4_ciclo1_lectura_patron_descenso,
    'valor_nominal4_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal4_ciclo1_lectura_IBC_ascenso,
    'valor_nominal4_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal4_ciclo1_lectura_IBC_descenso,
    'valor_nominal4_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal4_ciclo2_lectura_patron_ascenso,
    'valor_nominal4_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal4_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal5_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal5_ciclo1_lectura_patron_ascenso,
    'valor_nominal5_ciclo1_lectura_patron_descenso': mifolio.valor_nominal5_ciclo1_lectura_patron_descenso,
    'valor_nominal5_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal5_ciclo1_lectura_IBC_ascenso,
    'valor_nominal5_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal5_ciclo1_lectura_IBC_descenso,
    'valor_nominal5_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal5_ciclo2_lectura_patron_ascenso,
    'valor_nominal5_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal5_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal1_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal1_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal1_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal1_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal1_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal1_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal1_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal1_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal1_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal1_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal1_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal1_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,
    
    'valor_nominal2_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal2_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal2_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal2_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal2_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal2_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal2_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal2_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal2_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal2_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal2_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal2_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,

    'valor_nominal3_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal3_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal3_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal3_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal3_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal3_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal3_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal3_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal3_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal3_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal3_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal3_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,

    'valor_nominal4_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal4_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal4_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal4_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal4_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal4_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal4_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal4_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal4_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal4_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal4_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal4_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,

    'valor_nominal5_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal5_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal5_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal5_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal5_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal5_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal5_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal5_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal5_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal5_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal5_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal5_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,

}

# Diccionario para almacenar los resultados
    resultados = {}

# Convertir los valores nominales según la unidad de medida
    for key, valor_nominal in valores_nominales.items():
      if unidades_toma_datos == "Lb*f/in2":
        resultado = round(valor_nominal * 6.89476, 8)
      elif unidades_toma_datos == "kg*f/cm2":
        resultado = round(valor_nominal * 98.0665, 8)
      elif unidades_toma_datos == "kg*f/cm2":
        resultado = round(valor_nominal * 98.0665, 8)
      else:
        resultado = valor_nominal  # Mantener el valor nominal si son kPa

      resultados[key] = resultado

# Crear un diccionario para almacenar los valores promedio por valor nominal
    promedios_por_valor_nominal = {}

# Iterar sobre el diccionario de resultados
    for key, value in resultados.items():
    # Verificar si la medida tiene "IBC" en el nombre y "_ajuste_a_0" al final
       if "IBC" in key and "_ajuste_a_0" in key:
        # Obtener el valor nominal
        valor_nominal = key.split('_')[1]
        # Verificar si el valor nominal ya está en el diccionario de promedios
        if valor_nominal not in promedios_por_valor_nominal:
            # Si no está, inicializar una lista con el valor actual
            promedios_por_valor_nominal[valor_nominal] = [value]
        else:
            # Si está, agregar el valor a la lista existente
            promedios_por_valor_nominal[valor_nominal].append(value)

# Calcular el promedio para cada valor nominal y almacenarlo en un nuevo diccionario
    promedios_finales = {}
    for valor_nominal, medidas in promedios_por_valor_nominal.items():
      promedio = sum(medidas) / len(medidas)
      promedios_finales[valor_nominal] = promedio

    resultados_con_presion_columna = {}

# Itera sobre los elementos del diccionario original
    for key, value in resultados.items():
    # Resta presion_columna al valor actual y almacena el resultado en el nuevo diccionario
        resultados_con_presion_columna[key] = value - presion_columna

# Crea un nuevo diccionario para almacenar los errores del patrón
    error_patron = {}

# Itera sobre cada par clave-valor en el diccionario `resultados_con_presion_columna`
    for key, number in resultados_con_presion_columna.items():
    # Calcula la expresión polinómica usando los coeficientes de la curva del patrón
        error_patron[key] = (((number**10) * curva_patron.ca_x10) + ((number**9) * curva_patron.ca_x9) + ((number**8) * curva_patron.ca_x8) + ((number**7) * curva_patron.ca_x7) +
                      ((number**6) * curva_patron.ca_x6) + ((number**5) * curva_patron.ca_x5) + ((number**4) * curva_patron.ca_x4) + ((number**3) * curva_patron.ca_x3) +
                      ((number**2) * curva_patron.ca_x2) + (number * curva_patron.ca_x) + curva_patron.ca_B)
    
    correccion_temp= {}
    
    for key, number in resultados.items():
   # Convertir las cadenas a números flotantes si es necesario
        temperatura_amb_prom = float(temperatura_amb_prom)
        mifolio.coeficiente_termico = float(mifolio.coeficiente_termico)
        mifolio.temperatura_referencia_IBC = float(mifolio.temperatura_referencia_IBC)

# Realizar la operación corregida
        correccion_temp[key] = number * (1 + (mifolio.coeficiente_termico * (temperatura_amb_prom - mifolio.temperatura_referencia_IBC)))



# Crear un diccionario para almacenar los valores promedio por valor nominal
    promedios_lcp = {}

# Iterar sobre el diccionario de resultados
    for key, value in resultados_con_presion_columna.items():
       if "patron" in key and "_ajuste_a_0" in key:
        # Obtener el valor nominal
        valor_nominal = key.split('_')[1]
        # Verificar si el valor nominal ya está en el diccionario de promedios
        if valor_nominal not in promedios_lcp:
            # Si no está, inicializar una lista con el valor actual
            promedios_lcp[valor_nominal] = [value]
        else:
            # Si está, agregar el valor a la lista existente
            promedios_lcp[valor_nominal].append(value)

# Calcular el promedio para cada valor nominal y almacenarlo en un nuevo diccionario
    promedios_finales_lcp = {}
    for valor_nominal, medidas in promedios_lcp.items():
      promedio = sum(medidas) / len(medidas)
      promedios_finales_lcp[valor_nominal] = promedio
      
      
      # Crear un diccionario para almacenar los valores promedio por valor nominal
    promedios_lcetibc = {}

# Iterar sobre el diccionario de resultados
    for key, value in correccion_temp.items():
       if "IBC" in key and "_ajuste_a_0" in key:
        # Obtener el valor nominal
        valor_nominal = key.split('_')[1]
        # Verificar si el valor nominal ya está en el diccionario de promedios
        if valor_nominal not in promedios_lcetibc:
            # Si no está, inicializar una lista con el valor actual
            promedios_lcetibc[valor_nominal] = [value]
        else:
            # Si está, agregar el valor a la lista existente
            promedios_lcetibc[valor_nominal].append(value)

# Calcular el promedio para cada valor nominal y almacenarlo en un nuevo diccionario
    promedios_finales_lcetibc = {}
    for valor_nominal, medidas in promedios_lcetibc.items():
      promedio = sum(medidas) / len(medidas)
      promedios_finales_lcetibc[valor_nominal] = promedio
      
      promedios_ep = {}

# Iterar sobre el diccionario de resultados
    for key, value in error_patron.items():
       if "patron" in key and "_ajuste_a_0" in key:
        # Obtener el valor nominal
        valor_nominal = key.split('_')[1]
        # Verificar si el valor nominal ya está en el diccionario de promedios
        if valor_nominal not in promedios_ep:
            # Si no está, inicializar una lista con el valor actual
            promedios_ep[valor_nominal] = [value]
        else:
            # Si está, agregar el valor a la lista existente
            promedios_ep[valor_nominal].append(value)

# Calcular el promedio para cada valor nominal y almacenarlo en un nuevo diccionario
    promedios_finales_ep = {}
    for valor_nominal, medidas in promedios_ep.items():
      promedio = sum(medidas) / len(medidas)
      promedios_finales_ep[valor_nominal] = promedio
      
      
    E_values = {}
    for i in range(1, 6):  # Suponiendo que tienes 5 valores nominales
       nominal_key = f'nominal{i}'
       lcp = promedios_finales_lcp.get(nominal_key)
       lcetibc = promedios_finales_lcetibc.get(nominal_key)
       ep = promedios_finales_ep.get(nominal_key)
       E = lcetibc - (lcp - ep)
       E_values[nominal_key] = E
 # Crear un nuevo diccionario para almacenar los resultados de las restas
    histeresis_IBC = {}

# Iterar sobre el diccionario de valores nominales
    for key, value in correccion_temp.items():
    # Verificar si la clave contiene "IBC_ascenso" y "ciclo1"
       if "IBC_ascenso" in key and "ciclo1" in key:
        # Crear la clave correspondiente para "descenso"
           descenso_key = key.replace("ascenso", "descenso")
           if descenso_key in correccion_temp:
            # Realizar la resta y almacenar el resultado en el diccionario
            histeresis_IBC[key] = value - correccion_temp[descenso_key]
    histeresis_patron = {}

# Iterar sobre el diccionario de valores nominales
    for key, value in resultados_con_presion_columna.items():
    # Verificar si la clave contiene "IBC_ascenso" y "ciclo1"
       if "patron_ascenso" in key and "ciclo1" in key:
        # Crear la clave correspondiente para "descenso"
           descenso_key = key.replace("ascenso", "descenso")
           if descenso_key in resultados_con_presion_columna:
            # Realizar la resta y almacenar el resultado en el diccionario
            histeresis_patron[key] = value - resultados_con_presion_columna[descenso_key]
    
    incertidumbre_histererisis_ibc = {}
    
    for key, value in histeresis_IBC.items():
      incertidumbre_histererisis_ibc[key] = value/math.sqrt(12)
      

    incertidumbre_repetibilidad_IBC = {}
    for valor_nominal in range(1, 6):
        valores = [v for k, v in correccion_temp.items() if f'valor_nominal{valor_nominal}' in k and 'IBC' in k and '_ajuste_a_0' in k]
        suma = sum(valores)
        media = suma / len(valores)
        suma_cuadrados = sum((valor - media) ** 2 for valor in valores)
        desviacion = (math.sqrt(suma_cuadrados / (len(valores) - 1))) / math.sqrt(3)

        incertidumbre_repetibilidad_IBC[valor_nominal] = desviacion
    incertidumbre_cal_patron = {}

# Itera sobre cada par clave-valor en el diccionario `resultados_con_presion_columna`
    for key, number in promedios_finales_lcp.items():
    # Calcula la expresión polinómica usando los coeficientes de la curva del patrón
        incertidumbre_cal_patron[key] = ((((number**10) * curva_patron.ca_i_x10) + ((number**9) * curva_patron.ca_i_x9) + ((number**8) * curva_patron.ca_i_x8) + ((number**7) * curva_patron.ca_i_x7) +
                      ((number**6) * curva_patron.ca_i_x6) + ((number**5) * curva_patron.ca_i_x5) + ((number**4) * curva_patron.ca_i_x4) + ((number**3) * curva_patron.ca_i_x3) +
                      ((number**2) * curva_patron.ca_i_x2) + (number * curva_patron.ca_i_x) + curva_patron.ca_i_B))/2
    incertidumbre_repetibilidad_patron = {}

    for valor_nominal in range(1, 6):
    # Filtrar solo los valores correspondientes al valor nominal actual, lectura del patrón y ajuste a cero
       valores = [v for k, v in resultados_con_presion_columna.items() if f'valor_nominal{valor_nominal}' in k and 'lectura_patron' in k and 'ajuste_a_0' in k]
    
    # Calcular la media
       suma = round(sum(valores),6)
       media = round(suma / len(valores), 6)
    
    # Calcular la desviación estándar
       suma_cuadrados = round(sum((valor - media) ** 2 for valor in valores),6)
       desviacion = (math.sqrt(suma_cuadrados / (len(valores) - 1))) / math.sqrt(3)

       incertidumbre_repetibilidad_patron[valor_nominal] = desviacion
      
    max_key = max(histeresis_patron, key=histeresis_patron.get)
    max_value_hp = histeresis_patron[max_key]
 
    incertidumbre_hp =  (max_value_hp)/math.sqrt(12)
    
    u_total={
      'u_1': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[1]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal1']**2 +
    incertidumbre_repetibilidad_IBC[1]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal1_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
),
        'u_2': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[2]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal2']**2 +
    incertidumbre_repetibilidad_IBC[2]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal2_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
),
          'u_3': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[3]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal3']**2 +
    incertidumbre_repetibilidad_IBC[3]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal3_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
),  'u_4': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[4]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal4']**2 +
    incertidumbre_repetibilidad_IBC[4]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal4_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
),  'u_5': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[5]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal5']**2 +
    incertidumbre_repetibilidad_IBC[5]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal5_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
)
    }
    
    u_total_duplicado = {k: v * 2 for k, v in u_total.items()}
      
    context = {
      
        'u_total_duplicado' : u_total_duplicado,
        'u_total' : u_total,
        'incertidumbre_hp' : incertidumbre_hp,
        'max_value_hp' : max_value_hp,
        'incertidumbre_repetibilidad_patron' : incertidumbre_repetibilidad_patron,
        'incertidumbre_cal_patron' : incertidumbre_cal_patron,
        'incertidumbre_repetibilidad_IBC' : incertidumbre_repetibilidad_IBC,
        'incertidumbre_histererisis_ibc':incertidumbre_histererisis_ibc,
        'histeresis_patron' : histeresis_patron,
        'histeresis_IBC' : histeresis_IBC,
        'E_values':E_values,
        'promedios_finales_ep':promedios_finales_ep,
        'promedios_finales_lcetibc':promedios_finales_lcetibc,
        'correccion_temp' : correccion_temp,
        'error_patron' : error_patron,
        'resultados_con_presion_columna':resultados_con_presion_columna,
        'promedios_finales':promedios_finales,
        'resultados': resultados,
        'presion_columna' : presion_columna,
        'gravedad_local': gravedad_local,
        'latitud' : latitud,
        'mifolio': mifolio,
        'temperatura_amb_prom':temperatura_amb_prom,
        'promedios_finales_lcp': promedios_finales_lcp,
        
        'curva' : curva_patron,
        'ca_x10': curva_patron.ca_x10,
        'ca_x9': curva_patron.ca_x9,
        'ca_x8': curva_patron.ca_x8,
        'ca_x7': curva_patron.ca_x7,
        'ca_x6': curva_patron.ca_x6,
        'ca_x5': curva_patron.ca_x5,
        'ca_x4': curva_patron.ca_x4,
        'ca_x3': curva_patron.ca_x3,
        'ca_x2': curva_patron.ca_x2,
        'ca_x': curva_patron.ca_x,
        'ca_B': curva_patron.ca_B,
        
        'ca_i_x10': curva_patron.ca_i_x10,
        'ca_i_x9': curva_patron.ca_i_x9,
        'ca_i_x8': curva_patron.ca_i_x8,
        'ca_i_x7': curva_patron.ca_i_x7,
        'ca_i_x6': curva_patron.ca_i_x6,
        'ca_i_x5': curva_patron.ca_i_x5,
        'ca_i_x4': curva_patron.ca_i_x4,
        'ca_i_x3': curva_patron.ca_i_x3,
        'ca_i_x2': curva_patron.ca_i_x2,
        'ca_i_x': curva_patron.ca_i_x,
        'ca_i_B': curva_patron.ca_i_B,
        'incertidumbre_curva_patron' : incertidumbre_curva_patron,
        'incertidumbre_curva_patron_error' : incertidumbre_curva_patron_error,
        'incertidumbre_resolucion' : incertidumbre_resolucion,
        'incertidumbre_deriva_0': incertidumbre_deriva_0,
        'incertidumbre_deriva_patron' : incertidumbre_deriva_patron,
        'incertidumbre_deriva_0_patron' : incertidumbre_deriva_0_patron,
        'u_gravedad_local' : u_gravedad_local,
        'u_densidad' : u_densidad,
        'u_diferencia_altura' : u_diferencia_altura,
        'u_PCOL':u_PCOL,
        'u_reproducibilidad': curva_patron.reproducibilidad,
        

    }
  
    return HttpResponse(template.render(context, request))


def calculos_pd(request, id) :


    template = loader.get_template('calculos_pd.html')

    mifolio = PresionDiferencial.objects.get(id=id)
    
    
    temperatura_amb_prom = (mifolio.ambientales_temperatura_inicial + mifolio.ambientales_temperatura_final)/2

    
    humedad_relativa = (mifolio.ambientales_humedad_relativa_inicial + mifolio.ambientales_humedad_relativa_final)/2
    EC_p = (
        (0.000012378847 * ((temperatura_amb_prom +273.15)** 2)) +
        (-0.019121316 * (temperatura_amb_prom+273.15)) +
        33.93711047 +
        (-6343.1645 / (temperatura_amb_prom + 273.15))
    )
    presion_vapor_s= 1 * math.exp(
        (0.000012378847 * ((temperatura_amb_prom +273.15)** 2)) +
        (-0.019121316 * (temperatura_amb_prom+273.15)) +
        33.93711047 +
        (-6343.1645 / (temperatura_amb_prom + 273.15))
    )
    
    factor_fugacidad = 1.00062 + (0.0000000314 * mifolio.ambientales_presion_barometrica_inicial) + (0.00000056 * (temperatura_amb_prom ** 2))
    
    factor_molar_vapor = (factor_fugacidad*(humedad_relativa/100))*(presion_vapor_s/mifolio.ambientales_presion_barometrica_inicial)
    
    factor_compresibilidad = 1 - (mifolio.ambientales_presion_barometrica_inicial / (temperatura_amb_prom + 273.15)) * (
            (((0.00000158123 + (-0.000000029331 * temperatura_amb_prom) + (0.00000000011043 * temperatura_amb_prom**2)) +
              ((0.000005707 + (-0.00000002051 * temperatura_amb_prom))) * factor_molar_vapor) +
            (0.00019898 + (-0.000002376 * 0.00000158123) * factor_molar_vapor**2) +
            ((mifolio.ambientales_presion_barometrica_inicial**2) / ((temperatura_amb_prom + 273.15)**2)) * (
                0.0000000000183 + 0.00000000765 * factor_molar_vapor**2
            )
    )
    )

    
    pma= 0.02896351244*mifolio.ambientales_presion_barometrica_inicial
    zrt = factor_compresibilidad*(8.31451)*(temperatura_amb_prom + 273.15)
    mv_ma= 0.018015/0.02896351244
    L=pma/zrt
    
    densidad_aire= L*(1-(factor_molar_vapor*(1-mv_ma)))

    curva_patron = PatronesPresionManometrica.objects.get(id=mifolio.patron_id_presion_manometrica_id)
    diferencia_altura = mifolio.ambientales_altura_patron-mifolio.ambientales_altura_IBC
    latitud = mifolio.sitio_lat_degrees + mifolio.sitio_lat_minutes / 60 + mifolio.sitio_lat_seconds / 3600
    gravedad_local = (9.780318*(1+(0.0053024*(math.sin(math.pi*latitud/180)**2))-0.0000058*(math.sin(2*math.pi*latitud/180)**2))-(0.000003086*mifolio.sitio_altura))
    presion_columna = (densidad_aire*gravedad_local*(mifolio.ambientales_altura_patron-mifolio.ambientales_altura_IBC))/1000
    #incertidumbre
    instrumento_resolucion_float = float(mifolio.instrumento_resolucion)
    unidades_toma_datos = mifolio.unidades_toma_datos
    
    # Condicional para convertir el valor nominal
    if unidades_toma_datos == "Lb*f/in2":
        resultado = float(instrumento_resolucion_float * 6.89476)
    elif unidades_toma_datos == "kg*f/cm2":
        resultado = float(instrumento_resolucion_float * 98.0665)
    elif unidades_toma_datos == "inH2O":
        resultado = float(instrumento_resolucion_float * 0.2490889)
    else:
        resultado = instrumento_resolucion_float

    # Calcular la incertidumbre de resolución
    instrumento_resolucion_float = resultado
    
    
    incertidumbre_resolucion = instrumento_resolucion_float / math.sqrt(12)
    
    
    deriva_0_ibc_c1 = float(mifolio.desviacion_ciclo1_IBC)
    deriva_0_ibc_c2 = float(mifolio.desviacion_ciclo2_IBC)
    incertidumbre_deriva_0= (deriva_0_ibc_c1-deriva_0_ibc_c2)/ math.sqrt(3)
    incertidumbre_curva_patron = (curva_patron.ca_i_residuales)/math.sqrt(12)
    incertidumbre_curva_patron_error = (curva_patron.ca_residuales)/math.sqrt(12)
    deriva_patron =float(curva_patron.deriva)
    incertidumbre_deriva_patron = (deriva_patron)/(math.sqrt(12))
    incertidumbre_deriva_0_patron = (mifolio.desviacion_ciclo1_patron - mifolio.desviacion_ciclo2_patron)/math.sqrt(3)
  
    u_gravedad_local=(gravedad_local*0.0001)/(math.sqrt(3))
 
    dPsv_dt =  math.exp(EC_p) * (
    (2 * 0.000012378847 * (temperatura_amb_prom + 273.15)) +
    -0.019121316 -
    (-6343.1645 / ((temperatura_amb_prom + 273.15) ** 2))  # Corrigiendo la temperatura en el denominador
)
    
    df_dp = 0.0000000314
    df_dt = 2*(0.00000056)*temperatura_amb_prom
    dXv_dh =(presion_vapor_s)*(factor_fugacidad)/(mifolio.ambientales_presion_barometrica_inicial)
    dXv_df = 50/100*presion_vapor_s/mifolio.ambientales_presion_barometrica_inicial
    dxv_dp = -50/100*factor_fugacidad*presion_vapor_s/mifolio.ambientales_presion_barometrica_inicial**2
    dXv_dPsv = 50/100*factor_fugacidad/mifolio.ambientales_presion_barometrica_inicial
    dZ_dp = (-1/(temperatura_amb_prom+273.15))*(((0.00000158123+(-0.000000029331*temperatura_amb_prom)+(0.00000000011043*temperatura_amb_prom**2))+((0.000005707+(-0.00000002051*0.00000158123)))*factor_molar_vapor)+(0.00019898+(-0.000002376*temperatura_amb_prom))*factor_molar_vapor**2)+(2*mifolio.ambientales_presion_barometrica_inicial/(temperatura_amb_prom+273.15)**2)*(0.0000000000183+-0.00000000765*factor_molar_vapor**2)
    zrt_2=factor_compresibilidad*(8.31451)*((temperatura_amb_prom + 273.15)**2)
    zr_2t=factor_compresibilidad*((8.31451)**2)*(temperatura_amb_prom + 273.15)   
    dZ_dT= (mifolio.ambientales_presion_barometrica_inicial/(temperatura_amb_prom+273.15)**2)*(((0.00000158123+(-0.000000029331*temperatura_amb_prom)+(0.00000000011043*temperatura_amb_prom**2))+((0.000005707+(-0.00000002051*temperatura_amb_prom)))*factor_molar_vapor)+(0.00019898+(-0.000002376*temperatura_amb_prom))*factor_molar_vapor**2)-(2*mifolio.ambientales_presion_barometrica_final**2/(temperatura_amb_prom+273.15)**3)*(0.0000000000183+-0.00000000765*factor_molar_vapor**2)
    dZ_dt = (-mifolio.ambientales_presion_barometrica_inicial/(temperatura_amb_prom+273.15))*(-0.000000029331 + 2*0.00000000011043*temperatura_amb_prom+(-0.00000002051)*factor_molar_vapor+(-0.000002376)*factor_molar_vapor**2)
    dZ_dXv = (-mifolio.ambientales_presion_barometrica_inicial/(temperatura_amb_prom+273.15))*(0.000005707+(-0.00000002051)*0.00000158123+2*0.00019898*factor_molar_vapor+2*-0.000002376*temperatura_amb_prom*factor_molar_vapor)+(2*mifolio.ambientales_presion_barometrica_final**2*-0.00000000765*factor_molar_vapor/(temperatura_amb_prom+273.15)**2) 
    dp_dp =(0.02896351244/zrt)*(1-factor_molar_vapor*(1- mv_ma))
    dp_dz = (-pma/zrt)*(1-factor_molar_vapor*((1-mv_ma)))
    dp_dt =(-pma/zrt_2)*(1-factor_molar_vapor*(1-mv_ma))
    dp_dXV= (-pma/zrt)*(1-mv_ma)
    dp_dR =(-pma/zr_2t)*(1-factor_molar_vapor*(1-mv_ma))
    
    coeficiente_s_presion =(dp_dp+(dp_dz*dZ_dp)+(dp_dz*dZ_dXv*dXv_df*df_dp)+(dp_dz*dZ_dXv*dxv_dp)+(dp_dXV*dXv_df*df_dp)+(dp_dXV*dxv_dp))
    coeficiente_s_temperatura=(dp_dz*dZ_dT*1)+(dp_dz*dZ_dt)+(dp_dz*dZ_dXv*dXv_df*df_dt)+(dp_dz*dZ_dXv*dXv_dPsv*dPsv_dt*1)+(dp_dt*1)+(dp_dXV*dXv_df*df_dt)+(dp_dXV*dXv_dPsv*dPsv_dt*1)
    coeficiente_s_humedad_rel = (dp_dz*dZ_dXv*dXv_dh)+(dp_dXV*dXv_dh)
    coeficiente_s_constante = dp_dR
    incertidumbre_densidad_sum_cuadrados=(12.86*coeficiente_s_presion)**2+(0.455*coeficiente_s_temperatura)**2+(0.015*coeficiente_s_humedad_rel)**2+(0.0000084*coeficiente_s_constante)**2+(0.000095*1)**2
    incertidumbre_densidad_aire =2*( math.sqrt(incertidumbre_densidad_sum_cuadrados))

    u_diferencia_altura = (0.005)/(math.sqrt(12)) #norma tal parece equipo medicion nivel
    u_PCOL = (math.sqrt(
    (gravedad_local * diferencia_altura * incertidumbre_densidad_aire)**2 +
    (densidad_aire * diferencia_altura * u_gravedad_local)**2 +
    (gravedad_local * densidad_aire * u_diferencia_altura)**2
    ))/1000
    #calculos error 
    
    unidades_toma_datos=mifolio.unidades_toma_datos
   
    valores_nominales = {
    'desviacion_ciclo1_patron': mifolio.desviacion_ciclo1_patron,
    'desviacion_ciclo1_IBC': mifolio.desviacion_ciclo1_IBC,
    'desviacion_ciclo2_patron': mifolio.desviacion_ciclo2_patron,
    'desviacion_ciclo2_IBC': mifolio.desviacion_ciclo2_IBC,
    
    'valor_nominal1_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal1_ciclo1_lectura_patron_ascenso,
    'valor_nominal1_ciclo1_lectura_patron_descenso': mifolio.valor_nominal1_ciclo1_lectura_patron_descenso,
    'valor_nominal1_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal1_ciclo1_lectura_IBC_ascenso,
    'valor_nominal1_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal1_ciclo1_lectura_IBC_descenso,
    'valor_nominal1_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal1_ciclo2_lectura_patron_ascenso,
    'valor_nominal1_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal1_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal2_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal2_ciclo1_lectura_patron_ascenso,
    'valor_nominal2_ciclo1_lectura_patron_descenso': mifolio.valor_nominal2_ciclo1_lectura_patron_descenso,
    'valor_nominal2_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal2_ciclo1_lectura_IBC_ascenso,
    'valor_nominal2_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal2_ciclo1_lectura_IBC_descenso,
    'valor_nominal2_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal2_ciclo2_lectura_patron_ascenso,
    'valor_nominal2_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal2_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal3_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal3_ciclo1_lectura_patron_ascenso,
    'valor_nominal3_ciclo1_lectura_patron_descenso': mifolio.valor_nominal3_ciclo1_lectura_patron_descenso,
    'valor_nominal3_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal3_ciclo1_lectura_IBC_ascenso,
    'valor_nominal3_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal3_ciclo1_lectura_IBC_descenso,
    'valor_nominal3_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal3_ciclo2_lectura_patron_ascenso,
    'valor_nominal3_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal3_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal4_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal4_ciclo1_lectura_patron_ascenso,
    'valor_nominal4_ciclo1_lectura_patron_descenso': mifolio.valor_nominal4_ciclo1_lectura_patron_descenso,
    'valor_nominal4_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal4_ciclo1_lectura_IBC_ascenso,
    'valor_nominal4_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal4_ciclo1_lectura_IBC_descenso,
    'valor_nominal4_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal4_ciclo2_lectura_patron_ascenso,
    'valor_nominal4_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal4_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal5_ciclo1_lectura_patron_ascenso': mifolio.valor_nominal5_ciclo1_lectura_patron_ascenso,
    'valor_nominal5_ciclo1_lectura_patron_descenso': mifolio.valor_nominal5_ciclo1_lectura_patron_descenso,
    'valor_nominal5_ciclo1_lectura_IBC_ascenso': mifolio.valor_nominal5_ciclo1_lectura_IBC_ascenso,
    'valor_nominal5_ciclo1_lectura_IBC_descenso': mifolio.valor_nominal5_ciclo1_lectura_IBC_descenso,
    'valor_nominal5_ciclo2_lectura_patron_ascenso': mifolio.valor_nominal5_ciclo2_lectura_patron_ascenso,
    'valor_nominal5_ciclo2_lectura_IBC_ascenso': mifolio.valor_nominal5_ciclo2_lectura_IBC_ascenso,
    
    'valor_nominal1_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal1_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal1_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal1_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal1_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal1_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal1_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal1_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal1_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal1_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal1_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal1_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,
    
    'valor_nominal2_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal2_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal2_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal2_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal2_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal2_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal2_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal2_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal2_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal2_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal2_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal2_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,

    'valor_nominal3_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal3_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal3_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal3_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal3_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal3_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal3_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal3_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal3_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal3_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal3_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal3_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,

    'valor_nominal4_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal4_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal4_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal4_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal4_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal4_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal4_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal4_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal4_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal4_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal4_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal4_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,

    'valor_nominal5_ciclo1_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal5_ciclo1_lectura_patron_ascenso-mifolio.desviacion_ciclo1_patron,
    'valor_nominal5_ciclo1_lectura_patron_descenso_ajuste_a_0': mifolio.valor_nominal5_ciclo1_lectura_patron_descenso - mifolio.desviacion_ciclo1_patron,
    'valor_nominal5_ciclo1_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal5_ciclo1_lectura_IBC_ascenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal5_ciclo1_lectura_IBC_descenso_ajuste_a_0': mifolio.valor_nominal5_ciclo1_lectura_IBC_descenso - mifolio.desviacion_ciclo1_IBC,
    'valor_nominal5_ciclo2_lectura_patron_ascenso_ajuste_a_0': mifolio.valor_nominal5_ciclo2_lectura_patron_ascenso - mifolio.desviacion_ciclo2_patron,
    'valor_nominal5_ciclo2_lectura_IBC_ascenso_ajuste_a_0': mifolio.valor_nominal5_ciclo2_lectura_IBC_ascenso - mifolio.desviacion_ciclo2_IBC,

}

# Diccionario para almacenar los resultados
    resultados = {}

# Convertir los valores nominales según la unidad de medida
    for key, valor_nominal in valores_nominales.items():
      if unidades_toma_datos == "Lb*f/in2":
        resultado = round(valor_nominal * 6.89476, 8)
      elif unidades_toma_datos == "kg*f/cm2":
        resultado = round(valor_nominal * 98.0665, 8)
      elif unidades_toma_datos == "inH2O":
        resultado = round(valor_nominal * 0.2490889, 8)
      else:
        resultado = valor_nominal
      resultados[key] = resultado

# Crear un diccionario para almacenar los valores promedio por valor nominal
    promedios_por_valor_nominal = {}

# Iterar sobre el diccionario de resultados
    for key, value in resultados.items():
    # Verificar si la medida tiene "IBC" en el nombre y "_ajuste_a_0" al final
       if "IBC" in key and "_ajuste_a_0" in key:
        # Obtener el valor nominal
        valor_nominal = key.split('_')[1]
        # Verificar si el valor nominal ya está en el diccionario de promedios
        if valor_nominal not in promedios_por_valor_nominal:
            # Si no está, inicializar una lista con el valor actual
            promedios_por_valor_nominal[valor_nominal] = [value]
        else:
            # Si está, agregar el valor a la lista existente
            promedios_por_valor_nominal[valor_nominal].append(value)

# Calcular el promedio para cada valor nominal y almacenarlo en un nuevo diccionario
    promedios_finales = {}
    for valor_nominal, medidas in promedios_por_valor_nominal.items():
      promedio = sum(medidas) / len(medidas)
      promedios_finales[valor_nominal] = promedio

    resultados_con_presion_columna = {}

# Itera sobre los elementos del diccionario original
    for key, value in resultados.items():
    # Resta presion_columna al valor actual y almacena el resultado en el nuevo diccionario
        resultados_con_presion_columna[key] = value - presion_columna


#resultados de kpa inH2O para el error patron 
    resultados_inh2o_presion_colum = {}
    for key, value in resultados_con_presion_columna.items():
    # Resta presion_columna al valor actual y almacena el resultado en el nuevo diccionario
        resultados_inh2o_presion_colum[key] = value / 0.2490889








    error_patron = {}

# Itera sobre cada par clave-valor en el diccionario `resultados_con_presion_columna`
    for key, number in resultados_inh2o_presion_colum.items():
    # Calcula la expresión polinómica usando los coeficientes de la curva del patrón
        error_patron[key] = ((((number**10) * curva_patron.ca_x10) + ((number**9) * curva_patron.ca_x9) + ((number**8) * curva_patron.ca_x8) + ((number**7) * curva_patron.ca_x7) +
                      ((number**6) * curva_patron.ca_x6) + ((number**5) * curva_patron.ca_x5) + ((number**4) * curva_patron.ca_x4) + ((number**3) * curva_patron.ca_x3) +
                      ((number**2) * curva_patron.ca_x2) + (number * curva_patron.ca_x) + curva_patron.ca_B))*0.2490889
    
    correccion_temp= {}
    
    for key, number in resultados.items():
   # Convertir las cadenas a números flotantes si es necesario
        temperatura_amb_prom = float(temperatura_amb_prom)
        mifolio.coeficiente_termico = float(mifolio.coeficiente_termico)
        mifolio.temperatura_referencia_IBC = float(mifolio.temperatura_referencia_IBC)

# Realizar la operación corregida
        correccion_temp[key] = number * (1 + (mifolio.coeficiente_termico * (temperatura_amb_prom - mifolio.temperatura_referencia_IBC)))



# Crear un diccionario para almacenar los valores promedio por valor nominal
    promedios_lcp = {}

# Iterar sobre el diccionario de resultados
    for key, value in resultados_con_presion_columna.items():
       if "patron" in key and "_ajuste_a_0" in key:
        # Obtener el valor nominal
        valor_nominal = key.split('_')[1]
        # Verificar si el valor nominal ya está en el diccionario de promedios
        if valor_nominal not in promedios_lcp:
            # Si no está, inicializar una lista con el valor actual
            promedios_lcp[valor_nominal] = [value]
        else:
            # Si está, agregar el valor a la lista existente
            promedios_lcp[valor_nominal].append(value)

# Calcular el promedio para cada valor nominal y almacenarlo en un nuevo diccionario
    promedios_finales_lcp = {}
    for valor_nominal, medidas in promedios_lcp.items():
      promedio = sum(medidas) / len(medidas)
      promedios_finales_lcp[valor_nominal] = promedio
      
      
      # Crear un diccionario para almacenar los valores promedio por valor nominal
    promedios_lcetibc = {}

# Iterar sobre el diccionario de resultados
    for key, value in correccion_temp.items():
       if "IBC" in key and "_ajuste_a_0" in key:
        # Obtener el valor nominal
        valor_nominal = key.split('_')[1]
        # Verificar si el valor nominal ya está en el diccionario de promedios
        if valor_nominal not in promedios_lcetibc:
            # Si no está, inicializar una lista con el valor actual
            promedios_lcetibc[valor_nominal] = [value]
        else:
            # Si está, agregar el valor a la lista existente
            promedios_lcetibc[valor_nominal].append(value)

# Calcular el promedio para cada valor nominal y almacenarlo en un nuevo diccionario
    promedios_finales_lcetibc = {}
    for valor_nominal, medidas in promedios_lcetibc.items():
      promedio = sum(medidas) / len(medidas)
      promedios_finales_lcetibc[valor_nominal] = promedio
      
      promedios_ep = {}

# Iterar sobre el diccionario de resultados
    for key, value in error_patron.items():
       if "patron" in key and "_ajuste_a_0" in key:
        # Obtener el valor nominal
        valor_nominal = key.split('_')[1]
        # Verificar si el valor nominal ya está en el diccionario de promedios
        if valor_nominal not in promedios_ep:
            # Si no está, inicializar una lista con el valor actual
            promedios_ep[valor_nominal] = [value]
        else:
            # Si está, agregar el valor a la lista existente
            promedios_ep[valor_nominal].append(value)

# Calcular el promedio para cada valor nominal y almacenarlo en un nuevo diccionario
    promedios_finales_ep = {}
    for valor_nominal, medidas in promedios_ep.items():
      promedio = sum(medidas) / len(medidas)
      promedios_finales_ep[valor_nominal] = promedio
      
      
    E_values = {}
    for i in range(1, 6):  # Suponiendo que tienes 5 valores nominales
       nominal_key = f'nominal{i}'
       lcp = promedios_finales_lcp.get(nominal_key)
       lcetibc = promedios_finales_lcetibc.get(nominal_key)
       ep = promedios_finales_ep.get(nominal_key)
       E = lcetibc - (lcp - ep)
       E_values[nominal_key] = E
 # Crear un nuevo diccionario para almacenar los resultados de las restas
    histeresis_IBC = {}

# Iterar sobre el diccionario de valores nominales
    for key, value in correccion_temp.items():
    # Verificar si la clave contiene "IBC_ascenso" y "ciclo1"
       if "IBC_ascenso" in key and "ciclo1" in key:
        # Crear la clave correspondiente para "descenso"
           descenso_key = key.replace("ascenso", "descenso")
           if descenso_key in correccion_temp:
            # Realizar la resta y almacenar el resultado en el diccionario
            histeresis_IBC[key] = value - correccion_temp[descenso_key]
    histeresis_patron = {}

# Iterar sobre el diccionario de valores nominales
    for key, value in resultados_con_presion_columna.items():
    # Verificar si la clave contiene "IBC_ascenso" y "ciclo1"
       if "patron_ascenso" in key and "ciclo1" in key:
        # Crear la clave correspondiente para "descenso"
           descenso_key = key.replace("ascenso", "descenso")
           if descenso_key in resultados_con_presion_columna:
            # Realizar la resta y almacenar el resultado en el diccionario
            histeresis_patron[key] = value - resultados_con_presion_columna[descenso_key]
    
    incertidumbre_histererisis_ibc = {}
    
    for key, value in histeresis_IBC.items():
      incertidumbre_histererisis_ibc[key] = value/math.sqrt(12)
      

    incertidumbre_repetibilidad_IBC = {}
    for valor_nominal in range(1, 6):
        valores = [v for k, v in correccion_temp.items() if f'valor_nominal{valor_nominal}' in k and 'IBC' in k and '_ajuste_a_0' in k]
        suma = sum(valores)
        media = suma / len(valores)
        suma_cuadrados = sum((valor - media) ** 2 for valor in valores)
        desviacion = (math.sqrt(suma_cuadrados / (len(valores) - 1))) / math.sqrt(3)

        incertidumbre_repetibilidad_IBC[valor_nominal] = desviacion
    incertidumbre_cal_patron = {}

# Itera sobre cada par clave-valor en el diccionario `resultados_con_presion_columna`
    for key, number in promedios_finales_lcp.items():
    # Calcula la expresión polinómica usando los coeficientes de la curva del patrón
        incertidumbre_cal_patron[key] = ((((number**10) * curva_patron.ca_i_x10) + ((number**9) * curva_patron.ca_i_x9) + ((number**8) * curva_patron.ca_i_x8) + ((number**7) * curva_patron.ca_i_x7) +
                      ((number**6) * curva_patron.ca_i_x6) + ((number**5) * curva_patron.ca_i_x5) + ((number**4) * curva_patron.ca_i_x4) + ((number**3) * curva_patron.ca_i_x3) +
                      ((number**2) * curva_patron.ca_i_x2) + (number * curva_patron.ca_i_x) + curva_patron.ca_i_B))/2
    incertidumbre_repetibilidad_patron = {}

    for valor_nominal in range(1, 6):
    # Filtrar solo los valores correspondientes al valor nominal actual, lectura del patrón y ajuste a cero
       valores = [v for k, v in resultados_con_presion_columna.items() if f'valor_nominal{valor_nominal}' in k and 'lectura_patron' in k and 'ajuste_a_0' in k]
    
    # Calcular la media
       suma = round(sum(valores),6)
       media = round(suma / len(valores), 6)
    
    # Calcular la desviación estándar
       suma_cuadrados = round(sum((valor - media) ** 2 for valor in valores),6)
       desviacion = (math.sqrt(suma_cuadrados / (len(valores) - 1))) / math.sqrt(3)

       incertidumbre_repetibilidad_patron[valor_nominal] = desviacion
      
    max_key = max(histeresis_patron, key=histeresis_patron.get)
    max_value_hp = histeresis_patron[max_key]
 
    incertidumbre_hp =  (max_value_hp)/math.sqrt(12)
    
    u_total={
      'u_1': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[1]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal1']**2 +
    incertidumbre_repetibilidad_IBC[1]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal1_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
),
        'u_2': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[2]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal2']**2 +
    incertidumbre_repetibilidad_IBC[2]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal2_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
),
          'u_3': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[3]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal3']**2 +
    incertidumbre_repetibilidad_IBC[3]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal3_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
),  'u_4': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[4]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal4']**2 +
    incertidumbre_repetibilidad_IBC[4]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal4_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
),  'u_5': (math.sqrt(
    curva_patron.reproducibilidad**2 +
    u_PCOL**2 +
    incertidumbre_repetibilidad_patron[5]**2 +
    incertidumbre_deriva_0_patron**2 +
    incertidumbre_deriva_patron**2 +
    incertidumbre_curva_patron_error**2 +
    incertidumbre_curva_patron**2 +
    incertidumbre_cal_patron['nominal5']**2 +
    incertidumbre_repetibilidad_IBC[5]**2 +
    incertidumbre_hp**2 +
    incertidumbre_deriva_0**2 +
    incertidumbre_histererisis_ibc['valor_nominal5_ciclo1_lectura_IBC_ascenso_ajuste_a_0']**2 +
    incertidumbre_resolucion**2)
)
    }
    
    u_total_duplicado = {k: v * 2 for k, v in u_total.items()}
      
    context = {
        'incertidumbre_densidad_aire' : incertidumbre_densidad_aire,
        'densidad_aire':densidad_aire,
        'u_total_duplicado' : u_total_duplicado,
        'u_total' : u_total,
        'incertidumbre_hp' : incertidumbre_hp,
        'max_value_hp' : max_value_hp,
        'incertidumbre_repetibilidad_patron' : incertidumbre_repetibilidad_patron,
        'incertidumbre_cal_patron' : incertidumbre_cal_patron,
        'incertidumbre_repetibilidad_IBC' : incertidumbre_repetibilidad_IBC,
        'incertidumbre_histererisis_ibc':incertidumbre_histererisis_ibc,
        'histeresis_patron' : histeresis_patron,
        'histeresis_IBC' : histeresis_IBC,
        'E_values':E_values,
        'promedios_finales_ep':promedios_finales_ep,
        'promedios_finales_lcetibc':promedios_finales_lcetibc,
        'correccion_temp' : correccion_temp,
        'error_patron' : error_patron,
        'resultados_con_presion_columna':resultados_con_presion_columna,
        'promedios_finales':promedios_finales,
        'resultados': resultados,
        'presion_columna' : presion_columna,
        'gravedad_local': gravedad_local,
        'latitud' : latitud,
        'mifolio': mifolio,
        'temperatura_amb_prom':temperatura_amb_prom,
        'promedios_finales_lcp': promedios_finales_lcp,
        
        'curva' : curva_patron,
        'ca_x10': curva_patron.ca_x10,
        'ca_x9': curva_patron.ca_x9,
        'ca_x8': curva_patron.ca_x8,
        'ca_x7': curva_patron.ca_x7,
        'ca_x6': curva_patron.ca_x6,
        'ca_x5': curva_patron.ca_x5,
        'ca_x4': curva_patron.ca_x4,
        'ca_x3': curva_patron.ca_x3,
        'ca_x2': curva_patron.ca_x2,
        'ca_x': curva_patron.ca_x,
        'ca_B': curva_patron.ca_B,
        
        'ca_i_x10': curva_patron.ca_i_x10,
        'ca_i_x9': curva_patron.ca_i_x9,
        'ca_i_x8': curva_patron.ca_i_x8,
        'ca_i_x7': curva_patron.ca_i_x7,
        'ca_i_x6': curva_patron.ca_i_x6,
        'ca_i_x5': curva_patron.ca_i_x5,
        'ca_i_x4': curva_patron.ca_i_x4,
        'ca_i_x3': curva_patron.ca_i_x3,
        'ca_i_x2': curva_patron.ca_i_x2,
        'ca_i_x': curva_patron.ca_i_x,
        'ca_i_B': curva_patron.ca_i_B,
        'incertidumbre_curva_patron' : incertidumbre_curva_patron,
        'incertidumbre_curva_patron_error' : incertidumbre_curva_patron_error,
        'incertidumbre_resolucion' : incertidumbre_resolucion,
        'incertidumbre_deriva_0': incertidumbre_deriva_0,
        'incertidumbre_deriva_patron' : incertidumbre_deriva_patron,
        'incertidumbre_deriva_0_patron' : incertidumbre_deriva_0_patron,
        'u_gravedad_local' : u_gravedad_local,
        'u_diferencia_altura' : u_diferencia_altura,
        'u_PCOL':u_PCOL,
        'u_reproducibilidad': curva_patron.reproducibilidad,
        

    }
  
    return HttpResponse(template.render(context, request))




def patrones_presion_manometrica(request):
  misfolios = PatronesPresionManometrica.objects.all().values()
  template = loader.get_template('patrones_pm.html')
  context = {
    'misfolios': misfolios,
  }
  return HttpResponse(template.render(context, request))

def detalles_patrones_presion_manometrica(request, id):
    # Fetch data from your model
    instance = PatronesPresionManometrica.objects.get(id=id)

    # If the request is POST, it means the form has been submitted
    if request.method == 'POST':
        form = PatronesPresionManometricaForm(request.POST, instance=instance)
        if form.is_valid():
            # Perform the necessary actions with the submitted data, e.g., update the database
            form.save()
    else:
        form = PatronesPresionManometricaForm(instance=instance)

    # Convert model instance data to dictionary
    data_dict = {
        field.name: getattr(instance, field.name) for field in instance._meta.fields
    }

    # Convert dictionary to DataFrame
    data = pd.DataFrame([data_dict])

    # Render DataFrame as HTML table with editable fields
    html_table = data.to_html(classes='table table-striped', index=False, escape=False, 
                              render_links=False, table_id='editable_table')

    context = {
        'html_table': html_table,
        'form': form,
    }

    return render(request, 'detalles_patron_pm.html', context)

#calcular error patron  
