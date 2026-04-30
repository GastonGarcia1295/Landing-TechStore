import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'(<img src=")data:image/[^;]+;base64,[^"]+("[^>]*class="ac-img"[^>]*>)'
matches = re.findall(pattern, content)
print(f'Found {len(matches)} accessories images')

images = [
    'ha280f89250dd4f39b29419d2f16c65a-788636b0c75eae56e417065493906427-1024-1024.webp', # CABLE TIPO C
    'Cable-Iphone-a-USB-Blanco-1-mt-1.jpg.webp', # CABLE TRADICIONAL
    '1161-producto-4-8963.jpg', # CABEZAL 20W
    '18-02c52ce80e4ba4d15617475088862381-1024-1024.webp' # CABLE USB-C
]

if len(matches) == 4:
    for i, img in enumerate(images):
        content = re.sub(pattern, r'\g<1>' + img + r'\g<2>', content, count=1)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Replaced successfully!')
else:
    print('Error: Did not find exactly 4 images.')
