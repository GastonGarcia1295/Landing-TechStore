import re
import base64
import os
from rembg import remove

def process_images():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Find all base64 webp images in the HTML
    matches = re.findall(r'<img src="(data:image/webp;base64,([^"]+))" alt="(iPhone \d+)"', html)
    print(f'Found {len(matches)} iPhone images.')

    for original_src, b64_data, alt_text in matches:
        filename = alt_text.replace(' ', '_').lower() + '.webp'
        out_filename = alt_text.replace(' ', '_').lower() + '_nobg.png'
        
        print(f'Processing {alt_text}...')
        # Decode base64
        image_data = base64.b64decode(b64_data)
        
        # Remove background using alpha matting
        print('Removing background...')
        nobg_data = remove(image_data, alpha_matting=True, alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=10, alpha_matting_erode_size=10)
        
        # Save output image
        with open(out_filename, 'wb') as out_file:
            out_file.write(nobg_data)
        
        # Replace the base64 src in HTML with the new transparent image
        print(f'Updating HTML for {alt_text}...')
        html = html.replace(f'src="{original_src}"', f'src="{out_filename}"')

    # Also replace any jpg base64 if present
    matches_jpg = re.findall(r'<img src="(data:image/jpeg;base64,([^"]+))" alt="(iPhone \d+)"', html)
    print(f'Found {len(matches_jpg)} JPEG iPhone images.')
    for original_src, b64_data, alt_text in matches_jpg:
        out_filename = alt_text.replace(' ', '_').lower() + '_nobg.png'
        print(f'Processing {alt_text}...')
        image_data = base64.b64decode(b64_data)
        nobg_data = remove(image_data, alpha_matting=True, alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=10, alpha_matting_erode_size=10)
        with open(out_filename, 'wb') as out_file:
            out_file.write(nobg_data)
        html = html.replace(f'src="{original_src}"', f'src="{out_filename}"')


    # Save updated HTML
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Done.')

if __name__ == '__main__':
    process_images()
