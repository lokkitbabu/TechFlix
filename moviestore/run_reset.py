import os
import shutil
import subprocess

PROJECT_APPS = ["movies"]
DJANGO_MANAGE = "python manage.py"

def delete_migrations():
    """Deletes all migration files except __init__.py and removes __pycache__."""
    for app in PROJECT_APPS:
        migration_dir = os.path.join(app, "migrations")
        if os.path.exists(migration_dir):
            for file in os.listdir(migration_dir):
                file_path = os.path.join(migration_dir, file)
                if file != "__init__.py":
                    if os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        print(f"Deleted directory: {file_path}")
                    else:
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")

def delete_cache():
    """Deletes all __pycache__ directories in the project."""
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                cache_path = os.path.join(root, dir_name)
                shutil.rmtree(cache_path)
                print(f"Deleted cache: {cache_path}")

def run_commands():
    """Runs Django migration and server commands."""
    commands = [
        f"{DJANGO_MANAGE} makemigrations",
        f"{DJANGO_MANAGE} migrate",
        f"{DJANGO_MANAGE} runserver"
    ]
    
    for command in commands:
        print(f"\n Running: {command}")
        subprocess.run(command, shell=True)

if __name__ == "__main__":
    print(" Resetting Django project...\n")
    delete_migrations()
    delete_cache()
    run_commands()
