"""
Utility functions for Smart Finance Manager
"""
import re
from decimal import Decimal
try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


def extract_amount_from_receipt(image_file):
    """
    Extract expense amount from receipt image using OCR.
    
    Args:
        image_file: Uploaded image file (Django UploadedFile object)
    
    Returns:
        dict: {
            'amount': Decimal or None,
            'text': str (extracted text),
            'success': bool
        }
    """
    if not OCR_AVAILABLE:
        return {
            'amount': None,
            'text': '',
            'success': False,
            'error': 'OCR not available. Install pytesseract and Tesseract-OCR.'
        }
    
    try:
        # Set Tesseract path for Windows (adjust if needed)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # Open and process image
        image = Image.open(image_file)
        
        # Extract text using OCR
        extracted_text = pytesseract.image_to_string(image)
        
        # Try to find amount in the extracted text
        amount = extract_amount_from_text(extracted_text)
        
        return {
            'amount': amount,
            'text': extracted_text,
            'success': True
        }
    
    except Exception as e:
        return {
            'amount': None,
            'text': '',
            'success': False,
            'error': str(e)
        }


def extract_amount_from_text(text):
    """
    Extract monetary amount from text using regex patterns.
    
    Args:
        text: str - Text to search for amounts
    
    Returns:
        Decimal or None - Extracted amount
    """
    # Common patterns for amounts in receipts
    patterns = [
        r'total[:\s]+(?:rs\.?|₹)?\s*(\d+(?:[.,]\d{1,2})?)',  # Total: Rs. 123.45
        r'(?:rs\.?|₹)\s*(\d+(?:[.,]\d{1,2})?)',  # Rs. 123.45 or ₹123.45
        r'amount[:\s]+(?:rs\.?|₹)?\s*(\d+(?:[.,]\d{1,2})?)',  # Amount: 123.45
        r'grand\s+total[:\s]+(?:rs\.?|₹)?\s*(\d+(?:[.,]\d{1,2})?)',  # Grand Total: 123.45
        r'net\s+amount[:\s]+(?:rs\.?|₹)?\s*(\d+(?:[.,]\d{1,2})?)',  # Net Amount: 123.45
        r'(\d+(?:[.,]\d{1,2})?)\s*(?:rs\.?|₹)',  # 123.45 Rs.
    ]
    
    amounts = []
    
    # Search for all patterns
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                # Extract the amount and convert comma to dot if present
                amount_str = match.group(1).replace(',', '.')
                amount = Decimal(amount_str)
                amounts.append(amount)
            except:
                continue
    
    # Return the largest amount found (usually the total)
    if amounts:
        return max(amounts)
    
    return None


def parse_voice_expense(text):
    """
    Parse voice input to extract expense details.
    
    Examples:
        "spent 500 rupees on groceries"
        "expense of 250 for transport"
        "paid 1000 for electricity bill"
    
    Args:
        text: str - Voice input text
    
    Returns:
        dict: {
            'amount': Decimal or None,
            'description': str or None
        }
    """
    text = text.lower().strip()
    
    # Patterns to extract amount and description
    patterns = [
        r'(?:spent|paid|expense of)\s+(\d+(?:\.\d{1,2})?)\s*(?:rupees?|rs\.?|₹)?\s*(?:on|for)\s+(.+)',
        r'(\d+(?:\.\d{1,2})?)\s*(?:rupees?|rs\.?|₹)\s*(?:on|for)\s+(.+)',
        r'(?:spent|paid)\s+(\d+(?:\.\d{1,2})?)\s*(?:on|for)?\s*(.+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                amount = Decimal(match.group(1))
                description = match.group(2).strip() if len(match.groups()) > 1 else None
                return {
                    'amount': amount,
                    'description': description
                }
            except:
                continue
    
    # If no pattern matches, try to extract just numbers
    number_match = re.search(r'(\d+(?:\.\d{1,2})?)', text)
    if number_match:
        try:
            amount = Decimal(number_match.group(1))
            # Use remaining text as description
            description = re.sub(r'\d+(?:\.\d{1,2})?', '', text).strip()
            description = re.sub(r'(?:rupees?|rs\.?|₹|spent|paid|expense)', '', description, flags=re.IGNORECASE).strip()
            
            return {
                'amount': amount,
                'description': description if description else None
            }
        except:
            pass
    
    return {
        'amount': None,
        'description': text
    }
