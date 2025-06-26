import re
import argparse
import string
from collections import defaultdict

def parse_bib_entries(text):
    entries = re.split(r'(?=@)', text)
    return [e.strip() for e in entries if e.strip()]

def extract_field(entry, field_name):
    # Matches lines like: title = {Some Title}, or title = "Some Title"
    pattern = rf'{field_name}\s*=\s*["{{](.+?)["}}],?'
    match = re.search(pattern, entry, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def normalize(text):
    if not text:
        return ''
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def remove_duplicates(entries):
    seen = set()
    unique = []
    for entry in entries:
        title = normalize(extract_field(entry, 'title'))
        author = normalize(extract_field(entry, 'author'))
        identifier = (title, author)
        if not title and not author:
            print("⚠️ Skipping entry with no title or author.", flush=True)
            continue
        if identifier in seen:
            print(f"→ Dropping duplicate entry with title: '{title}...'", flush=True)
        else:
            seen.add(identifier)
            unique.append(entry)
    return unique

def main():
    parser = argparse.ArgumentParser(description="Remove duplicate .bib entries based on title+author.")
    parser.add_argument("input", help="Input .bib file")
    parser.add_argument("output", help="Output .bib file (deduplicated)")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    entries = parse_bib_entries(text)
    deduped = remove_duplicates(entries)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write("\n\n".join(deduped) + "\n")

    print(f"✅ Done. {len(entries) - len(deduped)} duplicates removed, {len(deduped)} entries written.")

if __name__ == "__main__":
    main()
