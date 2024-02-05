import requests
import zipfile
import io
import github3
import os
import re
import shutil
import platform
import win32com.client
import sys
from pathlib import Path
from pyshortcuts import make_shortcut
import getpass
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

#Repo Info
owner = 'WhyFenceCode'
repo = 'AutoUpdaterTest'
pathtorun = 'main.py'

#Config Info
show_ui = True
desktop_shortcut = True
update_allowed = False
install_allowed = False

#Configure Config Info
for arg in sys.argv:
    if arg == '--no-ui':
        show_ui = False

    if arg == '--install-allowed':
        install_allowed = True

    if arg == '--no-d-s':
        desktop_shortcut = False

#UI
class install_window(QtWidgets.QDialog):

    def close_and_continue(self):
        global install_allowed
        install_allowed = True
        self.close()

    def change_stylesheet(self, button):
        # Reset all buttons to default style
        for btn in self.button_group.buttons():
            btn.setStyleSheet("""
                color:gray;
                font-size: 20px;
                font-weight: light;
                margin-left: 10px;
                margin-right: 10px;
                margin-bottom: 15px;
                margin-top: 15px;
                border-radius: 16px;
                padding-top: 20px;
                padding-bottom: 20px;
                padding-left: 10px;
                text-align: left;
            """)

        # Apply new style to selected button
        button.setStyleSheet("""
            color:gray;
            font-size: 20px;
            font-weight: light;
            background:rgb(48, 50, 76);
            margin-left: 10px;
            margin-right: 10px;
            margin-bottom: 15px;
            margin-top: 15px;
            border-radius: 16px;
            padding-top: 20px;
            padding-bottom: 20px;
            padding-left: 10px;
            text-align: left;
        """)

    def allow_shortcut(self):
        global desktop_shortcut
        desktop_shortcut = True
    
    def refuse_shortcut(self):
        global desktop_shortcut
        desktop_shortcut = False


    def __init__(self):
        super().__init__()

        w = 405
        h = 720

        # Set dialog size
        self.resize(w, h)
        # Remove frame
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)
        # Make the dialog transparent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Round widget
        self.round_widget = QtWidgets.QWidget(self)
        self.round_widget.resize(w, h)

        self.round_widget.setStyleSheet(
            """
            background:rgb(26, 28, 48);
            border-radius: 32px;
            """
        )

        # Layout setup (if needed)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.round_widget)

        self.button_group = QButtonGroup(self)
        self.button_group.buttonClicked.connect(self.change_stylesheet)
        

        wdg_layout = QtWidgets.QVBoxLayout()
        wdg_layout.setAlignment(QtCore.Qt.AlignTop)
        self.round_widget.setLayout(wdg_layout)

        install_text = QtWidgets.QLabel(self)
        install_text.setText("INSTALL")
        wdg_layout.addWidget(install_text)
        install_text.setFont(QFont('Calibri')) 
        install_text.setStyleSheet(
            """
            color:white;
            font-size: 36px;
            font-weight: normal;
            margin-left: 20px;
            margin-top: 40px;
            """
        )

        install_subtext = QtWidgets.QLabel(self)
        install_subtext.setText("PROGRAM WILL RUN AFTER")
        wdg_layout.addWidget(install_subtext)
        install_subtext.setFont(QFont('Calibri')) 
        install_subtext.setStyleSheet(
            """
            color:gray;
            font-size: 20px;
            font-weight: light;
            margin-left: 20px;
            margin-bottom: 90px;
            """
        )

        shortcut_on = QtWidgets.QPushButton("CREATE DESKTOP SHORTCUT")
        wdg_layout.addWidget(shortcut_on)
        shortcut_on.clicked.connect(self.allow_shortcut)
        self.button_group.addButton(shortcut_on, id=1)
        shortcut_on.setFont(QFont('Calibri')) 
        shortcut_on.setStyleSheet(
            """
            color:gray;
            font-size: 20px;
            font-weight: light;
            background:rgb(48, 50, 76);
            margin-left: 10px;
            margin-right: 10px;
            margin-bottom: 15px;
            margin-top: 15px;
            border-radius: 16px;
            padding-top: 20px;
            padding-bottom: 20px;
            padding-left: 10px;
            text-align: left;
            """
        )

        shortcut_off = QtWidgets.QPushButton("NO DESKTOP SHORTCUT")
        wdg_layout.addWidget(shortcut_off)
        shortcut_off.clicked.connect(self.refuse_shortcut)
        self.button_group.addButton(shortcut_off, id=2)
        shortcut_off.setFont(QFont('Calibri')) 
        shortcut_off.setStyleSheet(
            """
            color:gray;
            font-size: 20px;
            font-weight: light;
            margin-left: 10px;
            margin-right: 10px;
            margin-bottom: 15px;
            margin-top: 15px;
            border-radius: 16px;
            padding-top: 20px;
            padding-bottom: 20px;
            padding-left: 10px;
            text-align: left;
            """
        )

        go = QtWidgets.QPushButton("INSTALL")
        wdg_layout.addWidget(go)
        go.clicked.connect(self.close_and_continue)
        go.setFont(QFont('Calibri')) 
        go.setStyleSheet(
            """
            color:rgb(26, 28, 48);
            background:rgb(13, 245, 216);
            font-size: 20px;
            font-weight: light;
            margin-left: 35px;
            margin-right: 35px;
            margin-bottom: 15px;
            margin-top: 80px;
            border-radius: 16px;
            padding-top: 20px;
            padding-bottom: 20px;
            text-align: center;
            """
        )

        self.show()





class updates_window(QtWidgets.QDialog):

    def close_and_continue(self):
        global update_allowed
        update_allowed = True
        self.close()

    def __init__(self, version):
        super().__init__()

        w = 405
        h = 720

        # Set dialog size
        self.resize(w, h)
        # Remove frame
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)
        # Make the dialog transparent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Round widget
        self.round_widget = QtWidgets.QWidget(self)
        self.round_widget.resize(w, h)

        self.round_widget.setStyleSheet(
            """
            background:rgb(26, 28, 48);
            border-radius: 32px;
            """
        )

        # Layout setup (if needed)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.round_widget)
        

        wdg_layout = QtWidgets.QVBoxLayout()
        wdg_layout.setAlignment(QtCore.Qt.AlignTop)
        self.round_widget.setLayout(wdg_layout)

        update_text = QtWidgets.QLabel(self)
        update_text.setText("UPDATE")
        wdg_layout.addWidget(update_text)
        update_text.setFont(QFont('Calibri')) 
        update_text.setStyleSheet(
            """
            color:white;
            font-size: 36px;
            font-weight: normal;
            margin-left: 20px;
            margin-top: 40px;
            """
        )

        install_subtext = QtWidgets.QLabel(self)
        install_subtext.setText("PROGRAM WILL RUN AFTER")
        wdg_layout.addWidget(install_subtext)
        install_subtext.setFont(QFont('Calibri')) 
        install_subtext.setStyleSheet(
            """
            color:gray;
            font-size: 20px;
            font-weight: light;
            margin-left: 20px;
            margin-bottom: 90px;
            """
        )

        version_text = QtWidgets.QLabel(self)
        version_text.setText(str(version))
        wdg_layout.addWidget(version_text)
        version_text.setFont(QFont('Calibri')) 
        version_text.setStyleSheet(
            """
            color:gray;
            font-size: 20px;
            font-weight: light;
            background:rgb(48, 50, 76);
            margin-left: 10px;
            margin-right: 10px;
            margin-bottom: 50px;
            margin-top: 50px;
            border-radius: 16px;
            padding-top: 20px;
            padding-bottom: 20px;
            padding-left: 10px;
            text-align: left;
            """
        )

        go = QtWidgets.QPushButton("UPDATE")
        wdg_layout.addWidget(go)
        go.clicked.connect(self.close_and_continue)
        go.setFont(QFont('Calibri')) 
        go.setStyleSheet(
            """
            color:rgb(26, 28, 48);
            background:rgb(13, 245, 216);
            font-size: 20px;
            font-weight: light;
            margin-left: 35px;
            margin-right: 35px;
            margin-bottom: 15px;
            margin-top: 80px;
            border-radius: 16px;
            padding-top: 20px;
            padding-bottom: 20px;
            text-align: center;
            """
        )

        self.show()

#Test Config Info
print(f'Show UI: {show_ui}')
print(f'Desktop Shortcut: {desktop_shortcut}')

#Helper Functions
def get_online_version(owner, repo):
    try:
        gh = github3.GitHub()
        repo = gh.repository(owner, repo)
        file = repo.file_contents('manifest.txt')
        file_content = file.decoded.decode('utf-8')

        for line in file_content.split('\n'):
            if line.startswith('version='):
                return line.split('=')[1]
    except:
        return None
    
def download_and_extract_repo(owner, repo, folder_name):
    url = f'https://github.com/{owner}/{repo}/archive/refs/heads/main.zip'
    response = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(response.content))
    z.extractall('.')
    
    os.rename(repo + '-main', folder_name)

def get_version():
    try:
        with open('.//manifest.txt', 'r') as f:
            content = f.read()
            match = re.search(r'version=(.*)', content)
            if match:
                return match.group(1)
            else:
                return None
    except:
        return None
    
def create_folder(folder_name):
    folder = Path(folder_name)
    if folder.exists():
        shutil.rmtree(str(folder))
        print(f"Folder '{folder_name}' has been removed.")
    folder.mkdir()
    print(f"Folder '{folder_name}' has been created.")
    
def delete_folders(folders_to_keep):
    path = os.getcwd()
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    for dir in dirs:
        if dir not in folders_to_keep and is_child_of_program_files(os.path.join(path, dir)) == True:
            shutil.rmtree(os.path.join(path, dir))
    
def change_version(new_version):
    try: 
        with open('manifest.txt', 'r+') as f:
            content = f.read()
            new_content = re.sub(r'(version=)(.*)', r'\g<1>' + new_version, content)
            f.seek(0)
            f.write(new_content)
            f.truncate()
    except:
        with open('manifest.txt', 'w') as f:
            stuff = ('repo=' + repo, 'version=' + new_version, 'author=' + owner)
            result = '\n'.join(stuff)
            f.write(result)

def get_os_type():
    return platform.system()

def get_program_files_directory():
    if os.name == 'nt': # Windows
        return os.environ['LOCALAPPDATA']
    elif os.name == 'posix': # Linux or MacOS
        return '/usr/local/bin'
    else:
        raise OSError('Unsupported OS')

def run_python_script(script_path):
    try:
        os.system(f'python ' + os.environ['LOCALAPPDATA'] + '\\.' + repo + '\\' + script_path)
    except:
        print(f'python {script_path} does not exist.')

def run_python_script_w_args(script_path, args):
    if not os.path.isfile(script_path):
        raise FileNotFoundError(f"The file {script_path} does not exist.")

    print(f'python {script_path + args}')
    os.system(f'python {script_path + args}')

def create_shortcut(python_file, name):
    # Get the user's desktop path
    username = getpass.getuser()
    desktop_path = f"C:\\Users\\{username}\\Desktop"

    # Create the shortcut
    make_shortcut(python_file, name=name)


def create_copy(destination_path):
    old_path = os.getcwd()
    os.chdir(os.environ['LOCALAPPDATA'])
    create_folder('.' + repo)
    os.chdir(old_path)

    # Copy the current script to the destination path
    current_script_path = os.path.realpath(__file__)
    print(current_script_path)
    copied_script_path = os.path.join(destination_path, os.path.basename(current_script_path))
    print(copied_script_path)
    shutil.copy2(current_script_path, copied_script_path)


def is_child_of_program_files(path):
    p = Path(path)
    u = Path(get_program_files_directory())
    if u in p.parents:
        return True
    else:
        return False

def delete_current_script():
    script_path = os.path.realpath(__file__)
    os.remove(script_path)

def update_ui():
    app = QtWidgets.QApplication([])
    #win = install_window()
    win = updates_window(get_online_version(owner, repo))
    app.exec()

def install_ui():
    app = QtWidgets.QApplication([])
    win = install_window()
    #win = updates_window(get_online_version(owner, repo))
    app.exec()

#Main
    
#Check if in program files
#If do the following
        
print(str(os.path.realpath(__file__)))

if is_child_of_program_files(os.path.realpath(__file__)):
    os.chdir(os.environ['LOCALAPPDATA'] +'\\.' + repo)
    print(str(get_version()))
    if get_version() != None:
        #Get current version
        current_version = get_version()

        #Get online version
        online_version = get_online_version(owner, repo)

        if current_version != online_version and online_version is not None:
            update_ui()
            if update_allowed == True:
                download_and_extract_repo(owner, repo, online_version)
                change_version(online_version)
                delete_folders([online_version, 'installer.py', 'manifest.txt', 'userData', repo])

        current_version = get_version()

        run_python_script(current_version + '\\' + pathtorun)
    else:
        if show_ui == True:
            print("In Program Files")
            install_ui()

        if install_allowed == True:
            online_version = get_online_version(owner, repo)
            download_and_extract_repo(owner, repo, online_version)
            change_version(online_version)
            delete_folders([online_version, 'installer.py', 'manifest.txt', 'userData', repo])

        else:
            sys.exit()

        current_version = get_version()

        run_python_script(current_version + '\\' + pathtorun)

else:
    if show_ui == True:
        install_ui()
    else:
        sys.exit()
        
    print(install_allowed)

    if install_allowed == True:
        print(get_program_files_directory())
        create_copy(get_program_files_directory() + '\\.' + repo)
        newpath = get_program_files_directory() + '\\.' + repo + '\\installer.py'

    if desktop_shortcut == True and install_allowed == True:
        create_shortcut(newpath, repo)

    appendings = [' --no-ui']
    if desktop_shortcut == False:
        appendings.append(' --no-d-s')

    if install_allowed == True:
        appendings.append(' --install-allowed')
        
    append_full = ''.join(appendings)

    if install_allowed == True:
        run_python_script_w_args(newpath, append_full)
        delete_current_script()

    