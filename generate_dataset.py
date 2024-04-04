import xml.etree.ElementTree as ET
import os
import cairosvg
from pathlib import Path
import json
from tqdm import tqdm


def extract_attributes(data_dir):
    """
    Returns: A dictionary mapping a kanji's unicode to its attributes.
    """
    tree = ET.parse(os.path.join(data_dir, 'kanjidic2.xml'))
    root = tree.getroot()
    entries = root.findall('character')

    attributes = dict()
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
<g style="fill:none;stroke:#000000;stroke-width:3;stroke-linecap:round;stroke-linejoin:round;">
{content}
</g>
</svg>
"""

def extract_strokes(data_dir, img_size):
    """
    Returns: A dictionary mapping a kanji's unicode to its strokes in SVG format.
    """
    tree = ET.parse(os.path.join(data_dir, 'kanjivg.xml'))
    root = tree.getroot()
    entries = root.findall('kanji')

    strokes = dict()
    for entry in entries:
        # Extract kanji unicode.
        kanji_id = entry.get('id').split('_')[-1]
        kanji_id = int(kanji_id, 16)
        content = ET.tostring(entry, encoding='unicode', xml_declaration=False)
        strokes[kanji_id] = svg_format.format(content=content, img_size=img_size)
    return strokes


def generate_dataset(data_dir, img_size):
    attributes = extract_attributes(data_dir)
    strokes = extract_strokes(data_dir, img_size)

    # Convert SVG strokes to PNG images and save on disk.
    img_dir = os.path.join(data_dir, 'images')
    Path(img_dir).mkdir(parents=True, exist_ok=True)
    new_attributes = dict()
    for kanji_id, strokes_i in tqdm(strokes.items()):
        if kanji_id not in attributes:
            continue
        img_path = os.path.join(img_dir, f'{kanji_id}.png')
        cairosvg.svg2png(bytestring=strokes_i.encode('utf-8'), write_to=img_path)
        new_attributes[kanji_id] = attributes[kanji_id]

    # Save kanji attributes to json file.
    filename = os.path.join(data_dir, 'attributes.json')
    with open(filename, 'w') as f:
        json.dump(new_attributes, f)
        
    print("Dataset generation completed.")


if __name__ == '__main__':
    generate_dataset(
        data_dir='data',
        img_size=128,
    )