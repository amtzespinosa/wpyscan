import requests

def fetch_vulnerabilities(feed_type='production'):
    base_url = 'https://www.wordfence.com/api/intelligence/v2/vulnerabilities'
    endpoint = f'{base_url}/{feed_type}'

    try:
        response = requests.get(endpoint)
        response.raise_for_status()

        vulnerabilities = response.json()
        return vulnerabilities

    except requests.exceptions.RequestException as e:
        print(f"Error fetching vulnerabilities: {e}")
        return None

if __name__ == "__main__":
    # Example usage to fetch vulnerabilities from the production feed
    vulnerabilities = fetch_vulnerabilities(feed_type='production')
    if vulnerabilities:
        print("Vulnerabilities fetched successfully.")
        print(f"Number of vulnerabilities: {len(vulnerabilities)}")
        # Add further processing or printing of vulnerability details as needed
