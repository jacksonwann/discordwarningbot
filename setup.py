import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    print("Installing required packages...")
    install("discord.py")
    print("Installation complete!")

if __name__ == "__main__":
    main()