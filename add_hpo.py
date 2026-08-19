import json
import urllib.request
import urllib.parse
import time

def fetch_hpo(term):
    # Try to simplify the term by removing commas and splitting by comma (sometimes terms are inverted like "Antihelix, Absent")
    parts = term.split(',')
    if len(parts) > 1:
        query = parts[-1].strip() + " " + " ".join(parts[:-1]).strip()
    else:
        query = term
    
    url = f"https://www.ebi.ac.uk/ols4/api/search?q={urllib.parse.quote(query)}&ontology=hp&rows=1"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            docs = data.get('response', {}).get('docs', [])
            if docs:
                return docs[0].get('obo_id'), docs[0].get('label')
    except Exception as e:
        print(f"Error fetching {query}: {e}")
    
    return None, None

def process_file(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    total = len(data)
    for i, item in enumerate(data):
        if 'hpo_id' not in item:
            term = item['term']
            hpo_id, hpo_label = fetch_hpo(term)
            if hpo_id:
                item['hpo_id'] = hpo_id
                item['hpo_label'] = hpo_label
            else:
                # fallback query
                hpo_id, hpo_label = fetch_hpo(term.split(',')[0])
                if hpo_id:
                    item['hpo_id'] = hpo_id
                    item['hpo_label'] = hpo_label
            print(f"Processed {i+1}/{total}: {term} -> {hpo_id} ({hpo_label})")
            time.sleep(0.1) # to avoid rate limit
            
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    process_file('/home/arkantu/workspace/docker/webapps-static-stack/morphology-atlas/data/organized/morphology_terms_corrected.json')
