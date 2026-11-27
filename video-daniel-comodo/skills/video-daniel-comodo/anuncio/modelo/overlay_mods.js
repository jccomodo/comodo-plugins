/* ===== Anúncio "Visita Marcada 1" (estilo B de ADS, STORY): copy animada + cartões de vidro ===== */
Object.assign(ICO,{
 chat:(c)=>`<path d="M14 18h72a8 8 0 018 8v40a8 8 0 01-8 8H44L24 90V74H14a8 8 0 01-8-8V26a8 8 0 018-8z" fill="${c}"/><circle cx="32" cy="46" r="6" fill="${OR}"/><circle cx="50" cy="46" r="6" fill="${OR}"/><circle cx="68" cy="46" r="6" fill="${OR}"/>`,
 funnel:(c)=>`<path d="M8 14h84L60 52v30l-20 10V52z" fill="${c}"/>`,
 cal:(c)=>`<rect x="10" y="18" width="80" height="72" rx="12" fill="${c}"/><rect x="10" y="18" width="80" height="22" rx="10" fill="${OR}"/><rect x="26" y="8" width="10" height="20" rx="5" fill="${c}"/><rect x="64" y="8" width="10" height="20" rx="5" fill="${c}"/><path d="M32 64l12 12 24-26" fill="none" stroke="${OR}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>`,
 coin:(c)=>`<circle cx="50" cy="50" r="42" fill="${c}"/><circle cx="50" cy="50" r="32" fill="none" stroke="${OR}" stroke-width="6"/><text x="50" y="62" text-anchor="middle" font-family="P" font-weight="900" font-size="34" fill="${OR}">R$</text>`,
 mega:(c)=>`<path d="M14 40h14l44-22v64L28 60H14z" fill="${c}"/><rect x="30" y="58" width="14" height="28" rx="5" fill="${c}"/><path d="M80 36q10 14 0 28" fill="none" stroke="${c}" stroke-width="7" stroke-linecap="round"/>`,
 x:(c)=>`<path d="M26 26l48 48M74 26L26 74" fill="none" stroke="${c}" stroke-width="13" stroke-linecap="round"/>`
});
const popK=(name,t)=>Math.max(0,g(name,t));
function popEl(el,name,t,x,y,s){const k=popK(name,t);el.setAttribute('transform',`translate(${x} ${y}) scale(${(s||1)*Math.min(k,1.1)})`);el.setAttribute('opacity',cl(k*1.7))}
function disc(s,r,fill,icon,icol,sc){const g_=SV(s,'g',{});SV(g_,'circle',{r,fill});const i=SV(g_,'g',{transform:`scale(${sc||r/62}) translate(-50 -50)`});i.innerHTML=ICO[icon](icol||WH);return g_}
const CY=1096,CH=300;
function card(root,h){glass(root,{left:px(CARD_X),top:px(CY),width:px(CARD_W),height:px(h||CH)});const L=content(root,CARD_X,CY,CARD_W,h||CH);return [L,svg(L,CARD_W,h||CH)]}
function label(L,x,y,w,txt,col,size){return D(L,{left:px(x-w/2),top:px(y),width:px(w),textAlign:'center',fontSize:px(size||30),fontWeight:700,color:col||'rgba(255,255,255,.95)',letterSpacing:'.04em',whiteSpace:'nowrap'},txt)}

/* 1 · "Empresário de planejados" */
kin('k1',[{words:[['empresário',0.00],['de',0.64]],size:110,color:WH},{words:[['planejados',0.84]],size:140,color:OR}],0.0,2.16,null,{W:800});

/* 2 · "dois, três, quatro, cinco mil ... todo mês": contador que sobe a cada número falado */
mod('c2',2.18,6.42,root=>{const [L,s]=card(root);
 const num=D(L,{left:'0px',top:'58px',width:px(CARD_W),textAlign:'center',fontSize:'150px',fontWeight:900,color:WH,lineHeight:'1',letterSpacing:'-.03em'},'');
 const T=[[2.74,'R$ 2 mil'],[3.32,'R$ 3 mil'],[3.94,'R$ 4 mil'],[4.54,'R$ 5 mil']];T.forEach((v,i)=>P('n'+i,0,[[v[0]-.05,1,.32,.6]]));
 const tm=D(L,{left:px(CARD_W/2-150),top:'214px',width:'300px',height:'60px',lineHeight:'60px',borderRadius:'30px',background:OR,color:WH,textAlign:'center',fontSize:'32px',fontWeight:700},'todo mês');P('tm',0,[[5.90,1,.38,.7]]);
 return t=>{let cur=-1;T.forEach((v,i)=>{if(t>=v[0]-.05)cur=i});if(cur<0){num.style.opacity=0;tm.style.opacity=0;return}
  const k=popK('n'+cur,t);num.textContent=T[cur][1];num.style.opacity=cl(k*2);num.style.transform=`translateY(${(1-Math.min(k,1))*20}px) scale(${lerp(.9,1,Math.min(k,1.06))})`;num.style.color=cur==3?OR:WH;
  const kt=popK('tm',t);tm.style.opacity=cl(kt*1.7);tm.style.transform=`scale(${Math.min(kt,1.08)})`}});

/* 3 · "em tráfego pago" */
kin('k3',[{words:[['em',6.48],['tráfego',6.70]],size:120,color:WH},{words:[['pago',7.04]],size:170,color:OR}],6.44,7.68,null,{W:700,cap:190});

/* 4 · "quantos clientes entraram na sua loja por causa disso?" */
mod('c4',8.56,12.42,root=>{const [L,s]=card(root);const ux=[150,275,400];
 const us=ux.map((x,i)=>{const g_=disc(s,56,'rgba(255,255,255,.92)','user','#8E8E93',.8);P('u'+i,0,[[9.98+i*.12,1,.42,.7]]);return g_});
 const ar=SV(s,'path',{d:'M480 130 H590 M566 106 L594 130 L566 154',fill:'none',stroke:WH,'stroke-width':9,'stroke-linecap':'round','stroke-linejoin':'round'});P('a4',0,[[10.50,1,.4,1]]);
 const st=disc(s,84,OR,'store',WH,1.1);P('st',0,[[11.20,1,.42,.7]]);
 const q=SV(s,'text',{x:0,y:0,'text-anchor':'middle','font-family':'P','font-weight':900,'font-size':110,fill:WH});q.textContent='?';P('q',0,[[11.86,1,.38,.55]]);
 const l1=label(L,275,222,300,'clientes'),l2=label(L,700,234,200,'loja');
 return t=>{us.forEach((g_,i)=>popEl(g_,'u'+i,t,ux[i],130));l1.style.opacity=cl(popK('u0',t)*1.7);ar.setAttribute('opacity',cl(g('a4',t)));
  popEl(st,'st',t,700,124);l2.style.opacity=cl(popK('st',t)*1.7);const kq=popK('q',t);q.setAttribute('transform',`translate(${812} ${96}) scale(${Math.min(kq,1.12)})`);q.setAttribute('opacity',cl(kq*1.7))}});

/* 5 · "mais ou menos" */
kin('k5',[{words:[['mais',13.98],['ou',14.30],['menos',14.52]],size:150,color:OR}],13.92,14.96,null,{W:760,cap:170});

/* 6 · "uma despesa fixa" */
kin('k6',[{words:[['uma',18.28],['despesa',18.48]],size:120,color:WH},{words:[['fixa',18.86]],size:200,color:OR}],18.24,19.58,null,{W:700,cap:210});

/* 7 · "a maioria das agências entrega lead e para por aí" */
mod('c7',22.50,27.12,root=>{const [L,s]=card(root);
 const ag=disc(s,70,'rgba(255,255,255,.92)','mega','#17130F',.9);P('ag',0,[[24.50,1,.42,.7]]);
 const ld=disc(s,62,OR,'user',WH,.85);P('ld',0,[[25.42,1,.42,.7]]);
 const ar=SV(s,'path',{d:'M290 130 H430',fill:'none',stroke:WH,'stroke-width':10,'stroke-linecap':'round'});const AL=140;P('ar',0,[[24.96,1,.5,1]]);
 const gap=SV(s,'path',{d:'M600 130 H800',fill:'none',stroke:'rgba(255,255,255,.55)','stroke-width':8,'stroke-linecap':'round','stroke-dasharray':'4 18'});
 const xx=disc(s,40,'#E5322B','x',WH,.5);P('xx',0,[[26.12,1,.34,.55]]);
 const l1=label(L,200,224,240,'agências'),l2=label(L,520,224,200,'lead');
 return t=>{popEl(ag,'ag',t,200,130);popEl(ld,'ld',t,520,130);const ka=cl(g('ar',t));ar.style.strokeDasharray=AL;ar.style.strokeDashoffset=AL*(1-ka);ar.setAttribute('opacity',ka>0?1:0);
  const kx=popK('xx',t);gap.setAttribute('opacity',cl(kx*1.7));popEl(xx,'xx',t,700,130);l1.style.opacity=cl(popK('ag',t)*1.7);l2.style.opacity=cl(popK('ld',t)*1.7)}});

/* 8 · "é você e a sua equipe" */
kin('k8',[{words:[['é',33.22],['você',33.44]],size:130,color:WH},{words:[['e',33.96],['a',34.16],['sua',34.28],['equipe',34.40]],size:120,color:OR}],33.18,35.20,null,{W:760});

/* 9 · "o seu tempo vai embora com gente que no fim não fecha" */
mod('c9',35.22,38.60,root=>{const [L,s]=card(root);
 const ck=SV(s,'g',{});SV(ck,'circle',{r:96,fill:'rgba(255,255,255,.92)'});const arc=SV(ck,'path',{d:'',fill:'none',stroke:OR,'stroke-width':16,'stroke-linecap':'round'});
 const hand=SV(ck,'path',{d:'M0 0V-62',stroke:'#17130F','stroke-width':10,'stroke-linecap':'round'});SV(ck,'circle',{r:10,fill:'#17130F'});P('ck',0,[[35.46,1,.42,.7]]);P('ar9',0,[[35.50,1,2.0,1]]);
 const u=disc(s,62,'rgba(255,255,255,.92)','user','#8E8E93',.85);P('u9',0,[[36.56,1,.42,.7]]);
 const xx=disc(s,30,'#E5322B','x',WH,.38);P('x9',0,[[37.42,1,.34,.55]]);
 return t=>{popEl(ck,'ck',t,300,150);const ka=cl(g('ar9',t));arc.setAttribute('d',arcPath(0,0,80,ka));hand.setAttribute('transform',`rotate(${ka*360})`);
  popEl(u,'u9',t,620,150);popEl(xx,'x9',t,676,96)}});

/* 10 · "a gente faz diferente" */
kin('k10',[{words:[['a',43.46],['gente',43.54],['faz',43.68]],size:120,color:WH},{words:[['diferente',43.90]],size:170,color:OR}],43.42,44.96,null,{W:780});

/* 11 · "atende todo o lead · filtra quem tem perfil · entrega a visita agendada no seu showroom" */
mod('c11',45.04,51.48,root=>{const [L,s]=card(root);const xs=[165,450,735],cy=124;
 const it=[['chat',45.06,'atende'],['funnel',47.14,'filtra'],['cal',49.46,'visita']].map(([ic,t0,lb],i)=>{const g_=disc(s,72,i==2?OR:'rgba(255,255,255,.92)',ic,i==2?WH:'#17130F',.92);P('i'+i,0,[[t0,1,.42,.7]]);return [g_,label(L,xs[i],222,220,lb)]});
 const a1=SV(s,'path',{d:`M${xs[0]+90} ${cy} H${xs[1]-90}`,fill:'none',stroke:'rgba(255,255,255,.8)','stroke-width':8,'stroke-linecap':'round'}),a2=SV(s,'path',{d:`M${xs[1]+90} ${cy} H${xs[2]-90}`,fill:'none',stroke:'rgba(255,255,255,.8)','stroke-width':8,'stroke-linecap':'round'});
 P('a1',0,[[46.90,1,.4,1]]);P('a2',0,[[49.20,1,.4,1]]);const AL=xs[1]-xs[0]-180;
 const ck=disc(s,26,'#2BB24C','check',WH,.36);P('ck11',0,[[50.66,1,.34,.55]]);
 return t=>{it.forEach(([g_,lb],i)=>{popEl(g_,'i'+i,t,xs[i],cy);lb.style.opacity=cl(popK('i'+i,t)*1.7)});
  [[a1,'a1'],[a2,'a2']].forEach(([a,n])=>{const k=cl(g(n,t));a.style.strokeDasharray=AL;a.style.strokeDashoffset=AL*(1-k);a.setAttribute('opacity',k>0?1:0)});popEl(ck,'ck11',t,xs[2]+58,cy-58)}});

/* 12 · "fechar a venda" */
kin('k12',[{words:[['fechar',56.38]],size:150,color:WH},{words:[['a',56.74],['venda',56.88]],size:150,color:OR}],56.34,57.14,null,{W:700,cap:180});

/* 13 · "deixa de ser um gasto e vira um canal ... faturamento consistente todos os meses" */
mod('c13',57.16,63.98,root=>{const [L,s]=card(root);
 const co=disc(s,62,'rgba(255,255,255,.92)','coin','#17130F',.8);P('co',0,[[58.98,1,.42,.7]]);
 const ar=SV(s,'path',{d:'M240 150 H330 M306 126 L334 150 L306 174',fill:'none',stroke:WH,'stroke-width':9,'stroke-linecap':'round','stroke-linejoin':'round'});P('a13',0,[[59.50,1,.4,1]]);
 const base=SV(s,'path',{d:'M400 246 H830',stroke:'rgba(255,255,255,.6)','stroke-width':5,'stroke-linecap':'round'});
 const hs=[70,110,150,190],bars=hs.map((h,i)=>{const r=SV(s,'rect',{x:430+i*100,width:64,rx:14,fill:i==3?OR:'rgba(255,255,255,.92)'});P('b'+i,0,[[61.08+i*.38,1,.5,.75]]);return [r,h]});
 const l1=label(L,170,224,200,'gasto'),l2=label(L,615,262,300,'faturamento',WH,26);
 return t=>{popEl(co,'co',t,170,140);l1.style.opacity=cl(popK('co',t)*1.7);const ka=cl(g('a13',t));ar.setAttribute('opacity',ka);
  base.setAttribute('opacity',cl(popK('b0',t)*3)*.9);bars.forEach(([r,h],i)=>{const k=Math.max(0,g('b'+i,t));const hh=h*Math.min(k,1.05);r.setAttribute('y',240-hh);r.setAttribute('height',Math.max(hh,0.01));r.setAttribute('opacity',k>0.01?1:0)});l2.style.opacity=cl(popK('b0',t)*1.7)}});
