import requests


def check_robots_txt():
    """
    Check if robots.txt exists and contains 'User-agent: *' and a sitemap reference.
    """
    # Step 1: Get domain input from the user
    domain = input("Enter the domain: ").strip()

    # Remove trailing slash if it exists
    if domain.endswith('/'):
        domain = domain[:-1]

    if not domain.startswith("http"):
        domain = "https://" + domain  # Add https if missing

    robots_url = f"{domain}/robots.txt"  # Robots.txt URL

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
    }

    try:
        # Step 2: Fetch robots.txt with a custom User-Agent
        response = requests.get(robots_url, headers=headers, timeout=10)

        # Handle different HTTP responses
        if response.status_code == 200:
            # Step 3: Check the content of robots.txt
            robots_content = response.text
            # print(f"\n📄 Robots.txt Content:\n{robots_content}\n")

            # Check for "User-agent: *"
            if "User-agent: *" in robots_content:
                print("✅ 'User-agent: *' is present in robots.txt.")
            else:
                print("❌ 'User-agent: *' is missing in robots.txt.")

            # Check for a sitemap reference
            if "Sitemap:" in robots_content:
                print("✅ Sitemap reference is present in robots.txt.")
                # Extract and display the sitemap URLs
                sitemaps = [line.split(": ", 1)[1] for line in robots_content.splitlines() if
                            line.startswith("Sitemap:")]
                for sitemap in sitemaps:
                    print(f"   - Sitemap found: {sitemap}")
            else:
                print("❌ No sitemap reference found in robots.txt.")

        elif response.status_code == 404:
            print("❌ robots.txt file not found (404 error).")
        else:
            print(f"❌ robots.txt file is inaccessible. HTTP status code: {response.status_code}")

    except requests.RequestException as e:
        print(f"❌ Failed to fetch robots.txt due to error: {e}")


# Run the script
if __name__ == "__main__":
    check_robots_txt()
