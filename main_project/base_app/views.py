# base_app/views.py
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .file_comparator import compare_files

def compare_files_view(request):
    true_file_path = None
    altered_file_path = None
    
    if request.method == 'POST':
        try:
            true_file = request.FILES['true_file']
            altered_file = request.FILES['altered_file']
            
            fs = FileSystemStorage()
            
            true_filename = fs.save(true_file.name, true_file)
            altered_filename = fs.save(altered_file.name, altered_file)
            
            true_file_path = fs.path(true_filename)
            altered_file_path = fs.path(altered_filename)
            
            report_file = 'report.txt'
            
            sentences_true, sentences_altered = compare_files(true_file_path, altered_file_path, report_file)
            
            return HttpResponse(f"Comparison report generated: <a href='{settings.MEDIA_URL}report.txt'>report.txt</a>")
        except KeyError:
            return HttpResponse("Error: Please provide both true and altered files.")
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")
    
    return render(request, 'compare_files.html', {'true_file_path': true_file_path, 'altered_file_path': altered_file_path})
