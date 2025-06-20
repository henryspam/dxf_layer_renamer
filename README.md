# Rename DXF Layer Names

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A small desktop tool with a graphical interface (GUI) to batch rename all layers in a DXF file by adding a custom prefix.

---

## ⚠️ Disclaimer

> ⚠️ **This program was created with the assistance of ChatGPT. It is provided for experimental and educational purposes only.**  
> The author does **not** accept any responsibility for data loss, incorrect modifications, or damages resulting from the use of this software.  
> **Use at your own risk.**

---

## 📦 Key Features

- ✅ Select a `.dxf` file through a file picker
- ✏️ Enter a custom prefix to apply to all layer names
- 🔍 Fully scans:
  - modelspace
  - layouts (paperspace)
  - blocks
- 🎨 Preserves all original layer properties:
  - color (`color`, `true_color`)
  - linetype
  - lineweight
  - transparency
  - plot flag
- 💾 Saves a new `.dxf` file with the prefix in the filename
- 📝 Generates a `.txt` log file listing all renamed layers

---
## 🪄 Executable File

👉 **[Download converti_nomi_layer_dxf_gui.exe](https://drive.google.com/file/d/1wVS19Bb9M8xsE76RAlHKbhMAp5W9s1Of/view?usp=drive_link)**  
No installation required – just download and run.

☕ Support the Project
If you found this tool useful and would like to support its development, consider buying me a coffee:
👉 [LINK](https://coff.ee/henry_9)

Thank you! ❤️

## 🖥️ Requirements

- Python 3.8 or higher
- [`ezdxf`](https://pypi.org/project/ezdxf/)

Install it using:

```bash
pip install ezdxf
