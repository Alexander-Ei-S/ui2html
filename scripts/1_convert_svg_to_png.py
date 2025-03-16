import os
import cairosvg
from PIL import Image

input_dir = "dataset/raw_svg"
output_dir = "dataset/processed"
high_res_size = (512, 512)
target_size = (64, 64)

# Список класів (автовизначення з папок у raw_svg)
classes = [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]

if not classes:
    raise ValueError("❌ Помилка: У папці dataset/raw_svg відсутні піддиректорії з класами!")

print(f"🔍 Знайдено класи: {', '.join(classes)}")

for cls in classes:
    class_input_path = os.path.join(input_dir, cls)
    class_output_path = os.path.join(output_dir, cls)
    os.makedirs(class_output_path, exist_ok=True)
    
    # Отримання списку SVG-файлів
    svg_files = [f for f in os.listdir(class_input_path) if f.endswith(".svg")]
    if not svg_files:
        print(f"⚠️ Увага: У папці {cls} відсутні SVG-файли!")
        continue
    
    print(f"\n📁 Обробка класу '{cls}' ({len(svg_files)} файлів):")
    
    for i, svg_file in enumerate(svg_files, 1):
        input_path = os.path.join(class_input_path, svg_file)
        output_path = os.path.join(class_output_path, svg_file.replace(".svg", ".png"))
        temp_file = os.path.join(class_output_path, "temp_high_res.png")
        
        print(f"\n[{i}/{len(svg_files)}] Конвертація {svg_file}...")
        
        try:
            # Крок 1: Конвертація SVG -> тимчасовий PNG (512x512)
            cairosvg.svg2png(
                url=input_path,
                write_to=temp_file,
                output_width=high_res_size[0],
                output_height=high_res_size[1]
            )
            
            # Крок 2: Стиснення до цільового розміру
            with Image.open(temp_file) as img:
                img = img.resize(target_size, Image.Resampling.LANCZOS)
                img.save(output_path)
            
            os.remove(temp_file)
            print(f"✅ Успішно: {output_path}")
            
        except Exception as e:
            print(f"❌ Помилка: {str(e)}")
            if os.path.exists(temp_file):
                os.remove(temp_file)

print("\n🎉 Конвертація завершена! Перевірте папку dataset/processed.")