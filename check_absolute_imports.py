import ast
import os
import sys
import site
import importlib.util

PROJECT_ROOT = "src"
EXTENSIONS = (".py",)

# Все внешние библиотеки: из site-packages
SITE_PACKAGES_PATHS = site.getsitepackages() + [site.getusersitepackages()]

def is_third_party_module(module_name: str) -> bool:
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is None or not spec.origin:
            return False
        return any(path in spec.origin for path in SITE_PACKAGES_PATHS)
    except ModuleNotFoundError:
        return False

def is_stdlib_module(module_name: str) -> bool:
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is None or not spec.origin:
            return False
        return "lib" in spec.origin and "site-packages" not in spec.origin
    except ModuleNotFoundError:
        return False

def is_allowed_import(module_name: str) -> bool:
    root_module = (module_name or "").split(".")[0]
    return is_stdlib_module(root_module) or is_third_party_module(root_module)

def is_absolute_local_import(module: str) -> bool:
    return module.startswith(PROJECT_ROOT)

def check_imports(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=filepath)
        except SyntaxError:
            print(f"[!] {filepath}: syntax error")
            return False

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name
                if is_allowed_import(name):
                    continue
                if not is_absolute_local_import(name):
                    print(f"[!] {filepath}: non-absolute local import: import {name}")
                    return False

        elif isinstance(node, ast.ImportFrom):
            if node.level > 0:  # relative import — допустимо
                continue
            mod = node.module or ""
            if is_allowed_import(mod):
                continue
            if not is_absolute_local_import(mod):
                print(f"[!] {filepath}: non-absolute local import: from {mod} import ...")
                return False
    return True

def main():
    success = True
    for root, _, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith(EXTENSIONS):
                filepath = os.path.join(root, file)
                if not check_imports(filepath):
                    success = False
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
