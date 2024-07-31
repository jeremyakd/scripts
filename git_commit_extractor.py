import os
import re
import subprocess
from collections import defaultdict

# Directorio del repositorio Git
repo_dir = 'git_repo'

# Palabra o regex a buscar
search_term = r'word'

# Archivo de salida
output_file = '/home/user'

# Navegar al directorio del repositorio
os.chdir(repo_dir)

# Obtener el log de Git
git_log = subprocess.run(['git', 'log', '--all', '--pretty=format:%H'], capture_output=True, text=True)
commits = git_log.stdout.splitlines()[::-1]  # Invertir para ordenar de más antiguo a más nuevo

# Diccionario para contar las modificaciones de archivos
file_modifications = defaultdict(int)

with open(output_file, 'w', encoding='utf-8') as f:
    for commit in commits:
        # Obtener el diff de cada commit en formato binario
        git_diff = subprocess.run(['git', 'show', commit], capture_output=True)
        diff_text = git_diff.stdout.decode('utf-8', errors='ignore')  # Decodificar ignorando errores

        # Buscar el término en el diff
        if re.search(search_term, diff_text):
            # Escribir el diff en el archivo de salida
            f.write(diff_text)
            f.write('\n' + '-'*80 + '\n')  # Línea de separación

            # Obtener los archivos modificados en el commit
            git_show = subprocess.run(['git', 'show', '--name-only', '--pretty=format:', commit], capture_output=True, text=True)
            modified_files = git_show.stdout.splitlines()

            for file in modified_files:
                if file and 'migrations' not in file:  # Evitar líneas vacías y excluir migraciones
                    file_modifications[file] += 1

    # Ordenar los archivos modificados por la cantidad de veces editados, de mayor a menor
    sorted_files = sorted(file_modifications.items(), key=lambda x: x[1], reverse=True)

    # Escribir la lista de archivos modificados y la cantidad de veces editados al final del archivo
    f.write('\n' + '='*80 + '\n')
    f.write('Archivos modificados:\n')
    for file, count in sorted_files:
        f.write(f'{file}: {count}\n')

print(f'Archivo exportado a {output_file}')
