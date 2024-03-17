# base_app/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .file_comparator import compare_files

def compare_files_view(request):
    if request.method == 'POST':
        true_file = request.FILES['true_file']
        altered_file = request.FILES['altered_file']
        
        # Assuming report_file is a fixed location for simplicity
        report_file = 'report.txt'
        
        sentences_true, sentences_altered = compare_files(true_file, altered_file, report_file)
        
        # Optionally, you can return some response or redirect to another page
        return HttpResponse("Comparison report generated: report.txt")
    else:
        return render(request, 'compare_files.html')
