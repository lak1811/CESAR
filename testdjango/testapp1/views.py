
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render, redirect
from .forms import FileUploadForm
from . import views
from .dash_app import appen
from .main import main
from .extrafuns import ss,ff,iint,fun_result,fun_uppercase,fun_idd_unixwind,fun_nomeppg,fun_ppgs,fun_peso_defesa,fun_indori_classif,fun_indprodart_classif
import zipfile
from django.conf import settings
import os
def index(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_zip = form.save()
            zip_folder_path = os.path.join(settings.MEDIA_ROOT, str(uploaded_zip.file))
            main(zip_folder_path)
        
            
            return redirect('dash_view')  # Redirect to a success page
    else:
        form = FileUploadForm()
    return render(request, 'testapp1/index.html', {'form': form})

def dash_view(request):
    
    
    redirect_url = 'http://127.0.0.1:8051/'
    return redirect(redirect_url)
