import subprocess
import sys

print("Cleaning previous dist folder...")
subprocess.run(["rm", "-rf", "dist"], check=True)

subprocess.run([
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--name", "spanshan",
    "main.py"
], check=True)

print("Copying nuget_restore...")
subprocess.run(["cp", "-r", "nuget_restore", "./dist/"], check=True)

print("Copying extensions...")
subprocess.run(["cp", "-r", "extensions", "./dist/"], check=True)