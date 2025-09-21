import spacy
import docx
import os

def audit_new_document(model_path, docx_path):
    """
    Loads a trained spaCy model and uses it to find entities
    in a new, unseen Word document.
    """
    
    # 1. Load the trained "smart" model from the folder
    print(f"\n--- Loading trained model from '{model_path}' ---")
    try:
        nlp = spacy.load(model_path)
    except OSError:
        print(f"❌ Error: Could not find a trained model at '{model_path}'.")
        print("Please make sure you have run the 'train_model.py' script successfully.")
        return

    # 2. Read the text from the new Word document
    print(f"--- Reading new document: '{docx_path}' ---")
    if not os.path.exists(docx_path):
        print(f"❌ Error: The document file '{docx_path}' was not found.")
        return
        
    try:
        doc = docx.Document(docx_path)
        full_text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"❌ Error reading the document file: {e}")
        return

    # 3. Use the trained model to analyze the text
    print("--- Auditing document and extracting entities... ---")
    doc_to_audit = nlp(full_text)

    # 4. Print the results!
    print("\n--- Audit Results: ---")
    if doc_to_audit.ents:
        for ent in doc_to_audit.ents:
            # Print the text it found and the label it gave
            print(f"  -> Found: '{ent.text}'  |  Type: '{ent.label_}'")
    else:
        print("  The model did not find any entities in this document.")


# --- Main part of the script ---
if __name__ == "__main__":
    
    # The folder where your trained model is saved
    TRAINED_MODEL_FOLDER = 'trained_model'
    
    # The new document you want to audit.
    # We will use sample_1.docx as a test to see if it works.
    DOCUMENT_TO_AUDIT = 'sample_1.docx'
    
    audit_new_document(TRAINED_MODEL_FOLDER, DOCUMENT_TO_AUDIT)
