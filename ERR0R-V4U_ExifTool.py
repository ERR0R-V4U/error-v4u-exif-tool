import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if not exif_data:
            return {}
        exif_details = {}
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            exif_details[tag] = value
        return exif_details
    except Exception as e:
        return {"error": str(e)}

def remove_exif(image_path, output_path):
    try:
        image = Image.open(image_path)
        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)
        image_without_exif.save(output_path)
        return True
    except Exception as e:
        return False

def main():
    print("""\n
    ███████╗██████╗ ██████╗ ██████╗  ██████╗ ██████╗ ██╗   ██╗
    ██╔════╝██╔══██╗╚════██╗╚════██╗██╔═████╗╚════██╗╚██╗ ██╔╝
    ███████╗██████╔╝ █████╔╝ █████╔╝██║██╔██║ █████╔╝ ╚████╔╝ 
    ╚════██║██╔═══╝ ██╔═══╝ ██╔═══╝ ████╔╝██║██╔═══╝   ╚██╔╝  
    ███████║██║     ███████╗███████╗╚██████╔╝███████╗   ██║   
    ╚══════╝╚═╝     ╚══════╝╚══════╝ ╚═════╝ ╚══════╝   ╚═╝   
          ERR0R-V4U EXIF TOOL | Extract & Remove Metadata
    """)

    image_path = input("👉 Enter image path: ")

    if not os.path.isfile(image_path):
        print("🚫 File not found.")
        return

    exif = get_exif_data(image_path)

    if not exif:
        print("ℹ️ No EXIF data found.")
    elif 'error' in exif:
        print(f"❌ Error: {exif['error']}")
    else:
        print("📸 EXIF Metadata:")
        for tag, value in exif.items():
            print(f" - {tag}: {value}")

    choice = input("\nDo you want to remove EXIF data? (y/n): ").strip().lower()
    if choice == 'y':
        output_file = input("👉 Enter output file name (e.g., output.jpg): ")
        if remove_exif(image_path, output_file):
            print(f"✅ EXIF removed. Saved as: {output_file}")
        else:
            print("❌ Failed to remove EXIF.")

if __name__ == '__main__':
    main()