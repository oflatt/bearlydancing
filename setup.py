import pip

installed_packages = pip.get_installed_distributions()
flat_installed_packages = [package.project_name for package in installed_packages]
dependencies = ["pygame", "numpy", "cx-Freeze"]

def install(package):
    pip.main(['install', package])

for d in dependencies:
    if d in flat_installed_packages:
        print(d + " already installed")
    else:
        print("installing " + d)
        install(d)

print("good to go. bigbang.py in the src folder starts the game.")
