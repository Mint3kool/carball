import os
import shutil
from tempfile import mkstemp

import_statement = 'import '

def split_to_list(drive_and_path):
    path = os.path.splitdrive(drive_and_path)[1]
    folders = []
    while 1:
        path, folder = os.path.split(path)

        if folder != "":
            folders.append(folder)
        else:
            if path != "":
                folders.append(path)

            break

    folders.reverse()
    return folders


def get_deepness(top_level_dir, path_list):
    return len(path_list) - path_list.index(top_level_dir)


def analyze_file(deepness, path_data, file_path):
    replace_map = dict()
    fh, abs_path = mkstemp()
    with os.fdopen(fh, 'w') as new_file:
        with open(file_path, 'r') as old_file:
            lines = old_file.readlines()
            for i in range(len(lines)):
                line = lines[i]
                if line.startswith(import_statement) and import_statement +'sys' not in line:
                    cut_line = line[len(import_statement):].rstrip()
                    ending_string = cut_line[cut_line.rfind('.') + 1:]
                    replace_map[cut_line] = ending_string
                    line = 'from ' + '.' * deepness + cut_line[:cut_line.rfind(ending_string) - 1] + ' import ' + ending_string + '\n'
                else:
                    for key in replace_map:
                        line = line.replace(key, replace_map[key])
                new_file.write(line)
    os.remove(file_path)
    shutil.move(abs_path, file_path)
    print('fixed:', str(len(replace_map)), 'imports')


def prevent_leaks():
    top_level_dir = 'generated'
    current_dir = os.path.dirname(__file__)
    proto_dir = [x[0] for x in os.walk(current_dir) if top_level_dir in x[0] and '__pycache__' not in x[0]]

    path_lists = []
    for path in proto_dir:
        path_list = split_to_list(path)
        deepness = get_deepness(top_level_dir, path_list)
        left_over_paths = path_list[-deepness:]
        path_lists.append((path, deepness, left_over_paths))
    for path_item in path_lists:
        path = path_item[0]
        only_files = [(os.path.join(path, f), f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))
                      and '.py' in f and '__init__' not in f]
        for file in only_files:
            print('fixing file: ', file[1], end='\t')
            analyze_file(path_item[1], path_lists, file[0])


prevent_leaks()
