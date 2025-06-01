import os
import json
import requests
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def banner():
    print(r"""
███████╗██████╗  ██████╗  ██████╗ ██████╗     ███████╗██╗  ██╗██╗███████╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔════╝██╔══██╗██╔═══██╗██╔═══██╗██╔══██╗    ██╔════╝╚██╗██╔╝██║██╔════╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
█████╗  ██████╔╝██║   ██║██║   ██║██████╔╝    █████╗   ╚███╔╝ ██║█████╗         ██║   ██║   ██║██║   ██║██║     ███████╗
██╔══╝  ██╔══██╗██║   ██║██║   ██║██╔══██╗    ██╔══╝   ██╔██╗ ██║██╔══╝         ██║   ██║   ██║██║   ██║██║     ╚════██║
███████╗██║  ██║╚██████╔╝╚██████╔╝██║  ██║    ███████╗██╔╝ ██╗██║██║            ██║   ╚██████╔╝╚██████╔╝███████╗███████║
╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝╚═╝╚═╝            ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
                                                                                                                         
   🔍 EXIF DATA EXTRACTOR & CLEANER TOOL
         BY: ERR0R-V4U 🧠
""")

def extract_exif(image_path):
    image = Image.open(image_path)
    info = image._getexif()
    exif_data = {}
    if info:
        for tag, value in info.items():
            tag_name = TAGS.get(tag, tag)
            exif_data[tag_name] = value
    return exif_data

def get_gps_info(exif_data):
    gps_info = exif_data.get("GPSInfo", {})
    gps_data = {}
    if gps_info:
        for key in gps_info.keys():
            decoded = GPSTAGS.get(key, key)
            gps_data[decoded] = gps_info[key]

        def convert_to_degrees(value):
            try:
                d = value[0][0] / value[0][1]
                m = value[1][0] / value[1][1]
                s = value[2][0] / value[2][1]
            except TypeError:
                d = float(value[0])
                m = float(value[1])
                s = float(value[2])
            return d + (m / 60.0) + (s / 3600.0)

        if "GPSLatitude" in gps_data and "GPSLatitudeRef" in gps_data:
            lat = convert_to_degrees(gps_data["GPSLatitude"])
            if gps_data["GPSLatitudeRef"] != "N":
                lat = -lat
            gps_data["Latitude"] = lat

        if "GPSLongitude" in gps_data and "GPSLongitudeRef" in gps_data:
            lon = convert_to_degrees(gps_data["GPSLongitude"])
            if gps_data["GPSLongitudeRef"] != "E":
                lon = -lon
            gps_data["Longitude"] = lon
    return gps_data

def get_location_name(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=10&addressdetails=1"
        headers = {'User-Agent': 'ERR0R-V4U-EXIF-Tool'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            address = data.get("address", {})
            components = []
            for key in ["city", "town", "village", "state", "country"]:
                if key in address:
                    components.append(address[key])
            return ", ".join(components) if components else "Unknown location"
        else:
            return "Failed to get location"
    except Exception as e:
        return f"Error: {str(e)}"

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"[+] Saved EXIF data to {filename}")

def remove_exif(image_path, output_path):
    image = Image.open(image_path)
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    image_without_exif.save(output_path)
    print(f"[+] EXIF data removed and saved to {output_path}")

def camera_info(exif_data):
    keys = ['Make', 'Model', 'LensModel', 'Software']
    return {k: exif_data[k] for k in keys if k in exif_data}

def owner_info():
    print("""
==============================
        Tools Owner Info
==============================
[📘] Facebook Page : https://www.facebook.com/profile.php?id=61564222827738
[📢] Telegram Channel: https://t.me/ERR0R_V4U_Your_Love
""")

def menu():
    print("""
==============================
    ERR0R-EXIF TOOLS MENU
==============================

[1] Extract EXIF Data & Display
[2] Remove EXIF Data (Keep Original)
[3] View GPS/Location Data
[4] View Camera Info
[5] Save EXIF Data as JSON
[6] Exit
""")

def main():
    banner()
    owner_info()
    image_path = input("[?] Enter image path: ").strip()
    if not os.path.exists(image_path):
        print("[-] File not found.")
        return

    exif_data = extract_exif(image_path)

    while True:
        menu()
        choice = input("[?] Enter your choice: ").strip()

        if choice == '1':
            if exif_data:
                for key, val in exif_data.items():
                    print(f"{key}: {val}")
            else:
                print("[-] No EXIF data found.")
        elif choice == '2':
            out_path = input("[+] Enter output filename (e.g., clean.jpg): ").strip()
            remove_exif(image_path, out_path)
        elif choice == '3':
            gps = get_gps_info(exif_data)
            if gps and "Latitude" in gps and "Longitude" in gps:
                print(json.dumps(gps, indent=4))
                location_name = get_location_name(gps["Latitude"], gps["Longitude"])
                print(f"📍 Approximate Location: {location_name}")
            else:
                print("[-] No GPS data found.")
        elif choice == '4':
            cam = camera_info(exif_data)
            if cam:
                print(json.dumps(cam, indent=4))
            else:
                print("[-] No camera info found.")
        elif choice == '5':
            if exif_data:
                filename = input("[+] Enter filename to save JSON (e.g., exif_data.json): ").strip()
                if filename == "":
                    filename = "exif_data.json"
                save_json(exif_data, filename)
            else:
                print("[-] No EXIF data to save.")
        elif choice == '6':
            print("[+] Exiting. Thanks for using ERR0R-V4U tool.")
            break
        else:
            print("[-] Invalid choice. Please enter a number between 1-6.")

if __name__ == "__main__":
    main()
