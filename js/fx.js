/* bashframes fx — vanilla, no deps. Page works without it. */
(function(){
var d=document,w=window,R=d.documentElement,B=d.body;
if(!B||!w.matchMedia||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
var $=function(s){return d.querySelectorAll(s)},vib=function(n){try{navigator.vibrate&&navigator.vibrate(n)}catch(e){}};
/* REC dot */
var hb=d.querySelector('.hud b');if(hb){var r=d.createElement('i');r.className='fx-rec';hb.parentNode.insertBefore(r,hb)}
/* 1 boot, once per session */
var ss;try{ss=sessionStorage}catch(e){}
if(!(ss&&ss.fxBoot)||/fxboot/.test(location.hash)){
 try{ss&&(ss.fxBoot=1)}catch(e){}
 var els=[].slice.call($('.profile,.feature,.group-head,.button-stack>.button,footer'));
 els.forEach(function(e,i){e.classList.add('fx-up');e.style.setProperty('--fx-d',(120+i*60)+'ms')});
 R.classList.add('fx-boot');
 setTimeout(function(){R.classList.remove('fx-boot');els.forEach(function(e){e.classList.remove('fx-up')})},1150);
}
/* 2 parallax */
var tx=0,ty=0,cx=0,cy=0,raf=0,S=R.style,MAX=7;
function loop(){cx+=(tx-cx)*.12;cy+=(ty-cy)*.12;
 S.setProperty('--fx-fx',(cx*.5).toFixed(2)+'px');S.setProperty('--fx-fy',(cy*.5).toFixed(2)+'px');
 S.setProperty('--fx-bx',(-cx).toFixed(2)+'px');S.setProperty('--fx-by',(-cy*.6).toFixed(2)+'px');
 S.setProperty('--fx-ix',(cx).toFixed(2)+'px');S.setProperty('--fx-iy',(cy).toFixed(2)+'px');
 raf=Math.abs(tx-cx)+Math.abs(ty-cy)>.02?requestAnimationFrame(loop):0}
function aim(x,y){tx=Math.max(-1,Math.min(1,x))*MAX;ty=Math.max(-1,Math.min(1,y))*MAX;R.classList.add('fx-px');raf||(raf=requestAnimationFrame(loop))}
var gotTilt=0;
w.addEventListener('deviceorientation',function(e){if(e.gamma==null)return;gotTilt=1;aim(e.gamma/30,(e.beta-45)/30)});
if(matchMedia('(hover: hover) and (pointer: fine)').matches)
 w.addEventListener('mousemove',function(e){gotTilt||aim(e.clientX/innerWidth*2-1,e.clientY/innerHeight*2-1)},{passive:true});
/* iOS 13+ permission on first gesture */
function perm(){d.removeEventListener('click',perm,true);
 [w.DeviceOrientationEvent,w.DeviceMotionEvent].forEach(function(E){
  if(E&&typeof E.requestPermission=='function')try{E.requestPermission().catch(function(){})}catch(e){}})}
d.addEventListener('click',perm,true);
/* 3 tap-to-focus + 4 haptics */
d.addEventListener('pointerdown',function(e){
 var t=e.target.closest&&e.target.closest('.button,.fbtn,.feature-media,a');if(!t)return;
 var b=t.getBoundingClientRect(),f=d.createElement('div');f.className='fx-af';
 f.style.cssText='left:'+(b.left-3)+'px;top:'+(b.top-3)+'px;width:'+(b.width+6)+'px;height:'+(b.height+6)+'px';
 f.innerHTML='<i></i><i></i><i></i><i></i>';B.appendChild(f);setTimeout(function(){f.remove()},220);vib(8)},{passive:true});
var tk=d.querySelector('.tk-track');tk&&tk.addEventListener('animationiteration',function(){vib(3)});
/* 5 shake / 'bars' */
var on=0,last=0,buf='';
function bars(){if(on)return;on=1;vib([8,40,8]);var o=d.createElement('div'),c=function(a){return '<div>'+a.map(function(x){return '<span style="background:'+x+'"></span>'}).join('')+'</div>'};
 o.className='fx-bars';o.setAttribute('aria-hidden','true');
 o.innerHTML=c(['#c0c0c0','#c0c000','#00c0c0','#00c000','#c000c0','#c00000','#0000c0'])+c(['#0000c0','#131313','#c000c0','#131313','#00c0c0','#131313','#c0c0c0'])+c(['#00214c','#fff','#32006a','#131313','#090909','#131313','#1d1d1d'])+'<b>BF-00 / TEST SIGNAL</b>';
 B.appendChild(o);setTimeout(function(){o.remove();on=0},1200)}
w.fxBars=bars;
w.addEventListener('devicemotion',function(e){var a=e.acceleration||{},m=Math.abs(a.x||0)+Math.abs(a.y||0)+Math.abs(a.z||0),n=Date.now();
 if(m>32&&n-last>1500){last=n;bars()}});
d.addEventListener('keydown',function(e){if(e.key&&e.key.length==1){buf=(buf+e.key.toLowerCase()).slice(-4);buf=='bars'&&bars()}});
})();
