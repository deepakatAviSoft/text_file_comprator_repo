# base_app/file_comparator.py
import difflib

def count_sentences(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            sentences = text.split('.')  # This splitting may not be robust
            return len(sentences)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return 0

def compare_files(true_file, altered_file, report_file):
    try:
        with open(true_file, 'r', encoding='utf-8') as true_f, open(altered_file, 'r', encoding='utf-8') as altered_f:
            true_text = true_f.read()
            altered_text = altered_f.read()

            # Split text into sentences more robustly
            true_sentences = true_text.split('\n')
            altered_sentences = altered_text.split('\n')

            # Compare sentences and generate report
            report = []
            for i, (true_sent, altered_sent) in enumerate(zip(true_sentences, altered_sentences), start=1):
                if true_sent != altered_sent:
                    report.append(f"Difference in sentence {i}:")
                    report.append(f"Original: {true_sent}")
                    report.append(f"Altered: {altered_sent}")

            # Write report to file
            with open(report_file, 'w', encoding='utf-8') as report_f:
                report_f.write('\n'.join(report))

            return len(true_sentences), len(altered_sentences)
    except FileNotFoundError:
        print("Error: One or more files not found.")
        return 0, 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0, 0
