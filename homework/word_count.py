"""Taller evaluable"""

# pylint: disable=broad-exception-raised

import glob
import os
import string
import time

# Crea la carpeta files/input

def initialize_input_directory(input_dir):
    if os.path.exists(input_dir):
        for file in glob.glob(f"{input_dir}/*"):
            os.remove(file)
    else:
        os.makedirs(input_dir)


initialize_input_directory("files/input")


def copy_raw_files_to_input_folder(n=5000):
    # Crea n copias de cada uno de los archivos en files/raw/
    for file in glob.glob("files/raw/*"):

        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        for i in range(1, n + 1):
            raw_filename_with_extension = os.path.basename(file)
            raw_filename_without_extension = os.path.splitext(raw_filename_with_extension)[
                0
            ]
            new_filename = f"{raw_filename_without_extension}_{i}.txt"
            with open(f"files/input/{new_filename}", "w", encoding="utf-8") as f2:
                f2.write(text)

copy_raw_files_to_input_folder(n=1000)

def run_job(input_path, output_path):
    start_time = time.time()


    # Lee los archivos de files/input
    sequence = []
    files = glob.glob(f"{input_path}/*")
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                sequence.append((file, line))


    # Mapea las líneas a pares (palabra, 1). Este es el mapper.
    pairs_sequence = []
    for _, line in sequence:
        line = line.lower()
        line = line.translate(str.maketrans("", "", string.punctuation))
        line = line.replace("\n", "")
        words = line.split()
        pairs_sequence.extend((word, 1) for word in words)

    # Ordena la secuencia de pares por la palabra. Este es el shuffle and sort.
    pairs_sequence = sorted(pairs_sequence)


    # Reduce la secuencia de pares sumando los valores por cada palabra. Este es el reducer.
    result = []
    for key, value in pairs_sequence:
        if result and result[-1][0] == key:
            result[-1] = (key, result[-1][1] + value)
        else:
            result.append((key, value))

    # Crea la carpeta files/output
    if os.path.exists(output_path):
        for file in glob.glob(f"{output_path}/*"):
            os.remove(file)
    else:
        os.makedirs(output_path)


    # Guarda el resultado en un archivo files/output/part-00000
    with open("files/output/part-00000", "w", encoding="utf-8") as f:
        for key, value in result:
            f.write(f"{key}\t{value}\n")


    # Crea el archivo _SUCCESS en files/output
    with open("files/output/_SUCCESS", "w", encoding="utf-8") as f:
        f.write("")

    # El experimento finaliza aquí.
    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")

run_job(
    "files/input",
    "files/output"
)