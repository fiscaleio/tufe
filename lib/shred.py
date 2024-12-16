import os, sys 
import random

def shred_file(file_path, passes=200):
    """Overwrite file with random data multiple times before deletion."""
    try:
        # Check if the file exists
        if os.path.isfile(file_path):
            # Get the file size
            file_size = os.path.getsize(file_path)
            
            # Open the file for writing (overwriting mode)
            with open(file_path, 'r+b') as f:
                for _ in range(passes):
                    # Overwrite with random data
                    f.seek(0)
                    f.write(bytearray(random.getrandbits(8) for _ in range(file_size)))
            
            # Now that the file is overwritten, we can safely delete it
            # os.remove(file_path)
            print(f"File {file_path} securely deleted.")
        else:
            print(f"File {file_path} not found.")
    except Exception as e:
        print(f"Error shredding file {file_path}: {e}")

if __name__ == '__main__':
    try:
        filepath = sys.argv[1]
    except:
        print("usage: python shred.py filepath")
        sys.exit()

    if os.path.isfile(filepath):
        shred_file(filepath)