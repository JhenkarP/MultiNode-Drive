#distributed-file-system/server/temp_test.py
header = 'Matrices.pdf'

file_found = False

to_write = ''

with open('myIndex/index_temp.txt', 'r') as f:

    for line in f:

        # if filename already exists, update flag
        if line.rstrip('\n').rstrip('/') == header:

            line = line.rstrip('\n').rstrip('/') + '\n'

            file_found = True

        to_write += line

if not file_found:

    to_write += header + '\n'

with open('myIndex/index_temp.txt', 'w') as f:

    f.write(to_write)