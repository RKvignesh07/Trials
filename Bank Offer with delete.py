import time
import requests
import random

# Replace with your actual values
BOT_TOKEN = '6947300929:AAHG2hzvK6sf7CEUHV6Ajo_GFC1zZbPXz7Q'
CHANNEL_ID = '@Tech_Bytez'

# List of deals with a delay of 5 minutes between each deal
deals_list = [
    {"title": "Deal 1", "description": "Description for Deal 1", "url": "https://example.com/deal1", "image_url": "https://m.media-amazon.com/images/I/51HaYVy6TnL._SX300_SY300_QL70_FMwebp_.jpg", "coupon": "DealCoupon1", "regular_price": "$99.99", "bank_offer": "5% Cashback with XYZ Bank Credit Card"},
    {"title": "Deal 2", "description": "Description for Deal 2", "url": "https://example.com/deal2", "image_url": "https://m.media-amazon.com/images/I/51HaYVy6TnL._SX300_SY300_QL70_FMwebp_.jpg", "coupon": "", "regular_price": "", "bank_offer": ""},
    {"title": "Deal 3", "description": "Description for Deal 3", "url": "https://example.com/deal3", "image_url": "https://example.com/image3.jpg", "coupon": "DealCoupon3", "regular_price": "", "bank_offer": "EMI Options available"},
    # Add more deals as needed
]

failed_deals = []

def is_valid_deal(deal):
    # Check if the deal structure is valid
    required_keys = ["title", "description", "url", "image_url"]
    return all(key in deal for key in required_keys)

def send_deal(deal, deal_number, total_deals, delay_time, sent_deals):
    # Validate the presence of necessary keys in the deal
    if is_valid_deal(deal):
        # Check if any of the essential fields (title, description, URL, image link) is empty
        if any(not deal[field] for field in ["title", "description", "url", "image_url"]):
            print(f"Deal '{deal['title']}' is missing essential fields. Skipping...", flush=True)
            failed_deals.append(deal)
            return

        try:
            # Check if the deal has already been sent
            if deal["title"] in sent_deals:
                print(f"Deal '{deal['title']}' has already been sent. Skipping...", flush=True)
                return

            # Download and attach the image
            image_path = download_image(deal["image_url"])

            if image_path:
                # Build the caption
                formatted_title = f"<b>{deal['title']}</b>"
                description = f"➡️ <b>{deal['description']}</b>"
                coupon_info = f"\n\n💥💥 Coupon: {deal['coupon']}" if deal["coupon"] else ""
                regular_price = f"\n\n💰 Regular Price: {deal['regular_price']} ❌" if deal["regular_price"] else ""
                bank_offer = f"\n\n🏦 Bank Offer: {deal['bank_offer']}" if deal["bank_offer"] else ""
                caption = f"{formatted_title}\n\n{description}{regular_price}{coupon_info}{bank_offer}\n\n🔗: {deal['url']}"
                
                url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
                files = {'photo': open(image_path, 'rb')}
                params = {'chat_id': CHANNEL_ID, 'caption': caption, 'parse_mode': 'HTML'}
                response = requests.post(url, files=files, params=params)

                # Check if the deal was successfully sent
                if response.status_code == 200:
                    # Display deal information in the output
                    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    print(f"Deal {deal_number}/{total_deals} - '{deal['title']}' sent at {current_time}.", flush=True)
                    print(f"Countdown for next deal:", end=" ", flush=True)

                    # Countdown before the next deal
                    for remaining_seconds in range(delay_time * 60, 0, -1):
                        print(f"\rRemaining: {remaining_seconds // 60} minutes and {remaining_seconds % 60} seconds... Pending Deals: {total_deals - deal_number}", end="", flush=True)
                        time.sleep(1)
                    
                    print(" " * 50, end="\n", flush=True)  # Clear the line after countdown

                    # Clean up: Delete the downloaded image
                    delete_image(image_path)

                    # Add the deal to the set of sent deals
                    sent_deals.add(deal["title"])
                else:
                    print(f"Failed to send deal '{deal['title']}'. Telegram API response: {response.text}")
                    failed_deals.append(deal)
            else:
                print(f"Image path is empty for deal '{deal['title']}'. Check the download_image function.")
                failed_deals.append(deal)
        except Exception as e:
            print(f"Error occurred while sending deal '{deal['title']}': {str(e)}")
            failed_deals.append(deal)
    else:
        print(f"Invalid deal structure for deal '{deal['title']}': {deal}")
        failed_deals.append(deal)

def download_image(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                image_data = response.content
                image_path = "downloaded_image.jpg"
                with open(image_path, 'wb') as image_file:
                    image_file.write(image_data)
                return image_path
            else:
                print(f"Failed to download image. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error occurred while downloading image (Attempt {attempt + 1}/{max_retries}): {str(e)}")
            time.sleep(2)  # Wait for 2 seconds before retrying

    print(f"Max retries exceeded. Unable to download image from URL: {url}")
    return None

def delete_image(path):
    # This is an imaginary function to delete the downloaded image
    # In a real-world scenario, you might want to delete the image after sending it.
    pass

def print_failed_deals():
    if failed_deals:
        print("\nDeals failed to send:")
        for deal in failed_deals:
            print(f"- {deal['title']}")

def send_deals():
    # Shuffle the deals list to send them in a random order
    random.shuffle(deals_list)
    
    total_deals = len(deals_list)
    delay_time = 1  # Adjust this value as needed (in minutes)
    
    print(f"Total number of deals in the list: {total_deals}")

    # Set to keep track of sent deals
    sent_deals = set()

    for i, deal in enumerate(deals_list, start=1):
        send_deal(deal, i, total_deals, delay_time, sent_deals)

    print("\nAll deals sent successfully!")
    print_failed_deals()

if __name__ == "__main__":
    send_deals()
