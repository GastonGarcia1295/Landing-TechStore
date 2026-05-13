// NAV
document.getElementById('menu-btn').addEventListener('click',()=>document.getElementById('mobile-menu').classList.toggle('open'));
document.querySelectorAll('#mobile-menu a').forEach(a=>a.addEventListener('click',()=>document.getElementById('mobile-menu').classList.remove('open')));
window.addEventListener('scroll',()=>document.getElementById('nav').classList.toggle('scrolled',scrollY>20));

// ── SAND PARTICLES ────────────────────────────────────────────
(function(){
  const cv=document.getElementById('sand-canvas');
  const ctx=cv.getContext('2d');
  let W,H,grains=[];
  let mx=innerWidth/2,my=innerHeight/2;

  function resize(){W=cv.width=innerWidth;H=cv.height=innerHeight}
  resize();window.addEventListener('resize',()=>{resize();initGrains()});
  document.addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY});

  function mkGrain(){
    return{
      x:Math.random()*W,y:Math.random()*H,
      vx:(Math.random()-.5)*.4,vy:(Math.random()-.5)*.4,
      r:Math.random()*1.8+.3,
      alpha:Math.random()*.25+.05,
      life:Math.random(),decay:Math.random()*.0025+.0008,
      wobble:Math.random()*Math.PI*2,
      wobbleSpeed:Math.random()*.018+.004
    };
  }
  function initGrains(){grains=[];for(let i=0;i<200;i++){const g=mkGrain();g.life=Math.random();grains.push(g)}}
  initGrains();

  function draw(){
    ctx.clearRect(0,0,W,H);
    grains.forEach((g,i)=>{
      // wobble drift
      g.wobble+=g.wobbleSpeed;
      g.vx+=Math.sin(g.wobble)*.01;
      g.vy+=Math.cos(g.wobble*.7)*.008;

      // repel from cursor
      const dx=mx-g.x,dy=my-g.y,d=Math.sqrt(dx*dx+dy*dy);
      if(d<180){const f=(180-d)/180;g.vx-=(dx/d)*f*.7;g.vy-=(dy/d)*f*.7}

      // speed limit
      const sp=Math.sqrt(g.vx*g.vx+g.vy*g.vy);
      if(sp>1.8){g.vx*=1.8/sp;g.vy*=1.8/sp}
      g.vx*=.97;g.vy*=.97;
      g.x+=g.vx;g.y+=g.vy;
      if(g.x<0)g.x=W;if(g.x>W)g.x=0;if(g.y<0)g.y=H;if(g.y>H)g.y=0;

      // fade in/out life cycle
      g.life-=g.decay;
      if(g.life<=0){grains[i]=mkGrain();return}
      const fade=g.life<.2?g.life/.2:1;

      // draw grain — warm sand color
      const hue=30+Math.random()*10;
      ctx.beginPath();ctx.arc(g.x,g.y,g.r,0,Math.PI*2);
      ctx.fillStyle=`hsla(${hue},40%,75%,${(g.alpha*fade).toFixed(3)})`;
      ctx.fill();

      // faint connection lines
      grains.forEach((g2,j)=>{
        if(j<=i)return;
        const dd=Math.hypot(g.x-g2.x,g.y-g2.y);
        if(dd<80){
          ctx.beginPath();ctx.moveTo(g.x,g.y);ctx.lineTo(g2.x,g2.y);
          ctx.strokeStyle=`rgba(200,180,140,${((1-dd/80)*.04).toFixed(3)})`;
          ctx.lineWidth=.5;ctx.stroke();
        }
      });
    });
    requestAnimationFrame(draw);
  }
  draw();
})();

// ── SCROLL REVEAL ─────────────────────────────────────────────
const obs=new IntersectionObserver(es=>es.forEach(e=>{
  if(e.isIntersecting){e.target.classList.add('visible');obs.unobserve(e.target)}
}),{threshold:.08});
document.querySelectorAll('.reveal').forEach(el=>obs.observe(el));

// ── 3D TILT PHONE CARDS ───────────────────────────────────────
document.querySelectorAll('.phone-card').forEach(card=>{
  card.addEventListener('mousemove',e=>{
    const r=card.getBoundingClientRect();
    const x=(e.clientX-r.left)/r.width-.5;
    const y=(e.clientY-r.top)/r.height-.5;
    card.style.transform=`perspective(800px) rotateX(${(-y*12).toFixed(1)}deg) rotateY(${(x*12).toFixed(1)}deg) translateY(-8px) scale(1.02)`;
    card.style.boxShadow=`${(x*20).toFixed(0)}px ${(y*20+24).toFixed(0)}px 48px rgba(0,0,0,.13)`;
  });
  card.addEventListener('mouseleave',()=>{card.style.transform='';card.style.boxShadow=''});
});

// ── MAGNETIC SPOTLIGHT ON TRUST & REVIEW BOXES ───────────────
document.querySelectorAll('.trust-box,.review-card').forEach(box=>{
  box.addEventListener('mousemove',e=>{
    const r=box.getBoundingClientRect();
    box.style.setProperty('--mx',((e.clientX-r.left)/r.width*100)+'%');
    box.style.setProperty('--my',((e.clientY-r.top)/r.height*100)+'%');
  });
});

// acc spotlight
document.querySelectorAll('.ac').forEach(c=>{
  c.addEventListener('mousemove',e=>{
    const r=c.getBoundingClientRect();
    c.style.setProperty('--mx',((e.clientX-r.left)/r.width*100)+'%');
    c.style.setProperty('--my',((e.clientY-r.top)/r.height*100)+'%');
  });
});
// acc sand canvas
(function(){
  const cv=document.getElementById('accCvs');
  if(!cv)return;
  const ctx=cv.getContext('2d');
  const sec=document.getElementById('accesorios');
  let amx=0,amy=0,G=[];
  function rsz(){cv.width=sec.offsetWidth;cv.height=sec.offsetHeight}
  rsz();window.addEventListener('resize',()=>{rsz();init()});
  document.addEventListener('mousemove',e=>{
    const r=sec.getBoundingClientRect();amx=e.clientX-r.left;amy=e.clientY-r.top;
  });
  function mk(){return{x:Math.random()*cv.width,y:Math.random()*cv.height,
    vx:(Math.random()-.5)*.45,vy:(Math.random()-.5)*.45,
    r:Math.random()*1.8+.3,alpha:Math.random()*.28+.07,
    life:Math.random(),decay:Math.random()*.002+.0007,
    wb:Math.random()*Math.PI*2,ws:Math.random()*.02+.004};}
  function init(){G=[];for(let i=0;i<180;i++){const g=mk();g.life=Math.random();G.push(g)}}
  init();
  function draw(){
    ctx.clearRect(0,0,cv.width,cv.height);
    G.forEach((g,i)=>{
      g.wb+=g.ws;
      g.vx+=Math.sin(g.wb)*.012;g.vy+=Math.cos(g.wb*.7)*.009;
      const dx=amx-g.x,dy=amy-g.y,d=Math.sqrt(dx*dx+dy*dy);
      if(d<170){const f=(170-d)/170;g.vx-=(dx/d)*f*.85;g.vy-=(dy/d)*f*.85}
      const sp=Math.sqrt(g.vx*g.vx+g.vy*g.vy);
      if(sp>2){g.vx*=2/sp;g.vy*=2/sp}
      g.vx*=.97;g.vy*=.97;g.x+=g.vx;g.y+=g.vy;
      if(g.x<0)g.x=cv.width;if(g.x>cv.width)g.x=0;
      if(g.y<0)g.y=cv.height;if(g.y>cv.height)g.y=0;
      g.life-=g.decay;
      if(g.life<=0){G[i]=mk();return}
      const fade=g.life<.18?g.life/.18:1;
      ctx.beginPath();ctx.arc(g.x,g.y,g.r,0,Math.PI*2);
      ctx.fillStyle=`rgba(210,175,105,${(g.alpha*fade).toFixed(3)})`;ctx.fill();
    });
    requestAnimationFrame(draw);
  }
  draw();
})();


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
    dot.style.transform = `translate(calc(${mouseX}px - 50%), calc(${mouseY}px - 50%))`;
  });

  // Lerp ring
  function renderCursor() {
    ringX += (mouseX - ringX) * 0.15;
    ringY += (mouseY - ringY) * 0.15;
    ring.style.transform = `translate(calc(${ringX}px - 50%), calc(${ringY}px - 50%))`;
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
 
