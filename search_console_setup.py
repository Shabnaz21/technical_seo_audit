import requests
from bs4 import BeautifulSoup

def check_search_console(domain):
    try:
        # Fetch the domain's HTML content
        response = requests.get(domain)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for the Google Search Console meta tag
        meta_tag = soup.find('meta', attrs={'name': 'google-site-verification'})

        if meta_tag:
            content_value = meta_tag.get('content', None)
            if content_value:
                print(f"Google Search Console meta tag found: {content_value}")
                return content_value
            else:
                print("Google Search Console meta tag is present but has no content.")
                return None
        else:
            print("Google Search Console meta tag is not present.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the domain: {e}")
        return None

# Example usage
domain = "https://topsell.shop"  # Replace with your domain
check_search_console(domain)
