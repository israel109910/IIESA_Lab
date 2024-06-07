from django import forms
from .models import PresionManometrica
from .models import PatronesPresionManometrica
from .models import PresionDiferencial





class crearPresionManometricaForm(forms.ModelForm):
    class Meta:
        model = PresionManometrica
        fields = 'fecha_asignacion', 'responsable'
    
class EditarForm(forms.ModelForm):
    class Meta:
        model = PresionManometrica
        exclude = (
           "unidades_toma_datos", "desviacion_ciclo1_patron","desviacion_ciclo1_IBC",
            "desviacion_ciclo2_patron", "desviacion_ciclo2_IBC","valor_nominal1", "valor_nominal2", "valor_nominal3",
            "valor_nominal4","valor_nominal5","valor_nominal6","valor_nominal1_ciclo1_lectura_patron_ascenso","valor_nominal1_ciclo1_lectura_patron_descenso"
            ,"valor_nominal1_ciclo1_lectura_IBC_ascenso", "valor_nominal1_ciclo1_lectura_IBC_descenso", "valor_nominal1_ciclo2_lectura_patron_ascenso",
             "valor_nominal1_ciclo2_lectura_IBC_ascenso", 
            "valor_nominal2_ciclo1_lectura_patron_ascenso", "valor_nominal2_ciclo1_lectura_patron_descenso", "valor_nominal2_ciclo1_lectura_IBC_ascenso",
            "valor_nominal2_ciclo1_lectura_IBC_descenso","valor_nominal2_ciclo2_lectura_patron_ascenso", 
            "valor_nominal2_ciclo2_lectura_IBC_ascenso","valor_nominal3_ciclo1_lectura_patron_ascenso","valor_nominal3_ciclo1_lectura_patron_descenso",
            "valor_nominal3_ciclo1_lectura_IBC_ascenso", "valor_nominal3_ciclo1_lectura_IBC_descenso","valor_nominal3_ciclo2_lectura_patron_ascenso",
            "valor_nominal3_ciclo2_lectura_IBC_ascenso",  "valor_nominal4_ciclo1_lectura_patron_ascenso","valor_nominal4_ciclo1_lectura_patron_descenso",
            "valor_nominal4_ciclo1_lectura_IBC_ascenso","valor_nominal4_ciclo1_lectura_IBC_descenso","valor_nominal4_ciclo2_lectura_patron_ascenso",
            "valor_nominal4_ciclo2_lectura_IBC_ascenso", "valor_nominal5_ciclo1_lectura_patron_ascenso", "valor_nominal5_ciclo1_lectura_patron_descenso",
            "valor_nominal5_ciclo1_lectura_IBC_ascenso", "valor_nominal5_ciclo1_lectura_IBC_descenso","valor_nominal5_ciclo2_lectura_patron_ascenso",
            "valor_nominal5_ciclo2_lectura_IBC_ascenso"
            
  )
        
    fecha_recepcion = forms.DateField(
        label="Fecha Recepcion",
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
        input_formats=["%Y-%m-%d"]
    )
    fecha_calibracion = forms.DateField(
        label="Fecha de Calibracion",
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
        input_formats=["%Y-%m-%d"]
    )
    fecha_emision = forms.DateField(
        label="Fecha de Emision",
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
        input_formats=["%Y-%m-%d"]
    )
    fecha_entrega_IBC = forms.DateField(
        label="Fecha de Entrega IBC",
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
        input_formats=["%Y-%m-%d"]
    )
    
class TomaDatosManometricoForm(forms.ModelForm):
    class Meta:
        model = PresionManometrica
        fields = (
            "unidades_toma_datos", "desviacion_ciclo1_patron","desviacion_ciclo1_IBC",
            "desviacion_ciclo2_patron", "desviacion_ciclo2_IBC","valor_nominal1", "valor_nominal2", "valor_nominal3",
            "valor_nominal4","valor_nominal5","valor_nominal1_ciclo1_lectura_patron_ascenso","valor_nominal1_ciclo1_lectura_patron_descenso"
            ,"valor_nominal1_ciclo1_lectura_IBC_ascenso", "valor_nominal1_ciclo1_lectura_IBC_descenso", "valor_nominal1_ciclo2_lectura_patron_ascenso",
             "valor_nominal1_ciclo2_lectura_IBC_ascenso", 
            "valor_nominal2_ciclo1_lectura_patron_ascenso", "valor_nominal2_ciclo1_lectura_patron_descenso", "valor_nominal2_ciclo1_lectura_IBC_ascenso",
            "valor_nominal2_ciclo1_lectura_IBC_descenso","valor_nominal2_ciclo2_lectura_patron_ascenso", 
            "valor_nominal2_ciclo2_lectura_IBC_ascenso","valor_nominal3_ciclo1_lectura_patron_ascenso","valor_nominal3_ciclo1_lectura_patron_descenso",
            "valor_nominal3_ciclo1_lectura_IBC_ascenso", "valor_nominal3_ciclo1_lectura_IBC_descenso","valor_nominal3_ciclo2_lectura_patron_ascenso",
            "valor_nominal3_ciclo2_lectura_IBC_ascenso",  "valor_nominal4_ciclo1_lectura_patron_ascenso","valor_nominal4_ciclo1_lectura_patron_descenso",
            "valor_nominal4_ciclo1_lectura_IBC_ascenso","valor_nominal4_ciclo1_lectura_IBC_descenso","valor_nominal4_ciclo2_lectura_patron_ascenso",
            "valor_nominal4_ciclo2_lectura_IBC_ascenso", "valor_nominal5_ciclo1_lectura_patron_ascenso", "valor_nominal5_ciclo1_lectura_patron_descenso",
            "valor_nominal5_ciclo1_lectura_IBC_ascenso", "valor_nominal5_ciclo1_lectura_IBC_descenso","valor_nominal5_ciclo2_lectura_patron_ascenso",
            "valor_nominal5_ciclo2_lectura_IBC_ascenso"
            
  )
    
    
    
    
    
    
    
class crearPresionDiferencialForm(forms.ModelForm):
    class Meta:
        model = PresionDiferencial
        fields = 'fecha_asignacion', 'responsable'
    
class EditarFormPresionDiferencial(forms.ModelForm):
    class Meta:
        model = PresionDiferencial
        exclude = (
           "unidades_toma_datos", "desviacion_ciclo1_patron","desviacion_ciclo1_IBC",
            "desviacion_ciclo2_patron", "desviacion_ciclo2_IBC","valor_nominal1", "valor_nominal2", "valor_nominal3",
            "valor_nominal4","valor_nominal5","valor_nominal6","valor_nominal1_ciclo1_lectura_patron_ascenso","valor_nominal1_ciclo1_lectura_patron_descenso"
            ,"valor_nominal1_ciclo1_lectura_IBC_ascenso", "valor_nominal1_ciclo1_lectura_IBC_descenso", "valor_nominal1_ciclo2_lectura_patron_ascenso",
             "valor_nominal1_ciclo2_lectura_IBC_ascenso", 
            "valor_nominal2_ciclo1_lectura_patron_ascenso", "valor_nominal2_ciclo1_lectura_patron_descenso", "valor_nominal2_ciclo1_lectura_IBC_ascenso",
            "valor_nominal2_ciclo1_lectura_IBC_descenso","valor_nominal2_ciclo2_lectura_patron_ascenso", 
            "valor_nominal2_ciclo2_lectura_IBC_ascenso","valor_nominal3_ciclo1_lectura_patron_ascenso","valor_nominal3_ciclo1_lectura_patron_descenso",
            "valor_nominal3_ciclo1_lectura_IBC_ascenso", "valor_nominal3_ciclo1_lectura_IBC_descenso","valor_nominal3_ciclo2_lectura_patron_ascenso",
            "valor_nominal3_ciclo2_lectura_IBC_ascenso",  "valor_nominal4_ciclo1_lectura_patron_ascenso","valor_nominal4_ciclo1_lectura_patron_descenso",
            "valor_nominal4_ciclo1_lectura_IBC_ascenso","valor_nominal4_ciclo1_lectura_IBC_descenso","valor_nominal4_ciclo2_lectura_patron_ascenso",
            "valor_nominal4_ciclo2_lectura_IBC_ascenso", "valor_nominal5_ciclo1_lectura_patron_ascenso", "valor_nominal5_ciclo1_lectura_patron_descenso",
            "valor_nominal5_ciclo1_lectura_IBC_ascenso", "valor_nominal5_ciclo1_lectura_IBC_descenso","valor_nominal5_ciclo2_lectura_patron_ascenso",
            "valor_nominal5_ciclo2_lectura_IBC_ascenso"
            
  )
        
    fecha_recepcion = forms.DateField(
        label="Fecha Recepcion",
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
        input_formats=["%Y-%m-%d"]
    )
    fecha_calibracion = forms.DateField(
        label="Fecha de Calibracion",
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
        input_formats=["%Y-%m-%d"]
    )
    fecha_emision = forms.DateField(
        label="Fecha de Emision",
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
        input_formats=["%Y-%m-%d"]
    )
    fecha_entrega_IBC = forms.DateField(
        label="Fecha de Entrega IBC",
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}),
        input_formats=["%Y-%m-%d"]
    )
    
class TomaDatosPresionDiferencialForm(forms.ModelForm):
    class Meta:
        model = PresionDiferencial
        fields = (
            "unidades_toma_datos", "desviacion_ciclo1_patron","desviacion_ciclo1_IBC",
            "desviacion_ciclo2_patron", "desviacion_ciclo2_IBC","valor_nominal1", "valor_nominal2", "valor_nominal3",
            "valor_nominal4","valor_nominal5","valor_nominal1_ciclo1_lectura_patron_ascenso","valor_nominal1_ciclo1_lectura_patron_descenso"
            ,"valor_nominal1_ciclo1_lectura_IBC_ascenso", "valor_nominal1_ciclo1_lectura_IBC_descenso", "valor_nominal1_ciclo2_lectura_patron_ascenso",
             "valor_nominal1_ciclo2_lectura_IBC_ascenso", 
            "valor_nominal2_ciclo1_lectura_patron_ascenso", "valor_nominal2_ciclo1_lectura_patron_descenso", "valor_nominal2_ciclo1_lectura_IBC_ascenso",
            "valor_nominal2_ciclo1_lectura_IBC_descenso","valor_nominal2_ciclo2_lectura_patron_ascenso", 
            "valor_nominal2_ciclo2_lectura_IBC_ascenso","valor_nominal3_ciclo1_lectura_patron_ascenso","valor_nominal3_ciclo1_lectura_patron_descenso",
            "valor_nominal3_ciclo1_lectura_IBC_ascenso", "valor_nominal3_ciclo1_lectura_IBC_descenso","valor_nominal3_ciclo2_lectura_patron_ascenso",
            "valor_nominal3_ciclo2_lectura_IBC_ascenso",  "valor_nominal4_ciclo1_lectura_patron_ascenso","valor_nominal4_ciclo1_lectura_patron_descenso",
            "valor_nominal4_ciclo1_lectura_IBC_ascenso","valor_nominal4_ciclo1_lectura_IBC_descenso","valor_nominal4_ciclo2_lectura_patron_ascenso",
            "valor_nominal4_ciclo2_lectura_IBC_ascenso", "valor_nominal5_ciclo1_lectura_patron_ascenso", "valor_nominal5_ciclo1_lectura_patron_descenso",
            "valor_nominal5_ciclo1_lectura_IBC_ascenso", "valor_nominal5_ciclo1_lectura_IBC_descenso","valor_nominal5_ciclo2_lectura_patron_ascenso",
            "valor_nominal5_ciclo2_lectura_IBC_ascenso"
            
  )
    





        
class PatronesPresionManometricaForm(forms.ModelForm):
     class Meta:
        model = PatronesPresionManometrica
        fields = ['ca_x10', 'ca_x9', 'ca_x8','ca_x7', 'ca_x6', 'ca_x5','ca_x4', 'ca_x3', 'ca_x2','ca_x', 'ca_B', 'ca_residuales']  # Add fields you want to be editable in the form