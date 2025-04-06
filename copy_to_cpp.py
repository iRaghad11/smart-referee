import os
import shutil

source_folder = r"C:\Users\Fajr2\OneDrive\سطح المكتب\smart_var"

destination_folder = os.path.join(source_folder, "cpp_files")
os.makedirs(destination_folder, exist_ok=True)

for filename in os.listdir(source_folder):
    old_path = os.path.join(source_folder, filename)

    if os.path.isfile(old_path):  
        new_filename = os.path.splitext(filename)[0] + ".cpp"
        new_path = os.path.join(destination_folder, new_filename)
        
        shutil.copy(old_path, new_path)  
        print(f"Copied: {filename} -> {new_filename}")

print("All files copied as .cpp successfully!")