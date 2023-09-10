from cx_Freeze import setup, Executable
import sys

base = None

if sys.platform == 'win32':
    base = None


executables = [Executable("main.py", base=base)]

packages = ["tkinter","tkcalendar","sqlite3","PIL","os"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "Diario de obra",
    options = options,
    version = "1.0",
    description = 'Software que o usuario pode armazenar o dia a dia de sua obra',
    executables = executables
)