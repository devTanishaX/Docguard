import docx
import os
# NEW: Import the 'Auto' classes to load your saved model
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification

def audit_document_with_hf_model(model_path, docx_path):
    if not os.path.exists(model_path):
        print(f"Error: Model folder '{model_path}' not found. Please train the model first.")
        return
    if not os.path.exists(docx_path):
        print(f"Error: Document '{docx_path}' not found.")
        return

    print(f"\nLoading model from '{model_path}' ---")
    
    # --- NEW CHANGES START HERE ---
    # 1. Load the tokenizer that you saved
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    # 2. Load the model that you saved
    model = AutoModelForTokenClassification.from_pretrained(model_path)
    
    # 3. Create the pipeline using your specific model and tokenizer
    nlp_pipeline = pipeline(
        "ner", 
        model=model, 
        tokenizer=tokenizer, 
        aggregation_strategy="simple"
    )
    # --- NEW CHANGES END HERE ---
        
    print(f"Reading document: '{docx_path}' ---")
    try:
        doc = docx.Document(docx_path)
        full_text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading .docx file: {e}")
        return

    if not full_text.strip():
        print("Error: Document is empty or could not be read.")
        return

    print("Auditing document... ---")
    entities = nlp_pipeline(full_text)
    print("\n--- Raw Data for Duty Calculator (COPY THIS LIST) ---")
    print(entities)
    print("\nAudit Results ---")
    if entities:
        for entity in entities:
            # The 'replace' logic is to clean up tokens that get split
            entity_text = entity['word'].strip().replace(' ##', '')
            entity_label = entity['entity_group']
            score = entity['score']
            print(f"  -> Found: '{entity_text}'  |  Type: '{entity_label}' (Confidence: {score:.2%})")
    else:
        print("  The model did not find any entities.")

if __name__ == "__main__":
    TRAINED_MODEL_FOLDER = 'trained_hf_model'
    
    # IMPORTANT: Change this to one of your test .docx files
    DOCUMENT_TO_AUDIT = 'sample_3.docx' 
    
    audit_document_with_hf_model(TRAINED_MODEL_FOLDER, DOCUMENT_TO_AUDIT)