import requests
import csv
import urllib.parse
import time

def fetch_card_by_name(card_name):
    """Fetch specific card data from Yu-Gi-Oh! API using card name"""
    encoded_name = urllib.parse.quote(card_name.strip())
    url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?name={encoded_name}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['data'][0]  # Return first match
    except Exception as e:
        print(f"Error fetching data for {card_name}: {e}")
        return None

def create_card_row(card):
    """Convert card data to CSV row format"""
    if not card:
        return None
        
    # Create handle from name (lowercase with hyphens)
    handle = card['name'].lower().replace(' ', '-')
    
    # Get price from Amazon if available
    price = card['card_prices'][0]['amazon_price'] if 'card_prices' in card else ''
    
    # Get image URL
    image_url = card['card_images'][0]['image_url'] if 'card_images' in card else ''
    
    # Create tags from card attributes
    tags = []
    if 'attribute' in card:
        tags.append(card['attribute'])
    if 'race' in card:
        tags.append(card['race'])
    if 'level' in card:
        tags.append(f"Level {card['level']}")
    tags = ', '.join(tags)

    return {
        'Handle': handle,
        'Title': card['name'],
        'Body (HTML)': card.get('desc', ''),
        'Vendor': 'Konami',
        'Product Category': 'Card Games',
        'Type': 'Card',
        'Tags': tags,
        'Published': 'TRUE',
        'Variant SKU': str(card.get('id', '')),
        'Variant Price': price,
        'Image Src': image_url,
        'Image Alt Text': f"{card['name']} Yu-Gi-Oh! Card",
        'Status': 'active',
        'Metafield: custom.attack': card.get('atk', ''),
        'Metafield: custom.defense': card.get('def', ''),
        'Metafield: custom.level': card.get('level', ''),
        'Metafield: custom.race': card.get('race', ''),
        'Metafield: custom.attribute': card.get('attribute', '')
    }

def process_deck_file(deck_name):
    """Process a deck file and create corresponding CSV"""
    input_file = f"{deck_name}.txt"
    output_file = f"{deck_name}.csv"
    
    fieldnames = [
        'Handle', 'Title', 'Body (HTML)', 'Vendor', 'Product Category', 'Type',
        'Tags', 'Published', 'Variant SKU', 'Variant Price', 'Image Src',
        'Image Alt Text', 'Status', 'Metafield: custom.attack',
        'Metafield: custom.defense', 'Metafield: custom.level',
        'Metafield: custom.race', 'Metafield: custom.attribute'
    ]

    try:
        # Read card names from deck file
        with open(input_file, 'r', encoding='utf-8') as f:
            card_names = f.readlines()
        
        # Create CSV file
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Process each card
            for card_name in card_names:
                print(f"Processing card: {card_name.strip()}")
                card_data = fetch_card_by_name(card_name)
                if card_data:
                    row = create_card_row(card_data)
                    if row:
                        writer.writerow(row)
                # Add small delay to avoid API rate limiting
                time.sleep(0.1)
                
        print(f"Successfully created {output_file}")
    except FileNotFoundError:
        print(f"Error: Could not find deck file '{input_file}'")
    except Exception as e:
        print(f"Error processing deck: {e}")

def main():
    # Get deck name from user
    deck_name = input("Enter deck file name (without .txt extension): ")
    process_deck_file(deck_name)

if __name__ == "__main__":
    main()
