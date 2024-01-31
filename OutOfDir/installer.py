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
import pyuac

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

def create_shortcut(file_path, shortcut_name):
    if os.name != 'nt':
        raise Exception('This function only works on Windows.')

    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    shortcut_path = os.path.join(desktop, f'{shortcut_name}.lnk')

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = file_path
    shortcut.save()

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
    global update_allowed
    new_update_allowed = input("New version available. Do you want to install it? This will overwrite your current version. (y/n) ")
    if new_update_allowed == 'y':
        update_allowed = True

def install_ui():
    global install_allowed
    global desktop_shortcut
    new_install_allowed = input(" Do you want to install this program? (y/n) ")
    if new_install_allowed == 'y':
        install_allowed = True

    new_install_allowed = input(" Do you want to make a desktop shortcut? (y/n) ")
    if new_install_allowed == 'n':
        desktop_shortcut = False

#Main
    
#Check if in program files
#If do the following
        
print(str(os.path.realpath(__file__)))

if is_child_of_program_files(os.path.realpath(__file__)):
    print(str(get_version()))
    if get_version() != None:
        #Get current version
        os.chdir(os.environ['LOCALAPPDATA'])
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
        os.chdir(os.environ['LOCALAPPDATA'] +'\\.' + repo)
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

    if install_allowed == True:
        print(get_program_files_directory())
        create_copy(get_program_files_directory() + '\\.' + repo)
        newpath = get_program_files_directory() + '\\.' + repo + '\\installer.py'

    if desktop_shortcut == True:
        create_shortcut(newpath, repo)

    appendings = [' --no-ui']
    if desktop_shortcut == False:
        appendings.append(' --no-d-s')

    if install_allowed == True:
        appendings.append(' --install-allowed')
        
    append_full = ''.join(appendings)

    if install_allowed == True:
        run_python_script_w_args(newpath, append_full)

    