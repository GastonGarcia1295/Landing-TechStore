import os

def inject_premium_ui():
    # 1. Update index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    html_additions = """
<div id="preloader" class="preloader">
  <div class="loader-text">TECH STORE</div>
</div>
<div id="scroll-progress" class="scroll-progress"></div>
<div class="cursor-dot" id="cursor-dot"></div>
<div class="cursor-ring" id="cursor-ring"></div>
<div class="grain-overlay"></div>
"""
    if '<div id="preloader"' not in html:
        html = html.replace('<body>', '<body>\n' + html_additions)

    # Make "WhatsApp" and other big buttons magnetic
    html = html.replace('class="btn btn-orange', 'class="btn btn-orange magnetic')
    html = html.replace('class="ac-btn"', 'class="ac-btn magnetic"')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    # 2. Update style.css
    with open('style.css', 'r', encoding='utf-8') as f:
        css = f.read()

    css_additions = """
/* ── PREMIUM UI ELEMENTS ───────────────────────────── */
body, a, button, .btn, .ac-btn, .nav-link { cursor: none !important; }

/* Preloader */
.preloader {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: #000; z-index: 99999;
  display: flex; align-items: center; justify-content: center;
  transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.8s;
}
.preloader.hidden { opacity: 0; visibility: hidden; }
.loader-text {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 3rem; color: #fff; letter-spacing: 4px;
  animation: pulseLoader 1.5s infinite alternate;
}
@keyframes pulseLoader { 0% { opacity: 0.3; transform: scale(0.98); } 100% { opacity: 1; transform: scale(1); } }

/* Scroll Progress */
.scroll-progress {
  position: fixed; top: 0; left: 0; height: 3px; background: #FF9900;
  width: 0%; z-index: 99998; pointer-events: none;
  transition: width 0.1s ease-out;
  box-shadow: 0 0 10px rgba(255,153,0,0.5);
}

/* Custom Cursor */
.cursor-dot {
  position: fixed; top: 0; left: 0; width: 6px; height: 6px;
  background: #FF9900; border-radius: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none; z-index: 100000;
  transition: width 0.2s, height 0.2s, background 0.2s;
}
.cursor-ring {
  position: fixed; top: 0; left: 0; width: 36px; height: 36px;
  border: 1px solid rgba(255,153,0,0.5); border-radius: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none; z-index: 99999;
  transition: width 0.3s, height 0.3s, border-color 0.3s;
}
.cursor-hover .cursor-dot { width: 40px; height: 40px; background: rgba(255,153,0,0.1); border: 1px solid rgba(255,153,0,0.3); mix-blend-mode: difference; }
.cursor-hover .cursor-ring { width: 60px; height: 60px; border-color: transparent; }

/* Grain Overlay */
.grain-overlay {
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  pointer-events: none; z-index: 99997; opacity: 0.05;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
}

/* Magnetic Items */
.magnetic { display: inline-block; transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
"""
    if '.cursor-dot' not in css:
        with open('style.css', 'a', encoding='utf-8') as f:
            f.write(css_additions)

    # 3. Update script.js
    with open('script.js', 'r', encoding='utf-8') as f:
        js = f.read()

    js_additions = """
// ── PREMIUM UI LOGIC ──────────────────────────────────────────

// Preloader
window.addEventListener('load', () => {
  setTimeout(() => {
    document.getElementById('preloader')?.classList.add('hidden');
  }, 500);
});

// Scroll Progress
window.addEventListener('scroll', () => {
  const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
  const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  const scrolled = (winScroll / height) * 100;
  const progress = document.getElementById('scroll-progress');
  if(progress) progress.style.width = scrolled + '%';
});

// Custom Cursor & Magnetic Buttons
(function(){
  const dot = document.getElementById('cursor-dot');
  const ring = document.getElementById('cursor-ring');
  if(!dot || !ring) return;

  let mouseX = window.innerWidth/2, mouseY = window.innerHeight/2;
  let ringX = mouseX, ringY = mouseY;
  
  // Track mouse
  window.addEventListener('mousemove', e => {
    mouseX = e.clientX; mouseY = e.clientY;
    dot.style.transform = `translate(${mouseX}px, ${mouseY}px)`;
  });

  // Lerp ring
  function renderCursor() {
    ringX += (mouseX - ringX) * 0.15;
    ringY += (mouseY - ringY) * 0.15;
    ring.style.transform = `translate(${ringX}px, ${ringY}px)`;
    requestAnimationFrame(renderCursor);
  }
  renderCursor();

  // Hover states
  document.querySelectorAll('a, button, .btn, .ac-btn, .nav-link').forEach(el => {
    el.addEventListener('mouseenter', () => document.body.classList.add('cursor-hover'));
    el.addEventListener('mouseleave', () => document.body.classList.add('cursor-hover'));
    el.addEventListener('mouseleave', () => document.body.classList.remove('cursor-hover'));
  });

  // Magnetic effect
  document.querySelectorAll('.magnetic').forEach(btn => {
    btn.addEventListener('mousemove', e => {
      const rect = btn.getBoundingClientRect();
      const h = rect.width / 2;
      const v = rect.height / 2;
      const x = e.clientX - rect.left - h;
      const y = e.clientY - rect.top - v;
      btn.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.transform = `translate(0px, 0px)`;
    });
  });
})();
"""
    if 'PREMIUM UI LOGIC' not in js:
        with open('script.js', 'a', encoding='utf-8') as f:
            f.write(js_additions)

if __name__ == '__main__':
    inject_premium_ui()
