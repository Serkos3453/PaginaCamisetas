import os
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


def comprimir_ultra(directorio_origen):
    for root, dirs, files in os.walk(directorio_origen):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                ruta_archivo = os.path.join(root, file)
                try:
                    with Image.open(ruta_archivo) as img:
                        img = img.convert("RGB")

                        # Bajamos a 500px (mucha diferencia de peso)
                        if img.width > 500:
                            proporcion = 500 / float(img.width)
                            alto = int((float(img.height) * float(proporcion)))
                            img = img.resize((500, alto), Image.Resampling.LANCZOS)

                        # Calidad 30% y sin perfiles de color/metadatos
                        img.save(ruta_archivo, "JPEG", optimize=True, quality=30, subsampling=0)
                        print(f"Ultra-comprimida: {file}")
                except Exception as e:
                    os.remove(ruta_archivo)  # Si está rota, mejor borrarla para ganar espacio
                    print(f"Borrada por corrupta: {file}")


if __name__ == "__main__":
    comprimir_ultra("./media/camisetas")