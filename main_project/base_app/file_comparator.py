# base_app/file_comparator.py
import difflib

def count_sentences(file_path):
    """
    Count the number of sentences in a file.

    Args:
        file_path (str): The path to the file to count sentences in.

    Returns:
        int: The number of sentences in the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            sentences = text.split('.')
            return len(sentences)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return 0

def compare_files(true_file, altered_file, report_file):
    """
    Compare two files and generate a report of the differences.

    Args:
        true_file (str): The path to the original file.
        altered_file (str): The path to the altered file.
        report_file (str): The path to write the comparison report.

    Returns:
        tuple: A tuple containing the number of sentences in the original and altered files, respectively.
    """
    try:
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
                    report.append(f"Missing in sentence {i} in {true_file}: {' '.join(added_words)}")
                if removed_words:
                    report.append(f"Extra in sentence {i} in {true_file}: {' '.join(removed_words)}")

            with open(report_file, 'w', encoding='utf-8') as report_f:
                report_f.write('\n'.join(report))

            return len(true_sentences), len(altered_sentences)
    except FileNotFoundError:
        print("Error: One or more files not found.")
        return 0, 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0, 0
