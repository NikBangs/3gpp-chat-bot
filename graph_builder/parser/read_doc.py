from pathlib import Path

def read_doc(path):

    ext = path.suffix.lower()

    if ext == ".docx":
        from docx import Document
        print(f"📂 Trying to open (Word): {path}")
        doc = Document(str(path))
        return "\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())


    elif ext == ".doc":
        try:
            import win32com.client
            

           # Start Word
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False

            # Get full absolute path in Windows-friendly format
            abs_path = Path(path).resolve(strict=True)
            word_path = str(abs_path)

            print(f"📂 Trying to open (Word): {word_path}")

            # Open the file in Word (non-visible)
            doc = word.Documents.Open(word_path)
            text = doc.Content.Text
            doc.Close(False)
            word.Quit()

            return text

        except Exception as e:
            import traceback
            print("🛠 FULL ERROR TRACE:")
            traceback.print_exc()
            raise RuntimeError(f"Could not read .doc file using Word COM: {e}")



    else:
        raise ValueError("Unsupported file format. Only .doc and .docx allowed.")
