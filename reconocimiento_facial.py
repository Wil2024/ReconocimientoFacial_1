import os
import face_recognition
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Función para cargar imágenes de referencia para comparación y unificarlas por persona
def cargar_imagenes_referencia(ruta_carpeta):
    imagenes_referencia = {}
    for nombre_archivo in os.listdir(ruta_carpeta):
        ruta_imagen = os.path.join(ruta_carpeta, nombre_archivo)
        imagen = face_recognition.load_image_file(ruta_imagen)
        codificaciones = face_recognition.face_encodings(imagen)
        
        if codificaciones:
            codificacion = codificaciones[0]
            nombre = os.path.splitext(nombre_archivo)[0].split('_')[0]  # Supongamos que el nombre de la persona está antes de un guion bajo en el nombre del archivo
            if nombre in imagenes_referencia:
                imagenes_referencia[nombre].append(codificacion)
            else:
                imagenes_referencia[nombre] = [codificacion]
    
    return imagenes_referencia

# Función para comparar la imagen cargada con las de referencia unificadas
def comparar_imagen(ruta_imagen_cargada, imagenes_referencia):
    imagen_cargada = face_recognition.load_image_file(ruta_imagen_cargada)
    codificaciones_cargadas = face_recognition.face_encodings(imagen_cargada)
    
    if len(codificaciones_cargadas) > 0:
        codificacion_cargada = codificaciones_cargadas[0]
        for nombre, codificaciones in imagenes_referencia.items():
            coincidencias = face_recognition.compare_faces(codificaciones, codificacion_cargada)
            if True in coincidencias:
                return nombre
    
    return "Desconocido"

# Función para cargar y comparar una imagen
def cargar_y_comparar_imagen():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        resultado = comparar_imagen(file_path, imagenes_referencia)
        messagebox.showinfo("Resultado de Comparación", f"La persona en la imagen es: {resultado}")

# Crear la interfaz gráfica
def create_gui():
    root = tk.Tk()
    root.title("Comparación de Imágenes")
    root.geometry("400x200")

    label = tk.Label(root, text="Comparación de Imágenes", font=("Helvetica", 16))
    label.pack(pady=20)

    comparar_button = ttk.Button(root, text="Cargar y Comparar Imagen", command=cargar_y_comparar_imagen)
    comparar_button.pack(pady=10)

    root.mainloop()

# Ruta de la carpeta con imágenes de referencia
ruta_carpeta_referencia = "imagenes_base"

# Cargar imágenes de referencia
imagenes_referencia = cargar_imagenes_referencia(ruta_carpeta_referencia)

# Ejecutar la interfaz gráfica
if __name__ == "__main__":
    create_gui()
