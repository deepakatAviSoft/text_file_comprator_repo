import difflib

def count_sentences(file_path):
    """
    Function to count the number of sentences in a given file.
    
    Parameters:
    - file_path: The path to the file to be processed.
    
    Returns:
    - The number of sentences in the file.
    """
    try:
        # Open the file in read mode
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the entire content of the file
            text = file.read()
            # Split the text into sentences based on the period (.)
            sentences = text.split('.')
            # Return the number of sentences
            return len(sentences)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return 0
    except Exception as e:
        print(f"An error occurred while processing file '{file_path}': {e}")
        return 0

def compare_files(true_file, altered_file, report_file):
    """
    Function to compare two text files and generate a report of the differences.
    
    Parameters:
    - true_file: The path to the original file.
    - altered_file: The path to the altered file.
    - report_file: The path to the file where the comparison report will be saved.
    
    Returns:
    - A tuple containing the number of sentences in the original and altered files, respectively.
    """
    try:
        # Open the original and altered files in read mode
        with open(true_file, 'r', encoding='utf-8') as true_f, open(altered_file, 'r', encoding='utf-8') as altered_f:
            # Read the entire content of both files
            true_text = true_f.read()
            altered_text = altered_f.read()

            # Split the text of each file into sentences based on the period (.)
            true_sentences = true_text.split('.')
            altered_sentences = altered_text.split('.')

            # Initialize an empty list to store the comparison report
            report = []
            # Iterate over the sentences in both files
            for i, (true_sent, altered_sent) in enumerate(zip(true_sentences, altered_sentences), start=1):
                # Create a SequenceMatcher object to find differences between sentences
                sm = difflib.SequenceMatcher(None, true_sent.strip().split(), altered_sent.strip().split())
                # Get words added to the altered sentence compared to the original
                added_words = [word for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag == 'insert' for word in altered_sent.strip().split()[j1:j2]]
                # Get words removed from the original sentence compared to the altered
                removed_words = [word for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag == 'delete' for word in true_sent.strip().split()[i1:i2]]
                # If there are added words, add them to the report
                if added_words:
                    report.append(f"Missing in sentence {i} (File1): {' '.join(added_words)}")
                # If there are removed words, add them to the report
                if removed_words:
                    report.append(f"Extra in sentence {i} (File2): {' '.join(removed_words)}")

            # Write the comparison report to the specified file
            with open(report_file, 'w', encoding='utf-8') as report_f:
                report_f.write('\n'.join(report))

            # Return the number of sentences in both files
            return len(true_sentences), len(altered_sentences)
    except FileNotFoundError:
        print(f"Error: One or more files not found.")
        return 0, 0
    except Exception as e:
        print(f"An error occurred while comparing files: {e}")
        return 0, 0

if __name__ == "__main__":
    # Define file paths
    true_file = 'true_file.txt'
    altered_file = 'altered_file.txt'
    report_file = 'report.txt'

    # Count sentences in each file
    sentences_count_true_file = count_sentences(true_file)
    sentences_count_altered_file = count_sentences(altered_file)

    # Print the number of sentences in each file
    print(f"Number of sentences in {true_file}: {sentences_count_true_file}")
    print(f"Number of sentences in {altered_file}: {sentences_count_altered_file}")

    # Compare files and generate a comparison report
    sentences1, sentences2 = compare_files(true_file, altered_file, report_file)

    # Print a message indicating that the comparison report has been generated
    print(f"Comparison report generated: {report_file}")
