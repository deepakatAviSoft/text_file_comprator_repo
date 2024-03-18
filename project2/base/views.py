from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import difflib

def count_sentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        sentences = text.split('.')
        return len(sentences)

def compare_files(true_file, altered_file, report_file):
    with open(true_file, 'r', encoding='utf-8') as true_f, open(altered_file, 'r', encoding='utf-8') as altered_f:
        true_text = true_f.read()
        altered_text = altered_f.read()

        true_sentences = true_text.split('.')
        altered_sentences = altered_text.split('.')

        report = []
        for i, (true_sent, altered_sent) in enumerate(zip(true_sentences, altered_sentences), start=1):
            sm = difflib.SequenceMatcher(None, true_sent.strip().split(), altered_sent.strip().split())
            added_words = [word for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag == 'insert' for word in altered_sent.strip().split()[j1:j2]]
            removed_words = [word for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag == 'delete' for word in true_sent.strip().split()[i1:i2]]
            if added_words:
                report.append(f"Missing in sentence {i} (File1): {' '.join(added_words)}")
            if removed_words:
                report.append(f"Extra in sentence {i} (File2): {' '.join(removed_words)}")

        with open(report_file, 'w', encoding='utf-8') as report_f:
            report_f.write('\n'.join(report))

        return len(true_sentences), len(altered_sentences)

def compare_and_download(request):
    true_file = 'true_file.txt'
    altered_file = 'altered_file.txt'
    report_file = 'report.txt'

    sentences_count_true_file = count_sentences(true_file)
    sentences_count_altered_file = count_sentences(altered_file)

    comparison_report = compare_files(true_file, altered_file, report_file)

    with open(report_file, 'rb') as f:
        response = HttpResponse(f.read(), content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{report_file}"'
        return response

    return render(request, 'compare_result.html', {
        'sentences_count_true_file': sentences_count_true_file,
        'sentences_count_altered_file': sentences_count_altered_file,
        'report_file': report_file,
    })
