# dump your graham modules in this folder!

from os.path import dirname, basename, isfile, join, normpath
import glob
import imp

def load():
    module_paths = glob.glob(join(dirname(__file__), "*.py"))
    modules = []
    for path in module_paths:
        name = basename(normpath(path)).split(".")[0]
        if name != "__init__":
            try:
                modules.append(imp.load_source(name, path))
            except Exception as e:
                print("Module could not be loaded: "+name)
                print(e)
    return modules