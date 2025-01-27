
def sort_text_file(input_file, output_file):
    # Read the file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    sorted_lines = sorted(line.strip() for line in lines)

    # Write the sorted lines back to the output file
    with open(output_file, 'w') as file:
        for line in sorted_lines:
            file.write(line + '\n')

    print(f"File '{input_file}' sorted alphabetically and saved as '{output_file}'.")



input_file = "tagalog_lemmas.txt"  # Replace with your input file name
output_file = "tagalog_lemmas.txt"    # Replace with your output file name

sort_text_file(input_file, output_file)
