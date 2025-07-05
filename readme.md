# Scripts & Workflow Tools

This repository is a collection of scripts and utilities designed to speed up and streamline my workflow. The idea is for this repository to grow over time as new scripts are added to solve tasks that I find annoying or repetitive.

## Purpose

The main goal of this repository is to provide a central place to store productiviy enhancers. Each script is self-contained and documented for easy use and extension.

---

## Scripts

### `vaultnote.py`

**Purpose:**

`vaultnote.py` is an interactive tool for copying files into and out of your personal knowledge vault (think Obsidian). It allows you to browse the vault's directory structure and select exactly where to paste or pull files, including any subdirectory or the vault root.

**Usage:**

- **Push a file into the vault:**
  ```bash
  vaultnote <filename>
  ```
  You will be prompted to browse the vault's folders and select a destination directory. You can paste the file at any level, including the root.

- **Pull a file from the vault:**
  ```bash
  vaultnote
  ```
  You will be prompted to browse the vault, select a file, and it will be copied to your current working directory.

**Environment Variable:**

- Set the location of your vault with (add to .bashrc for persistence):
  ```bash
  export VAULT_ROOT=YOUR_VAULT_ROOT

---

## Contributing

Feel free to add new scripts or suggest improvements to existing ones. The goal is to make this repository a living toolbox that can help in improving productivity.
