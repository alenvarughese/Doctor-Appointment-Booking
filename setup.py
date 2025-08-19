#!/usr/bin/env python3
"""
Setup script for the Doctor Appointment Booking System
This script helps initialize the Django project and create initial data.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None

def setup_backend():
    """Setup the Django backend"""
    print("Setting up Django backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("Backend directory not found. Please ensure you're in the project root.")
        return False
    
    os.chdir(backend_dir)
    
    # Check if virtual environment exists
    venv_dir = Path("venv")
    if not venv_dir.exists():
        print("Creating virtual environment...")
        result = run_command("python -m venv venv")
        if result is None:
            return False
    
    # Activate virtual environment and install requirements
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    print("Installing Python dependencies...")
    result = run_command(f"{pip_cmd} install -r requirements.txt")
    if result is None:
        return False
    
    print("Running Django migrations...")
    result = run_command(f"{pip_cmd} install django")
    if result is None:
        return False
    
    result = run_command("python manage.py makemigrations")
    if result is None:
        return False
    
    result = run_command("python manage.py migrate")
    if result is None:
        return False
    
    print("Creating superuser...")
    print("Please follow the prompts to create an admin user.")
    result = run_command("python manage.py createsuperuser")
    if result is None:
        print("Superuser creation failed. You can create one manually later.")
    
    print("Backend setup completed successfully!")
    return True

def setup_frontend():
    """Setup the React frontend"""
    print("Setting up React frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("Frontend directory not found. Please ensure you're in the project root.")
        return False
    
    os.chdir(frontend_dir)
    
    print("Installing Node.js dependencies...")
    result = run_command("npm install")
    if result is None:
        return False
    
    print("Frontend setup completed successfully!")
    return True

def main():
    """Main setup function"""
    print("Doctor Appointment Booking System - Setup Script")
    print("=" * 50)
    
    # Check if we're in the project root
    if not Path("backend").exists() or not Path("frontend").exists():
        print("Error: Please run this script from the project root directory.")
        print("Make sure both 'backend' and 'frontend' directories exist.")
        sys.exit(1)
    
    # Store original directory
    original_dir = os.getcwd()
    
    try:
        # Setup backend
        if not setup_backend():
            print("Backend setup failed!")
            sys.exit(1)
        
        # Return to original directory
        os.chdir(original_dir)
        
        # Setup frontend
        if not setup_frontend():
            print("Frontend setup failed!")
            sys.exit(1)
        
        print("\n" + "=" * 50)
        print("Setup completed successfully!")
        print("\nTo start the application:")
        print("1. Backend: cd backend && python manage.py runserver")
        print("2. Frontend: cd frontend && npm start")
        print("\nThe application will be available at:")
        print("- Backend: http://localhost:8000")
        print("- Frontend: http://localhost:3000")
        print("- Admin: http://localhost:8000/admin")
        
    except KeyboardInterrupt:
        print("\nSetup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Setup failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
