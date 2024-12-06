import requests
from bs4 import BeautifulSoup
import csv

def fetch_and_parse_sitemap(domain, sitemap_path="sitemap.xml", filename="sitemap_urls.csv"):
    """
    Fetch and parse sitemap(s) from the provided domain.
    Save the URLs into a CSV file.
    """
    # Remove trailing slash if it exists
    if domain.endswith('/'):
        domain = domain[:-1]

    if not domain.startswith("http"):
        domain = "https://" + domain  # Add https if missing

    sitemap_url = f"{domain}/{sitemap_path}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
    }

    try:
        print(f"Trying to fetch: {sitemap_url}")
        response = requests.get(sitemap_url, headers=headers, timeout=10)

        if response.status_code == 200:
            print(f"✅ Successfully fetched {sitemap_path}")
            urls, nested_sitemaps = parse_sitemap(response.text)
            write_urls_to_csv(urls, filename)

            # Process nested sitemaps if detected
            if nested_sitemaps:
                print("\n📂 Nested Sitemap(s) detected. Fetching nested sitemaps...")
                for nested_sitemap_url in nested_sitemaps:
                    fetch_and_parse_sitemap(nested_sitemap_url, sitemap_path="", filename=filename)
        else:
            print(f"❌ {sitemap_path} not found (HTTP {response.status_code}).")
            # If sitemap.xml is not found, check for sitemap_index.xml
            if sitemap_path == "sitemap.xml":
                print("Checking for sitemap_index.xml...")
                fetch_and_parse_sitemap(domain, sitemap_path="sitemap_index.xml", filename=filename)
    except requests.RequestException as e:
        print(f"❌ Error fetching {sitemap_path}: {e}")


def parse_sitemap(sitemap_content):
    """
    Parse and return the URLs and nested sitemap URLs from the sitemap.
    """
    try:
        soup = BeautifulSoup(sitemap_content, "xml")  # Parse as XML
        urls = [url.text for url in soup.find_all("loc")]  # Extract <loc> tags
        nested_sitemaps = []

        # Detect if it's a sitemap index (contains nested sitemaps)
        if soup.find("sitemapindex"):
            nested_sitemaps = urls  # All <loc> tags in sitemap index are nested sitemaps
            print(f"✅ Found {len(nested_sitemaps)} nested sitemap(s).")

        else:
            print(f"✅ Found {len(urls)} URL(s).")

        return urls, nested_sitemaps
    except Exception as e:
        print(f"❌ Error parsing sitemap: {e}")
        return [], []


def write_urls_to_csv(urls, filename):
    """
    Write the list of URLs into a CSV file.
    """
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for url in urls:
                writer.writerow([url])
        print(f"✅ URLs have been saved to {filename}.")
    except Exception as e:
        print(f"❌ Error writing to CSV file: {e}")


if __name__ == "__main__":
    domain = input("Enter the domain: ").strip()
    filename = input("Enter the filename to save URLs (e.g., sitemap_urls.csv): ").strip()
    fetch_and_parse_sitemap(domain, filename=filename)
