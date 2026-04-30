import re
import base64
import os
from rembg import remove

def process():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Fix the text
    html = html.replace('16 Pro y Pro Max', '16 Plus, Pro y Pro Max')

    # 2. Find avif base64 images (iPhone 13)
    matches_avif = re.findall(r'<img src="(data:image/avif;base64,([^"]+))" alt="(iPhone \d+)"', html)
    print(f'Found {len(matches_avif)} AVIF iPhone images.')

    for original_src, b64_data, alt_text in matches_avif:
        out_filename = alt_text.replace(' ', '_').lower() + '_nobg.png'
        print(f'Processing {alt_text}...')
        image_data = base64.b64decode(b64_data)
        
        # Remove background
        nobg_data = remove(image_data, alpha_matting=True, alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=10, alpha_matting_erode_size=10)
        
        with open(out_filename, 'wb') as out_file:
            out_file.write(nobg_data)
            
        print(f'Updating HTML for {alt_text}...')
        html = html.replace(f'src="{original_src}"', f'src="{out_filename}"')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Done.')

if __name__ == '__main__':
    process()
