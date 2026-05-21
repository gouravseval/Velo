EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "product_id": {
            "type": "string",
            "description": "Unique product/item identifier"
        },
        "rating": {
            "type": "number",
            "minimum": 1,
            "maximum": 5,
            "description": "Numeric rating from 1 to 5"
        },
        "review_text": {
            "type": "string",
            "description": "Full text of the review"
        },
        "reviewer_name": {
            "type": "string",
            "description": "Name of the reviewer"
        },
        "review_date": {
            "type": "string",
            "description": "Date in ISO 8601 format"
        }
    },
    "required": ["product_id", "rating", "review_text"]
}

EXTRACTION_INSTRUCTIONS = """
- rating must be a number 1-5. If you see "5 stars" extract 5.
- review_text should be the full review body, not the title.
- If product_id is missing, look for 'id', 'sku', 'asin', or 'item_id' columns.
- Dates should be normalized to YYYY-MM-DD format.
"""
