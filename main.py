from glob import glob
import sys
from PyPDF2 import PdfFileMerger
import argparse
from natsort import natsorted

parser = argparse.ArgumentParser(description='Pdf merge tool.')

def get_pdf_file_names(recursive: bool) -> list:
    file_names = list()
    dir = ''

    if (recursive):
        dir = '**/*.pdf'
    else:
        dir = '*.pdf'

    for file in glob(dir):
        file_names.append(file)

    return natsorted((file_names))

def main(*args):
    parser.add_argument('--all', required=False, default='y', help='y / n: An option to merge with files in subdirectories. Default is "y".')

    args = parser.parse_args()
    subdir_arg = args.all.lower()

    if (subdir_arg != 'y' and subdir_arg != 'n'):
        print('Please check the option. Use command below.')
        print('python pdf_merge.py -h')

    with_subdirs = subdir_arg == 'y'

    print('Trying to find pdf files...')
    print()
    
    file_names = get_pdf_file_names(with_subdirs)

    if (len(file_names) < 2):
        print("There's no pdf files to merge in this dir.")
        return

    print('These files below will be merged.')
    for file in file_names:
        print(f'- {file}')
    print()

    merger = PdfFileMerger()
    for pdf in file_names:
        print(f'Processing with file: {pdf}')
        merger.append(pdf)
    print()

    merged_file_name = f'MERGED_{file_names[0]}'
    splitted = merged_file_name.split(('/'))
    new_file_name = '[MERGED]' + splitted[len(splitted) - 1]

    print('Merging files...')
    print()

    merger.write(new_file_name)
    merger.close()

    print(f'PDF MERGE DONE with file: {new_file_name}')
    print()


if __name__ == "__main__":
    main(sys.argv)