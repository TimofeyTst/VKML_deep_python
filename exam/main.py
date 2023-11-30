import threading

def process_file(input_file, output_template, k):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    threads = []
    for i in range(k):
        output_file = f"{output_template}_{i + 1}.txt"
        current_lines = lines[i::k]

        thread = threading.Thread(target=write_to_file, args=(output_file, current_lines))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def write_to_file(output_file, lines):
    with open(output_file, 'w') as file:
        file.writelines(lines)

input_filename = 'input.txt'
output_template = 'output_file'
k = 2

process_file(input_filename, output_template, k)
