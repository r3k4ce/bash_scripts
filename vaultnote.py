#!/usr/bin/env python3
import os
import sys
import argparse
import shutil

def get_vault_root():
    vault = os.environ.get('VAULT_ROOT')
    if not vault:
        sys.exit("Error: VAULT_ROOT environment variable not set.")
    vault = os.path.expanduser(vault)
    if not os.path.isdir(vault):
        sys.exit(f"Error: VAULT_ROOT '{vault}' is not a directory.")
    return vault

def prompt_menu(current_path, include_files=False):
    """
    Simple numbered menu for directories (and files if include_files).
    Returns either:
      - new_path (str) if drilling into a subdir
      - 'UP' if user chose to go up
      - selected_file_path (str) if include_files=True and user picked a file
      - None if user quit
    """
    while True:
        entries = sorted(os.listdir(current_path))
        dirs = [e for e in entries if os.path.isdir(os.path.join(current_path, e))]
        files = [e for e in entries if include_files and os.path.isfile(os.path.join(current_path, e))]

        print(f"\nVault: {current_path}")
        for idx, d in enumerate(dirs, start=1):
            print(f" {idx}) {d}/")
        n_dirs = len(dirs)

        if include_files and files:
            for idx, f in enumerate(files, start=n_dirs+1):
                print(f" {idx}) {f}")

        print(" u) up   q) quit")
        choice = input("Select> ").strip().lower()
        if choice == 'q':
            return None
        if choice == 'u':
            return 'UP'
        if choice.isdigit():
            i = int(choice)
            if 1 <= i <= n_dirs:
                return os.path.join(current_path, dirs[i-1])
            if include_files and n_dirs < i <= n_dirs + len(files):
                return os.path.join(current_path, files[i-n_dirs-1])
        print("  ⛔ Invalid choice, try again.")

def navigate_to_target(vault_root, include_files=False):
    """
    Walk the vault tree until user either:
      - picks a directory (push mode, include_files=False)
      - picks a file   (pull mode, include_files=True)
    """
    path = vault_root
    first_prompt = True
    while True:
        # Always ask if user wants to paste here (push mode)
        if not include_files:
            if first_prompt or path != vault_root:
                confirm = input(f"Paste file into '{path}'? [Y/n] ").strip().lower()
                if confirm in ('', 'y', 'yes'):
                    return path
            first_prompt = False
        res = prompt_menu(path, include_files=include_files)
        if res is None:
            sys.exit("Aborted by user.")
        if res == 'UP':
            if os.path.abspath(path) == os.path.abspath(vault_root):
                print("🔙 Already at vault root.")
            else:
                path = os.path.dirname(path)
        else:
            if include_files and os.path.isfile(res):
                return res
            if os.path.isdir(res):
                path = res

def main():
    parser = argparse.ArgumentParser(
        description="vaultnote: push/pull notes to/from your vault"
    )
    parser.add_argument(
        "filename",
        nargs="?",
        help="(push) local file to copy INTO the vault"
    )
    args = parser.parse_args()

    vault_root = get_vault_root()

    if args.filename:
        # --- PUSH MODE ---
        src = os.path.abspath(args.filename)
        if not os.path.isfile(src):
            sys.exit(f"Error: source file '{src}' does not exist.")
        target_dir = navigate_to_target(vault_root, include_files=False)
        try:
            shutil.copy2(src, target_dir)
            print(f"\n✅ Copied '{src}' → '{target_dir}/'")
        except Exception as e:
            print(f"\n❌ Error copying: {e}")
            sys.exit(1)

    else:
        # --- PULL MODE ---
        file_in_vault = navigate_to_target(vault_root, include_files=True)
        dst = os.path.join(os.getcwd(), os.path.basename(file_in_vault))
        try:
            shutil.copy2(file_in_vault, dst)
            print(f"\n✅ Pulled '{file_in_vault}' → '{dst}'")
        except Exception as e:
            print(f"\n❌ Error pulling: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
