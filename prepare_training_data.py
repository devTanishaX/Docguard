import json
import docx
import os
import re

def create_training_data(docx_path, json_path):
    try:
        doc = docx.Document(docx_path)
        full_text = "\n".join([para.text for para in doc.paragraphs])
    except Exception:
        return None

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    except Exception:
        return None

    entities = []

    def find_and_add_entity(text_to_find, label):
        if text_to_find is None: return
        text_str = str(text_to_find).strip()
        if not text_str: return
        
        # This robust pattern correctly finds numbers with commas and currency symbols
        if text_str.isdigit():
            num_with_commas = f"{int(text_str):,}"
            pattern = r'(?:Rs\.?|INR)?\s*(' + re.escape(num_with_commas) + r'|' + re.escape(text_str) + r')\s*(?:/-)?'
        else:
            pattern = re.escape(text_str).replace(r'\ ', r'\s+')

        try:
            for match in re.finditer(pattern, full_text, re.IGNORECASE):
                start, end = match.span()
                entities.append((start, end, label))
                return
        except re.error:
            pass

    def extract_amount(value):
        return value.get('amount') if isinstance(value, dict) else value

    for party in metadata.get('parties', []):
        find_and_add_entity(party.get('name'), party.get('role', 'PARTY').upper())
    find_and_add_entity(metadata.get('premises', {}).get('address'), 'PREMISES_ADDRESS')
    financials = metadata.get('financials', {})
    find_and_add_entity(extract_amount(financials.get('monthly_rent')), 'RENT_AMOUNT')
    find_and_add_entity(extract_amount(financials.get('security_deposit')), 'DEPOSIT_AMOUNT')
    find_and_add_entity(extract_amount(financials.get('stamp_duty')), 'STAMP_DUTY')
    term = metadata.get('term', {})
    find_and_add_entity(term.get('start_date'), 'START_DATE')
    find_and_add_entity(term.get('end_date'), 'END_DATE')
    find_and_add_entity(extract_amount(term.get('duration')), 'DURATION')

    if full_text and entities:
        return (full_text, {'entities': entities})
    return None

if __name__ == "__main__":
    document_pairs = []
    # 1. Point directly to your new folder name
    target_folder = 'data_samples' 
    
    # 2. Scan inside the data_samples folder instead of the root
    if os.path.exists(target_folder):
        for filename in os.listdir(target_folder):
            if filename.lower().endswith(".docx") and not filename.startswith('~'):
                base_name = os.path.splitext(filename)[0]
                
                # Check for matching JSON files inside data_samples
                json_file = next((f for f in [base_name + ".json", base_name + ".json.txt"] 
                                  if os.path.exists(os.path.join(target_folder, f))), None)
                
                if json_file:
                    # Keep track of the proper folder paths
                    full_docx_path = os.path.join(target_folder, filename)
                    full_json_path = os.path.join(target_folder, json_file)
                    document_pairs.append((full_docx_path, full_json_path))

    master_training_data = []
    print(f"--- Found {len(document_pairs)} document pairs to process inside '{target_folder}'. ---")
    for docx_file, json_file in document_pairs:
        print(f"Processing '{docx_file}'...")
        example = create_training_data(docx_file, json_file)
        if example:
            master_training_data.append(example)

    if master_training_data:
        # 3. This line remains unchanged so it still outputs directly to your root folder!
        with open('master_training_data.json', 'w', encoding='utf-8') as f:
            json.dump(master_training_data, f, indent=4)
        print(f"\n Success! Created 'master_training_data.json' with {len(master_training_data)} documents.")