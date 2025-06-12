import difflib
import shutil
import os

# Dictionary of known magic bytes (File Signatures)
known_magic_bytes = {
    # Image Formats
    'PNG': b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A',
    'JPEG': b'\xFF\xD8\xFF',
    'GIF (87a)': b'\x47\x49\x46\x38\x37\x61',
    'GIF (89a)': b'\x47\x49\x46\x38\x39\x61',
    'BMP': b'\x42\x4D',

    # Document Formats
    'PDF': b'\x25\x50\x44\x46',
    'MS Office (Old, pre-2007)': b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1',
    'DOCX, PPTX, XLSX (Office Open XML)': b'\x50\x4B\x03\x04',

    # Archive Formats
    'ZIP': b'\x50\x4B\x03\x04',
    'GZIP': b'\x1F\x8B\x08',
    '7-Zip Archive': b'\x37\x7A\xBC\xAF\x27\x1C',
    'RAR Archive': b'\x52\x61\x72\x21\x1A\x07\x00',

    # Executable Formats
    'ELF Executable': b'\x7F\x45\x4C\x46',  # Linux Executable
    'Windows Executable (EXE/DLL)': b'\x4D\x5A',
    
    # Video & Audio Formats
    'RIFF (AVI/WAV)': b'\x52\x49\x46\x46',
    'MPEG Video': b'\x00\x00\x01\xBA',
    'MPEG Video': b'\x00\x00\x01\xB3',
    'MKV Video': b'\x1A\x45\xDF\xA3',
    'MP4 Video': b'\x66\x74\x79\x70',
    'OGG Audio': b'\x4F\x67\x67\x53',

    # Disk Images
    'ISO Disk Image': b'\x43\x44\x30\x30\x31',
    'FAT16 Boot Sector': b'\xEB\x3C\x90',
    'FAT32 Boot Sector': b'\x33\xC0\x8E\xD0\xBC\x00\x7C',
}

def main():
    print("===== Welcome to FileFixer =====")
    print("This program attempts to fix corrupted files by restoring their magic bytes.")
    print("You can let the program make an educated guess (Auto Mode) or manually specify the file type.")
    
    msg = ("1 for Auto Mode \n"
           "2 for Manual Mode \n"
           "3 to List Supported Types \n"
           "0 to Exit \n"
           "Enter the number of your choice: "
    )
    while (choice := input(msg).strip()) != "0":
        if choice == "1":
            auto_fix()
        elif choice == "2":
            manual_fix()
        elif choice == "3":
            list_file_types()
        else:
            print("Invalid input, try again.")

def list_file_types():
    """ Displays all supported file types. """
    print("Supported File Types:")
    for file_type in known_magic_bytes:
        print(f" - {file_type}")
    print()

def manual_fix():
    """ Allows user to manually choose a file type and apply the correct magic bytes. """
    target_path = input("Enter the full path of the file to fix: ").strip()
    
    if not os.path.exists(target_path):
        print("❌ Error: File not found.")
        return
    
    list_file_types()
    user_type_request = input("Enter the desired file type (case insensitive): ").strip().upper()

    # Find matching magic bytes
    if user_type_request not in known_magic_bytes:
        print("❌ Unknown file type. Try again.")

    apply_fix(target_path, known_magic_bytes[user_type_request], user_type_request)
    


def auto_fix():
    """ Automatically detects the closest matching file type and applies the fix. """
    target_path = input("\nEnter the full path of the file to fix: ").strip()

    if not os.path.exists(target_path):
        print("❌ Error: File not found.")
        return

    # Read first 16 bytes
    with open(target_path, "rb") as f:
        file_bytes = f.read(16)

    best_match = best_score = 0
    for file_type, magic in known_magic_bytes.items():
        similarity = difflib.SequenceMatcher(None, file_bytes[:len(magic)], magic).ratio()
        if similarity > best_score:
            best_match = (magic, file_type)
            best_score = similarity

    if best_match:
        new_magic_bytes, matched_type = best_match
        print(f"🔍 Closest match found: {matched_type}")
        apply_fix(target_path, new_magic_bytes, matched_type)
    else:
        print("❌ No close match found.")

def apply_fix(target_path, new_magic_bytes, file_type):
    """ Applies new magic bytes to a file and saves a backup """
    backup_path = target_path + ".bak"
    shutil.copy2(target_path, backup_path)  # Preserve original

    with open(target_path, "r+b") as f:
        f.write(new_magic_bytes)

    print(f"✔ Magic bytes updated to match {file_type}.")
    print(f"✔ Original file backed up as {backup_path}.")

# Run the program
if __name__ == "__main__":
    main()
