import xml.etree.ElementTree as ET
import os
import cairosvg
from pathlib import Path
from tqdm import tqdm
import csv


def extract_attributes(data_dir):
    """
    Return a dictionary mapping a kanji's unicode to its attributes (reading & meaning)
    from the kanjidic2.xml file.
    """
    tree = ET.parse(os.path.join(data_dir, 'kanjidic2.xml'))
    root = tree.getroot()
    entries = root.findall('character')

    attributes = {}
    for entry in entries:
        # Extract kanji unicode.
        kanji_id = entry.find('codepoint/cp_value[@cp_type="ucs"]').text
        kanji_id = int(kanji_id, 16)
        # Extract Japanese readings.
        readings = [x.text for x in entry.findall('reading_meaning/rmgroup/reading') if x.get('r_type').startswith('ja')]
        # Extract English meanings.
        meanings = [x.text for x in entry.findall('reading_meaning/rmgroup/meaning') if 'm_lang' not in x.attrib]
        attributes[kanji_id] = {'readings': readings, 'meanings': meanings}
    return attributes


svg_format = """
<svg xmlns="http://www.w3.org/2000/svg" width="{img_size}" height="{img_size}" viewBox="0 0 109 109">
<rect width="100%" height="100%" fill="#ffffff"/>
<g style="fill:none;stroke:#000000;stroke-width:3;stroke-linecap:round;stroke-linejoin:round;">
{content}
</g>
</svg>
"""

def extract_strokes(data_dir, img_size):
    """
    Return a dictionary mapping a kanji's unicode to its strokes in SVG format
    from the kanjivg.xml file.
    """
    tree = ET.parse(os.path.join(data_dir, 'kanjivg.xml'))
    root = tree.getroot()
    entries = root.findall('kanji')

    strokes = {}
    for entry in entries:
        # Extract kanji unicode.
        kanji_id = entry.get('id').split('_')[-1]
        kanji_id = int(kanji_id, 16)
        content = ET.tostring(entry, encoding='unicode', xml_declaration=False)
        strokes[kanji_id] = svg_format.format(content=content, img_size=img_size)
    return strokes


def generate_dataset(data_dir, img_size):
    """Generate the kanji dataset with the images and their corresponding meaning."""
    # Extract kanjis attributes & strokes from data files.
    attributes = extract_attributes(data_dir)
    strokes = extract_strokes(data_dir, img_size)

    # Select the kanji ids in the intersection of attributes and strokes.
    kanji_ids = set(attributes) & set(strokes)
    # Remove kanjis which don't have meaning in their list.
    kanji_ids = [kanji_id for kanji_id in kanji_ids if attributes[kanji_id]['meanings']]
    kanji_ids.sort()

    # Format kanji meanings into rows to save as a csv file,
    # and convert SVG strokes to PNG images and save on disk.
    metadata = [['file_name', 'text']]
    img_dir = os.path.join(data_dir, 'images')
    Path(img_dir).mkdir(parents=True, exist_ok=True)

    for i, kanji_id in tqdm(enumerate(kanji_ids)):
        max_digits = len(str(len(kanji_ids)))
        filename = f'{str(i + 1).zfill(max_digits)}.png'
        # We choose to use only the first meaning in the list.
        meaning = attributes[kanji_id]['meanings'][0]
        metadata.append([filename, meaning])
        filepath = os.path.join(img_dir, filename)
        cairosvg.svg2png(bytestring=strokes[kanji_id].encode('utf-8'), write_to=filepath)

    # Save kanji meanings to csv files.
    filename = os.path.join(img_dir, 'metadata.csv')
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(metadata)
        
    print("The dataset has been generated.")


if __name__ == '__main__':
    
    generate_dataset(
        data_dir='data',
        img_size=128,
    )