# upload/views.py
from django.shortcuts import render
from django.core.mail import send_mail
import pandas as pd
from .forms import UploadFileForm
from django.conf import settings

def handle_uploaded_file(file):
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
    else:
        raise ValueError("Unsupported file format")
    
    required_columns = ['Cust State', 'DPD']
    
    for column in required_columns:
        if column not in df.columns:
            raise KeyError(f"Required column '{column}' is missing in the uploaded file")
    
    summary = df.groupby(['Cust State', 'DPD']).size().reset_index(name='Count')
    return summary

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save()
            file = request.FILES['file']
            
            summary = handle_uploaded_file(file)
            email_subject = "Summary Report"
            email_body = summary.to_string(index=False)
                
            send_mail(
                    email_subject,
                    email_body,
                    'alpeshsodha2604@gmail.com',
                    ['tech@themedius.ai', 'hr@themedius.ai'],
                    fail_silently=False,
                )
                
            return render(request, 'data/summary.html', {'summary': summary.to_html(index=False)})
            
    else:
        form = UploadFileForm()
    return render(request, 'data/upload.html', {'form': form})


