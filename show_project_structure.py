import os
from dotenv import load_dotenv

load_dotenv()
root_dir = os.getenv('project_root_dir')


def print_clean_directory_structure(root, skip_dirs=('venv', 'data')):
    """
    Prints a tree of directories and files under root_dir without revealing root_dir name,
    skipping directories listed in skip_dirs.
    """
    skip_directories = ('.git', '.idea', '__pycache__') + skip_dirs

    for dirpath, dirnames, filenames in os.walk(root):
        # Remove unwanted dirs from traversal in-place
        dirnames[:] = [d for d in dirnames if d not in skip_directories]
        dirnames.sort()
        filenames.sort()

        # Compute relative path to hide root dir
        rel_path = os.path.relpath(dirpath, root)
        if rel_path == '.':
            rel_path = ''  # For root itself

        indent_level = rel_path.count(os.sep)
        indent = '    ' * indent_level

        # Print the directory name, but skip printing root itself
        if rel_path:
            print(f"{indent}[D] {os.path.basename(dirpath)}/")

        # Print files in the current directory
        for f in filenames:
            print(f"{indent}    [F] {f}")


if __name__ == '__main__':
    print_clean_directory_structure(root_dir)
