import json
import re

def get_state_from_address(address_string):
    """
    A simple function to extract the state from an address string.
    """
    address_lower = address_string.lower()
    if "karnataka" in address_lower:
        return "karnataka"
    if "delhi" in address_lower:
        return "delhi"
    if "maharashtra" in address_lower:
        return "maharashtra"
    return "unknown"


def calculate_stamp_duty(model_output):
    """
    Calculates the stamp duty based on the extracted entities from the AI model.
    """
    extracted_data = {}
    for entity in model_output:
        label = entity.get('entity_group')
        text = entity.get('word')
        
        # --- THIS IS THE GUARANTEED FIX FOR NUMBER EXTRACTION ---
        # We need to check for LANDLORD/TENANT too for your new model
        if label in ['RENT_AMOUNT', 'DEPOSIT_AMOUNT']:
            # Remove all non-digit characters from the string
            numeric_string = re.sub(r'[^\d]', '', text)
            if numeric_string:
                extracted_data[label] = int(numeric_string)
        # --- END OF FIX ---
        else:
            extracted_data[label] = text

    rent = extracted_data.get('RENT_AMOUNT', 0)
    deposit = extracted_data.get('DEPOSIT_AMOUNT', 0)
    address = extracted_data.get('PREMISES_ADDRESS', "")
    state = get_state_from_address(address)
    
    calculation_details = {
        "rent_extracted": f"Rs. {rent:,}",
        "deposit_extracted": f"Rs. {deposit:,}",
        "state_detected": state.capitalize(),
        "stamp_duty": "N/A",
        "notes": ""
    }

    if state == "karnataka":
        annual_rent = rent * 12
        total_consideration = annual_rent + deposit
        duty = total_consideration * 0.005
        
        if duty > 500:
            duty = 500
        
        calculation_details["stamp_duty"] = f"Rs. {duty:.2f}"
        calculation_details["notes"] = "Based on Karnataka rule: 0.5% of (Annual Rent + Deposit), capped at Rs. 500 for leases up to 1 year."

    elif state == "delhi":
        annual_rent = rent * 12
        duty = annual_rent * 0.02
        
        calculation_details["stamp_duty"] = f"Rs. {duty:.2f}"
        calculation_details["notes"] = "Based on Delhi rule: 2% of the average annual rent for leases up to 5 years."

    else:
        calculation_details["notes"] = "Stamp duty rules for the detected state are not implemented yet."

    return calculation_details


if __name__ == "__main__":
    
    # --- HERE ARE YOUR RESULTS FROM sample_3.docx ---
    # I have pasted the list your model found, but it missed the DEPOSIT_AMOUNT.
    
    sample_model_output = [
        {'entity_group': 'LANDLORD', 'score': 0.9858, 'word': 'mrs. meera deshpande'}, 
        {'entity_group': 'TENANT', 'score': 0.9866, 'word': 'mr. rohan bhatia'}, 
        {'entity_group': 'PREMISES_ADDRESS', 'score': 0.9976, 'word': '# d - 504, brigade metropolis, whitefield main road, mahadevapura, bengaluru - 560048, karnataka'}, 
        {'entity_group': 'RENT_AMOUNT', 'score': 0.9848, 'word': 'inr 28, 000 / -'},
        
        # --- !! ACTION REQUIRED !! ---
        # The model missed the deposit. I added this line for you.
        # Please open 'sample_3.docx', find the real deposit amount, 
        # and replace the text in 'word' below.
        {'entity_group': 'DEPOSIT_AMOUNT', 'score': 0.95, 'word': 'INR 150,000 (CHANGE ME!)'}
    ]

    print("--- Calculating Stamp Duty from AI Model Output (sample_3.docx) ---")
    result = calculate_stamp_duty(sample_model_output)
    
    print("\n---  Calculation Results ---")
    for key, value in result.items():
        print(f"  -> {key.replace('_', ' ').title()}: {value}")