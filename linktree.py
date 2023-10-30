## Link tree builder using Lxml
# (lighter but better in performance than scrapy)
# Author: Mukul Kumar

from lxml import html
import requests
import json

def build_link_tree(url):
    try:
        session = requests.Session()
        page = session.get(url)
        page.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Invalid URL")
        return None

    tree = html.fromstring(page.content)

    link_tree = {
        "url": url,
        "links": []
    }

    links = tree.xpath('//a')
    for link in links:
        link_url = link.get('href')
        link_title = link.text

        # Check for empty or None URLs.
        if link_url and link_url.strip():
            link_tree["links"].append({"url": link_url, "title": link_title})

    return link_tree

def build_recursive_link_tree(url, depth=2):
    if depth == 0:
        return build_link_tree(url)

    link_tree = build_link_tree(url)
    if link_tree is None:
        return None

    for link_info in link_tree["links"]:
        link_url = link_info["url"]
        if link_url and link_url.startswith("http") and link_url.startswith(start_url):
            sub_tree = build_recursive_link_tree(link_url, depth - 1)
            if sub_tree is not None:
                link_info["tree"] = sub_tree

    return link_tree

if __name__ == "__main__":
    start_url = input("Enter the URL to crawl: ")
    link_tree = build_recursive_link_tree(start_url)

    if link_tree is not None:
        def count_urls(tree):
            if "links" not in tree:
                return 0
            count = len(tree["links"])
            for link_info in tree["links"]:
                if "tree" in link_info:
                    count += count_urls(link_info["tree"])
            return count

        with open('linktree.json', 'w') as json_file:
            json.dump(link_tree, json_file, indent=4)

        num_urls = count_urls(link_tree)
        print(f"Link tree created in linktree.json. {num_urls} URLs found.")