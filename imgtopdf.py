import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import img2pdf
from PIL import Image
import os

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Imágenes a PDF")
        self.root.geometry("500x400")
        
        # Variables
        self.image_paths = []
        
        # Crear interfaz
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="Conversor de Imágenes a PDF", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Botón para seleccionar imágenes
        select_btn = ttk.Button(main_frame, text="Seleccionar Imágenes", 
                               command=self.select_images)
        select_btn.grid(row=1, column=0, pady=5, sticky=tk.W)
        
        # Botón para eliminar selección
        remove_btn = ttk.Button(main_frame, text="Eliminar Selección", 
                               command=self.remove_selected)
        remove_btn.grid(row=1, column=1, pady=5, sticky=tk.E)
        
        # Lista de imágenes seleccionadas
        self.listbox = tk.Listbox(main_frame, selectmode=tk.EXTENDED, height=10)
        self.listbox.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar para la lista
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.grid(row=2, column=2, sticky=(tk.N, tk.S))
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
        # Botones para mover imágenes en la lista
        move_frame = ttk.Frame(main_frame)
        move_frame.grid(row=3, column=0, columnspan=2, pady=5)
        
        up_btn = ttk.Button(move_frame, text="↑ Subir", command=self.move_up)
        up_btn.grid(row=0, column=0, padx=5)
        
        down_btn = ttk.Button(move_frame, text="↓ Bajar", command=self.move_down)
        down_btn.grid(row=0, column=1, padx=5)
        
        # Botón de conversión
        convert_btn = ttk.Button(main_frame, text="Convertir a PDF", 
                                command=self.convert_to_pdf, style="Accent.TButton")
        convert_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Configurar pesos de filas y columnas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Estilo para el botón principal
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 12, "bold"))
    
    def select_images(self):
        filetypes = (
            ("Imágenes", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
            ("Todos los archivos", "*.*")
        )
        
        paths = filedialog.askopenfilenames(
            title="Seleccionar imágenes",
            filetypes=filetypes
        )
        
        if paths:
            for path in paths:
                if path not in self.image_paths:
                    self.image_paths.append(path)
                    self.listbox.insert(tk.END, os.path.basename(path))
    
    def remove_selected(self):
        selected_indices = self.listbox.curselection()
        for index in selected_indices[::-1]:
            self.listbox.delete(index)
            self.image_paths.pop(index)
    
    def move_up(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            return
        
        for i in selected_indices:
            if i == 0:
                continue
            # Mover en la lista
            self.image_paths[i], self.image_paths[i-1] = self.image_paths[i-1], self.image_paths[i]
            # Mover en el listbox
            text = self.listbox.get(i)
            self.listbox.delete(i)
            self.listbox.insert(i-1, text)
        
        # Actualizar selección
        new_selection = [i-1 for i in selected_indices if i > 0]
        if new_selection:
            self.listbox.selection_set(new_selection[0], new_selection[-1])
    
    def move_down(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            return
        
        for i in selected_indices[::-1]:
            if i == self.listbox.size() - 1:
                continue
            # Mover en la lista
            self.image_paths[i], self.image_paths[i+1] = self.image_paths[i+1], self.image_paths[i]
            # Mover en el listbox
            text = self.listbox.get(i)
            self.listbox.delete(i)
            self.listbox.insert(i+1, text)
        
        # Actualizar selección
        new_selection = [i+1 for i in selected_indices if i < self.listbox.size() - 1]
        if new_selection:
            self.listbox.selection_set(new_selection[0], new_selection[-1])
    
    def convert_to_pdf(self):
        if not self.image_paths:
            messagebox.showwarning("Advertencia", "No hay imágenes seleccionadas.")
            return
        
        # Pedir ubicación para guardar el PDF
        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Guardar PDF como"
        )
        
        if not output_path:
            return
        
        try:
            # Convertir imágenes a PDF
            with open(output_path, "wb") as f:
                f.write(img2pdf.convert(self.image_paths))
            
            messagebox.showinfo("Éxito", f"PDF creado exitosamente:\n{output_path}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al crear el PDF:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToPDFConverter(root)
    root.mainloop()