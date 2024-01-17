from vulnerabilities_fetcher.wordfence_api import fetch_vulnerabilities

def check_wordpress_vulnerabilities(wordpress_version):
    if not wordpress_version:
        print("WordPress version not found.")
        return

    vulnerabilities = fetch_vulnerabilities()

    if vulnerabilities:
        for vuln_id, details in vulnerabilities.items():
            for software in details['software']:
                if (
                    software['type'] == 'core' and
                    software['name'] == 'WordPress' and
                    version_in_range(wordpress_version, software['affected_versions'])
                ):
                    print(f"    Title:      {details['title']}")
                    print(f"    References: {', '.join(details['references'])}")
                    print(f"    CVE:        {details.get('cve', 'N/A')}")
                    # Add score and rating information
                    score = details.get('cvss', {}).get('score', 'N/A')
                    rating = details.get('cvss', {}).get('rating', 'N/A')
                    print(f"    Score:      {score}")
                    print(f"    Rating:     {rating}")
                    print(f"    Published:  {details.get('published', 'N/A')}")
                    print(f"    Updated:    {details.get('updated', 'N/A')}")
                    print("")

def version_in_range(wordpress_version, affected_versions):
    for version, version_details in affected_versions.items():
        from_version = version_details.get('from_version')
        to_version = version_details.get('to_version')

        if (
            (from_version is None or wordpress_version >= from_version) and
            (to_version == '*' or wordpress_version <= to_version)
        ):
            return True

    return False
