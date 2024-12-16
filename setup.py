import os
import sys
import subprocess

def create_virtualenv(venv_name="env"):
    venv_dir = os.path.join(os.path.dirname(__file__), venv_name)
    
    if not os.path.isdir(venv_dir):
        print(f"creating virtual environment {venv_name}...")
        subprocess.check_call([sys.executable, '-m', 'venv', venv_dir])  # create venv
        print(f"virtual environment {venv_name} created successfully.")
    else:
        print(f"virtual environment {venv_name} already exists.")
    
    return venv_dir

def install_requirements(venv_dir):
    requirements = []
    
    # get requirements
    if sys.platform == "win32":
        requirements = ['flask', 'requests', 'pycryptodome', 'pywebview', 'nuitka']
    else:
        requirements = ['flask', 'requests', 'pycryptodome', 'pywebview[qt]']
    
    print("installing required packages...")
    # install pip packages
    subprocess.check_call([os.path.join(venv_dir, 'scripts' if sys.platform == "win32" else 'bin', 'pip'), 'install'] + requirements)
    print("requirements installed successfully.")

def build_project():
    if sys.platform == "win32":
        build_command = "nuitka --standalone --onefile --windows-console-mode=disable --windows-icon-from-ico=gui/assets/icon.ico --include-data-dir=gui=gui --include-data-dir=lib=lib main.py" 
    else:
        print("build command only available for windows; run as native python application. python main.py")  # no build for linux
        sys.exit()
    
    print(f"running build command: {build_command}")
    subprocess.check_call(build_command, shell=True)  # execute build
    print("build process completed successfully.")
    [shutil.rmtree(d) for d in ['main.build', 'main.dist', 'main.onefile-build'] if os.path.isdir(d)]


def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() == "build":
        build_project()  # build if 'build' argument
    else:
        venv_dir = create_virtualenv()  # create venv
        install_requirements(venv_dir)  # install requirements
    
        if sys.platform == "win32":
            print(f"virtual environment created and dependencies installed.\nto activate the environment, run:\n{venv_dir}\\scripts\\activate.bat")
        else:
            print(f"virtual environment created and dependencies installed.\nto activate the environment, run:\nsource {venv_dir}/bin/activate")  # linux activation

if __name__ == "__main__": main()
