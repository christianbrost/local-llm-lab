import ollama
import os
import sys
from pathvalidate import sanitize_filename

def get_image_files(folder_path):
    """gibt liste der bildpfade im ordner zurück"""
    imagePaths = []
    directory = os.fsencode(folder_path)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        imagePaths.append(folder_path + "/" + filename)

    return imagePaths


def describe_image(image_path):
    """schickt bild an llava, gibt freitext-beschreibung zurück"""
    try:
        image = [image_path]

        

        systemPrompt = ("describe the content of the image")
        messages = [
                {"role": "system", "content": systemPrompt, "images":image}
            ]

        response = ollama.chat(
            model="llava",  
            messages=messages
        )

        return response['message']['content'] #sollte doch richtiges format der rückgabe sein?
        
    except Exception as e:
        print(f"Fehler bei describe_image({image_path}): {e}")
        return None


def summarize_to_filename(description):
    """schickt beschreibung an textmodell, das daraus einen kurzen dateinamen macht"""
    try:
        messages = [
                {
                    "role": "system",
                    "content": (
                        "du bist ein strukturierter developer, der dateien anhand einer kurzen "
                        "beschreibung benennt. antworte AUSSCHLIESSLICH mit dem dateinamen, "
                        "ausschliesslich in deutsch antworten\n"
                        "format: exakt 2 wörter, snake_case, z.B. 'roter_sportwagen'.\n"
                        "keine Leerzeichen"
                    )
                },
                {
                    "role": "user",
                    "content": description
                }
        ]

        response = ollama.chat(
                    model="qwen2.5:7b",
                    messages=messages
        )

        return response['message']['content']
        
    except Exception as e:
        print(f"Fehler bei summarize_to_filename: {e}")
        return None

def rename_image(old_path, new_name, extension):
    """benennt die datei um (oder kopiert, je nachdem was du willst)"""
    try:
        filename = new_name + extension
        os.rename(old_path, filename)
        return 1
    except Exception as e:
        return None
        print(f"Fehler bei rename_image({old_path} -> {new_name}): {e}")


def process_folder(folder_path):
    image_files = get_image_files(folder_path)

    for image_path in image_files:
        #print("Currently processing " + image_path)
        root, ext = os.path.splitext(image_path)
        if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
             continue

        description = describe_image(image_path)
        if description == None:
            continue
        filename = summarize_to_filename (description)
        if filename == None:
                    continue
        validFilename = sanitize_filename(filename)
        if validFilename == None:
                    continue
        dirName = os.path.dirname(image_path)
        newPath = os.path.join(dirName, validFilename)
        
        if rename_image(old_path=image_path, new_name=newPath, extension=ext) == None:
            continue
        oldName = os.path.basename(image_path)
        newName = os.path.basename(newPath) + ext
        print(f"Vorher: {oldName}  ->  Nachher: {newName}\n")



def main():
    while True:
        folder_path = input("\nOrdnerpfad (oder 'exit'): ")

        if folder_path == "exit":
            print("Bye")
            break

        try:
            process_folder(folder_path)
        except Exception as e:
            print(f"Fehler: {e}")


if __name__ == "__main__":
    main()

