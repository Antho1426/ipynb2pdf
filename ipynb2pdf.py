#!/usr/local/bin/python2.7


# ipynb2pdf.py


#==================
debugModeOn = False
#==================


## Setting the current working directory automatically
import os
project_path = os.getcwd() # getting the path leading to the current working directory
os.getcwd() # printing the path leading to the current working directory
os.chdir(project_path) # setting the current working directory based on the path leading to the current working directory


## Required packages
import os
import osascript # for displaying the Desktop notification
from pathlib import Path # for getting the parent directory of the Jupyter Notebook
from termcolor import colored # (pip install termcolor)
from argparse import ArgumentParser
from pandas.io.clipboard import clipboard_get # to access the string situated in the clipboard


## Parsing the input argument
if not debugModeOn:
    parser = ArgumentParser(description='"ipynb2pdf.py" is a Python program that\
        automatically converts a ".ipynb" Jupyter Notebook into a readable ".pdf" document.')
    parser.add_argument('--path', metavar='/path/to/ipynb/file', type=str, default='clipboard', help='convert the ".ipynb" file into a ".pdf" file')
    args = parser.parse_args()
    argsPath = args.path
else: # in case we are in "debug mode"
    argsPath = '".ipynb" file path required'


## Tests (clipboard_value examples)
# :-) Absolute file path of existing ".ipynb" file:
#argsPath = '/Users/anthony/MEGA/DOCUMENTS/Programmation/Python/MyPythonProjects/ConvertJupyterNotebookToPDF/tests/classifying_space_rocks.ipynb'
# :-) Absolute file path of existing ".ipynb" file:
#argsPath = project_path + '/tests/classifying_space_rocks.ipynb'
# :-) Absolute file path of nonexistent ".ipynb" file:
#argsPath = project_path + '/tests/tada.ipynb'
# :-) Absolute file path of NON ".ipynb" file:
#argsPath = project_path + '/tests/video_test.mov'


## Function

def notify(message, title, subtitle, sound):
    """
    Posts macOS X notification

    Args:
        message (str): The message
        title (str): The title
        subtitle (str): The subtitle
        sound (str): The macOS X sound
    """

    code, out, err = osascript.run('display notification "{0}" with title "{1}" subtitle "{2}" sound name "{3}"'.format(message, title, subtitle, sound))


## Main process

# Launching initial notification
notify(title='ipynb2pdf.py',
               subtitle='Running ipynb2pdf.py script',
               message='Conversion process started...',
               sound='Blow')


if argsPath == 'clipboard': # this is True (i.e. argsPath == 'clipboard') only if debugModeOn is set to "False"
    # 1) Retrieving stored clipboard value
    print('\n1) Retrieving stored clipboard value')
    clipboard_value = clipboard_get()
else:
    # 1) Retrieving the ".ipynb" file path argument
    print('\n1) Retrieving the ".ipynb" file path argument')
    clipboard_value = argsPath
print(' clipboard_value: {0}'.format(clipboard_value.encode('utf-8')))

if os.path.isfile(clipboard_value): # checking if the file exists on the computer (cf.: https://linuxize.com/post/python-check-if-file-exists/)

    if clipboard_value.endswith(".ipynb"): # checking if the file is effectively a ".ipynb" file

        try:

            # 2) Converting ".ipynb" to ".html" (cf.: https://github.com/jupyter/nbconvert)
            # (Example: jupyter nbconvert --to html my_file.ipynb)
            print('2) Converting ".ipynb" to ".html"')
            ipynb_file_path = clipboard_value
            os.system('jupyter nbconvert --to html {0}'.format(ipynb_file_path))

            # 3) Converting ".html" to ".pdf" (cf.: https://wkhtmltopdf.org)
            # (Example: wkhtmltopdf my_file.html my_file.pdf)
            print('3) Converting ".html" to ".pdf"')
            html_file_path = ipynb_file_path.replace('.ipynb', '.html')
            pdf_file_path = ipynb_file_path.replace('.ipynb', '.pdf')
            os.system('wkhtmltopdf {0} {1}'.format(html_file_path, pdf_file_path))

            # 4) Removing the useless ".html" file
            print('4) Removing the useless ".html" file')
            os.remove(html_file_path)

            # 5) Posting macOS X notification
            print('5) Posting macOS X notification\n')
            parent_directory = Path(pdf_file_path).parent
            notify(title='ipynb2pdf.py',
                   subtitle='Jupyter Notebook converted into PDF :-)',
                   message='The PDF file is available in {0}'.format(parent_directory),
                   sound='Hero')

        except Exception as e:
            colored_error_message = colored('A problem occurred while trying to convert ".ipynb" file into ".pdf" file...', 'red', attrs=['reverse', 'blink'])
            print(':-/ ERROR! ' + colored_error_message + '\n Error message:\n  {0}'.format(e))

            # Posting macOS X notification
            notify(title='ipynb2pdf.py',
                   subtitle='ERROR: Jupyter Notebook NOT converted into PDF :-(',
                   message='A problem occurred in the conversion of the Jupyter Notebook into PDF...',
                   sound='Sosumi')

    else:
        colored_error_message = colored('This is NOT the path of a ".ipynb" file...', 'red', attrs=['reverse', 'blink'])
        print(' :-/ ERROR! ' + colored_error_message)

        # Posting macOS X notification
        notify(title='ipynb2pdf.py',
               subtitle='ERROR: Jupyter Notebook NOT converted into PDF :-(',
               message='The file to convert is NOT a Jupyter Notebook...',
               sound='Sosumi')

else:
    colored_error_message = colored('The ".ipynb" file path does not exist...', 'red', attrs=['reverse', 'blink'])
    print(' :-/ ERROR! ' + colored_error_message)

    # Posting macOS X notification
    notify(title='ipynb2pdf.py',
           subtitle='ERROR: Jupyter Notebook NOT converted into PDF :-(',
           message='The Jupyter Notebook file path does not exist...',
           sound='Sosumi')

# Exiting the Terminal window in case the program has been triggered by Alfred
# (Cf.: How do I close the Terminal in OSX from the command line? (https://superuser.com/questions/158375/how-do-i-close-the-terminal-in-osx-from-the-command-line/1385450))
osascript.run('tell application "iTerm2" to close first window')