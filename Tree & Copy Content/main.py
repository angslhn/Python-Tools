import os
import sys

def compile_folder_contents(target_folder, allowed_extensions=None, output_filename="ContentFolder.txt"):
    if not os.path.exists(target_folder):
        print(f"Error: Folder '{target_folder}' tidak ditemukan.")
        return

    if allowed_extensions:
        allowed_extensions = [ext.replace('.', '').lower() for ext in allowed_extensions]

    output_abspath = os.path.abspath(output_filename)

    with open(output_filename, 'w', encoding='utf-8') as outfile:
        process_directory(target_folder, target_folder, outfile, output_abspath, allowed_extensions)
        
    print(f"\n[SUKSES] Semua isi file dari folder '{target_folder}' telah disalin ke '{output_filename}'")
    if allowed_extensions:
        print(f"Filter ekstensi yang diterapkan: {allowed_extensions}")

def process_directory(current_dir, base_dir, outfile, output_abspath, allowed_extensions):
    try:
        items = os.listdir(current_dir)
    except PermissionError:
        return 

    files = []
    dirs = []

    for item in items:
        item_path = os.path.join(current_dir, item)
        if os.path.isfile(item_path):
            _, ext = os.path.splitext(item)
            ext_clean = ext.replace('.', '').lower()

            if not allowed_extensions or ext_clean in allowed_extensions:
                files.append(item)
                
        elif os.path.isdir(item_path):
            dirs.append(item)

    files.sort()
    dirs.sort()

    for file in files:
        file_path = os.path.join(current_dir, file)
        
        if os.path.abspath(file_path) == output_abspath:
            continue

        rel_path = os.path.relpath(file_path, start=os.path.dirname(base_dir) or '.').replace('\\', '/')
        outfile.write(f"====== File [{rel_path}] ======\n")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as infile:
                content = infile.read()
                outfile.write(content)
                
                if not content.endswith('\n'):
                    outfile.write('\n')
        except UnicodeDecodeError:
            outfile.write("[File biner atau format non-teks dilewati]\n")
            
        outfile.write('\n')

    for d in dirs:
        dir_path = os.path.join(current_dir, d)
        process_directory(dir_path, base_dir, outfile, output_abspath, allowed_extensions)


def generate_tree(current_dir, allowed_extensions, outfile, prefix="", is_root=True):
    if is_root:
        outfile.write(f"{os.path.basename(os.path.abspath(current_dir))}/\n")
    
    try:
        items = os.listdir(current_dir)
    except PermissionError:
        return

    filtered_items = []
    for item in items:
        item_path = os.path.join(current_dir, item)
        if os.path.isdir(item_path):
            filtered_items.append(item)
        else:
            _, ext = os.path.splitext(item)
            ext_clean = ext.replace('.', '').lower()
            if not allowed_extensions or ext_clean in allowed_extensions:
                filtered_items.append(item)
                
    filtered_items.sort()
    count = len(filtered_items)

    for index, item in enumerate(filtered_items):
        item_path = os.path.join(current_dir, item)
        is_last = (index == count - 1)
        connector = "└── " if is_last else "├── "
        
        if os.path.isdir(item_path):
            outfile.write(f"{prefix}{connector}{item}/\n")
            extension = "    " if is_last else "│   "
            generate_tree(item_path, allowed_extensions, outfile, prefix + extension, is_root=False)
        else:
            outfile.write(f"{prefix}{connector}{item}\n")

def compile_tree_structure(target_folder, allowed_extensions=None, output_filename="TreeFolder.txt"):
    if not os.path.exists(target_folder):
        print(f"Error: Folder '{target_folder}' tidak ditemukan.")
        return
        
    if allowed_extensions:
        allowed_extensions = [ext.replace('.', '').lower() for ext in allowed_extensions]

    with open(output_filename, 'w', encoding='utf-8') as outfile:
        generate_tree(target_folder, allowed_extensions, outfile)
        
    print(f"\n[SUKSES] Struktur direktori dari '{target_folder}' telah dibuat di '{output_filename}'")
    if allowed_extensions:
        print(f"Filter ekstensi yang ditampilkan: {allowed_extensions}")


if __name__ == "__main__":
    # ==========================================
    # AREA KONFIGURASI (UBAH SESUAI KEBUTUHAN)
    # ==========================================
    TARGET_DIR = "src"  
    
    # Masukkan ekstensi tanpa titik, contoh: ['ts', 'sql', 'js', 'json']
    # Biarkan kosong [] jika ingin mengambil semua jenis file.
    INCLUDES_EXTENSION = ['ts', 'sql', 'tsx'] 
    # ==========================================
    
    if len(sys.argv) > 1:
        TARGET_DIR = sys.argv[1]

    print("====================================")
    print("        TOOL EKSTRAKSI FOLDER       ")
    print("====================================")
    print("Pilih mode eksekusi:")
    print("1. Tree Content (Buat struktur folder")
    print("2. Copy Content (Salin isi kode/file)")
    print("====================================")
    
    try:
        pilihan = input("Masukkan pilihan Anda (1/2): ").strip()
        
        if pilihan == '1':
            print(f"\nMembuat struktur Tree untuk folder: '{TARGET_DIR}' ...")
            compile_tree_structure(TARGET_DIR, INCLUDES_EXTENSION, "TreeFolder.txt")
        elif pilihan == '2':
            print(f"\nMemulai proses ekstraksi isi file pada folder: '{TARGET_DIR}' ...")
            compile_folder_contents(TARGET_DIR, INCLUDES_EXTENSION, "ContentFolder.txt")
        else:
            print("\nPilihan tidak valid. Silakan jalankan ulang script dan pilih 1 atau 2.")
    except KeyboardInterrupt:
        print("\n\nProses dibatalkan oleh pengguna.")