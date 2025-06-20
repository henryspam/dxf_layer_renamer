import ezdxf
import os
import tkinter as tk
from tkinter import filedialog, messagebox

INVALID_FILENAME_CHARS = r'<>:"/\\|?*'

def is_valid_prefix(prefix):
    return not any(char in prefix for char in INVALID_FILENAME_CHARS)

def rename_layers_full_scope(dxf_path, prefix):
    try:
        doc = ezdxf.readfile(dxf_path)
        renamed_layers = []

        # Spazi da esaminare: modelspace + layout + blocchi
        drawing_spaces = [doc.modelspace()] + list(doc.layouts)
        block_spaces = list(doc.blocks)

        for layer in list(doc.layers):
            old_name = layer.dxf.name
            if old_name == "0" or old_name.startswith(prefix):
                continue

            new_name = prefix + old_name

            # Crea nuovo layer con stesse proprietà
            if new_name not in doc.layers:
                new_layer = doc.layers.new(name=new_name)
                new_layer.dxf.color = layer.dxf.color
                if layer.dxf.hasattr('true_color'):
                    new_layer.dxf.true_color = layer.dxf.true_color
                new_layer.dxf.linetype = layer.dxf.linetype
                new_layer.dxf.lineweight = layer.dxf.lineweight
                new_layer.dxf.plot = layer.dxf.plot
                if layer.dxf.hasattr('transparency'):
                    new_layer.dxf.transparency = layer.dxf.transparency

            # Sposta entità in tutti gli spazi
            for space in drawing_spaces + block_spaces:
                for entity in space:
                    if entity.dxf.layer == old_name:
                        entity.dxf.layer = new_name

            try:
                doc.layers.remove(old_name)
                renamed_layers.append((old_name, new_name))
            except ValueError:
                pass

        base_name, ext = os.path.splitext(os.path.basename(dxf_path))
        new_file_name = f"{prefix}{base_name}{ext}"
        new_dxf_path = os.path.join(os.path.dirname(dxf_path), new_file_name)
        doc.saveas(new_dxf_path)

        # Log TXT
        log_file_name = f"{prefix}{base_name}_layer_changes.txt"
        log_path = os.path.join(os.path.dirname(dxf_path), log_file_name)
        with open(log_path, 'w', encoding='utf-8') as log:
            log.write(f"Layer changes for '{new_file_name}':\n\n")
            for old_name, new_name in renamed_layers:
                log.write(f"{old_name} → {new_name}\n")

        return new_dxf_path, log_path

    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante la conversione:\n{e}")
        return None, None

# GUI
def run_gui():
    def seleziona_file():
        file = filedialog.askopenfilename(filetypes=[("File DXF", "*.dxf")])
        if file:
            percorso_file.set(file)

    def avvia_conversione():
        path = percorso_file.get()
        pref = prefisso.get().strip()
        if not path:
            messagebox.showwarning("Attenzione", "Seleziona un file DXF.")
            return
        if not pref:
            messagebox.showwarning("Attenzione", "Inserisci un prefisso.")
            return
        if not is_valid_prefix(pref):
            messagebox.showerror("Errore", f"Il prefisso contiene caratteri non validi: {INVALID_FILENAME_CHARS}")
            return

        nuovo_file, log = rename_layers_full_scope(path, pref)
        if nuovo_file:
            messagebox.showinfo("Fatto", f"File convertito:\n{os.path.basename(nuovo_file)}\n\nLog creato:\n{os.path.basename(log)}")

    root = tk.Tk()
    root.title("Rinomina Layer DXF con Prefisso")

    percorso_file = tk.StringVar()
    prefisso = tk.StringVar()

    tk.Label(root, text="1. Seleziona un file DXF:").pack(anchor="w", padx=10, pady=(10, 0))
    tk.Entry(root, textvariable=percorso_file, width=60).pack(padx=10)
    tk.Button(root, text="Sfoglia...", command=seleziona_file).pack(padx=10, pady=5)

    tk.Label(root, text="2. Inserisci il prefisso da applicare:").pack(anchor="w", padx=10, pady=(10, 0))
    tk.Entry(root, textvariable=prefisso, width=30).pack(padx=10)

    tk.Button(root, text="Converti", command=avvia_conversione, bg="#4CAF50", fg="white").pack(pady=15)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
