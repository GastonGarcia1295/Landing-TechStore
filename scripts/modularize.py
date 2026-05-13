import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract styles
styles = re.findall(r'<style>(.*?)</style>', content, re.DOTALL)
with open('style.css', 'w', encoding='utf-8') as f:
    for s in styles:
        f.write(s.strip() + '\n\n')

# Extract scripts
scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
with open('script.js', 'w', encoding='utf-8') as f:
    # First script is tailwind config, which is fine to keep in index.html, but let's check
    # Wait, the first script might have tailwind config. Let's see all scripts.
    # The tailwind config script should stay in HTML or go to script.js? It's better to keep tailwind.config in head script.
    # Or just extract all except tailwind.config.
    pass

def repl_style(match):
    return ''
def repl_script(match):
    # keep if it contains tailwind.config
    if 'tailwind.config' in match.group(0):
        return match.group(0)
    return ''

# Let's extract the non-tailwind scripts to script.js
js_content = ""
for s in scripts:
    if 'tailwind.config' not in s:
        js_content += s.strip() + '\n\n'

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

# Remove the extracted tags
new_content = re.sub(r'<style>.*?</style>', repl_style, content, flags=re.DOTALL)
new_content = re.sub(r'<script>.*?</script>', repl_script, new_content, flags=re.DOTALL)

# Add links to head and body end
new_content = new_content.replace('</head>', '  <link rel="stylesheet" href="style.css">\n</head>')
new_content = new_content.replace('</body>', '  <script src="script.js"></script>\n</body>')

# Remove any empty script tags that might have been left if there were any, wait, my repl_script returns '' so it completely removes the tag.

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Modularization complete!")
