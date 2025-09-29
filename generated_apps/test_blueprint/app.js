
// Blueprint-driven SPA renderer
const BP = window.__BLUEPRINT__ || { routes: [] };
const SAMPLE = window.__SAMPLE__ || {};
const state = JSON.parse(localStorage.getItem('bp_state')||'{}');
if(!state.currentUser){ state.currentUser = (SAMPLE.users&&SAMPLE.users[0]) || {username:'you', name:'คุณ'}; }
state.users = state.users || SAMPLE.users || [state.currentUser];
state.posts = state.posts || SAMPLE.posts || [];
state.notifications = state.notifications || SAMPLE.notifications || [];
state.messages = state.messages || SAMPLE.messages || [];
state.collections = state.collections || SAMPLE.collections || {}; // arbitrary named datasets
save();

function save(){ localStorage.setItem('bp_state', JSON.stringify(state)); }
function h(html){ const d=document.createElement('div'); d.innerHTML=html.trim(); return d.firstChild; }
function routeMap(){ const map={}; (BP.routes||[]).forEach(r=>{ map[r.path||'#/']=r; }); return map; }
const routes = routeMap();

function router(){ const hash=(location.hash||Object.keys(routes)[0]||'#/').replace('#',''); const full='#'+hash; const r=routes[full] || routes['#/'] || {components:[{type:'text',value:'ไม่พบหน้า'}]}; renderRoute(r); }
window.addEventListener('hashchange',router); window.addEventListener('load',router);

function renderRoute(r){ const app=document.getElementById('app'); app.innerHTML=''; const cont=h('<div class="container"></div>');
    (r.components||[]).forEach(c=> cont.appendChild(renderComponent(c)) );
    app.appendChild(cont);
}

function renderComponent(c){ const t=(c.type||'text').toLowerCase();
    if(t==='text'){ return h(`<div class="card">${escapeHtml(c.value||'')}</div>`); }
    if(t==='image'){ const el=h('<div class="card"></div>'); const im=new Image(); im.src=c.src||''; el.appendChild(im); return el; }
        if(t==='link'){ const el=h(`<a href="${c.to||'#/'}" class="card">${escapeHtml(c.label||'ลิงก์')}</a>`); el.onclick=(e)=>{ if(el.getAttribute('href').startsWith('#')){ e.preventDefault(); navigate(c.to||'#/'); } }; return el; }
        if(t==='button'){ const el=h(`<button>${escapeHtml(c.label||'ปุ่ม')}</button>`); el.onclick=()=>handleAction(c.action||'navigate', c); return el; }
        if(t==='list'){ const el=h('<ul class="card"></ul>'); const items = bindItems(c); items.forEach(it=> el.appendChild(h(`<li>${escapeHtml(String(it))}</li>`))); return el; }
        if(t==='table'){ return renderTable(c); }
    if(t==='grid'){ const el=h('<div class="grid"></div>'); const imgs=(state.posts||[]).map(p=>p.img).filter(Boolean); imgs.forEach(src=>{ const im=new Image(); im.src=src; el.appendChild(im); }); return el; }
        if(t==='form'){ return renderForm(c); }
        if(t==='composer'){ return renderComposer(c); }
    if(t==='inbox'){ return renderInbox(); }
    if(t==='notifications'){ return renderNotifications(); }
    if(t==='profile'){ return renderProfile(); }
    if(t==='feed'){ return renderFeed(); }
    if(t==='todo'){ return renderTodo(); }
    return h(`<div class="card">[${t}]</div>`);
}

function navigate(path){ location.hash = path; }
function escapeHtml(s){ return (s||'').replace(/[&<>"]+/g, m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m])); }

function handleAction(action, cfg){
    if(action==='navigate'){ navigate(cfg.to||'#/'); return; }
    if(action==='submit'){ const formId = cfg.formId||'__active_form'; const form = document.getElementById(formId) || cfg.__formEl; if(!form){ return; }
        const data={}; [...form.querySelectorAll('input,textarea,select')].forEach(el=> data[el.name||el.id||el.placeholder||'field'] = el.type==='file'? (el.files&&el.files[0]) : el.value);
        // bind to target collection
        const coll = cfg.collection || 'posts';
        if(coll){ state.collections[coll] = state.collections[coll]||[]; state.collections[coll].push({...data, id: Date.now()}); save(); if(cfg.redirect){ navigate(cfg.redirect); } else { router(); } }
        return;
    }
}

function bindItems(c){
    if(c.items){ return c.items; }
    if(c.collection){ const coll = state.collections[c.collection] || []; const field=c.field||'name'; return coll.map(x=>x[field]??JSON.stringify(x)); }
    return [];
}

function renderTable(c){ const cols = c.columns||[]; const rows = c.rows || (c.collection? (state.collections[c.collection]||[]) : []);
    const el=h('<div class="card"><div class="table-wrap"></div></div>');
    const wrap = el.querySelector('.table-wrap');
    const thead = `<thead><tr>${cols.map(col=>`<th>${escapeHtml(col.header||col.field||'')}</th>`).join('')}</tr></thead>`;
    const tbody = `<tbody>${rows.map(r=>`<tr>${cols.map(col=>`<td>${escapeHtml(String(r[col.field]??''))}</td>`).join('')}</tr>`).join('')}</tbody>`;
    wrap.innerHTML = `<table>${thead}${tbody}</table>`;
    return el;
}

function renderFeed(){ const wrap=h('<div></div>'); (state.posts||[]).sort((a,b)=>b.ts-a.ts).forEach(p=> wrap.appendChild(renderPost(p)) ); return wrap; }
function renderPost(p){ const el=h(`<article class="card">
    <div class="head"><strong>@${p.user}</strong></div>
    ${p.img?`<img src="${p.img}" alt="post"/>`:''}
    <div class="actions">
        <button data-like>❤ ${p.liked?'เลิกถูกใจ':'ถูกใจ'}</button>
        <button data-cmt>💬 คอมเมนต์</button>
        <button data-share>↗️ แชร์</button>
    </div>
    <div class="meta">${p.likes||0} likes</div>
    <div class="meta">${escapeHtml(p.caption||'')}</div>
    <div class="meta">${(p.comments||[]).length} ความคิดเห็น</div>
`);
    el.querySelector('[data-like]').onclick=()=>{ p.liked=!p.liked; p.likes=(p.likes||0)+(p.liked?1:-1); save(); router(); };
    el.querySelector('[data-cmt]').onclick=()=>{ const text=prompt('คอมเมนต์'); if(text){ p.comments=p.comments||[]; p.comments.push({user:state.currentUser.username,text}); save(); router(); } };
    return el;
}

function renderComposer(){ const el=h(`<div class="card">
    <h3>สร้างโพสต์ใหม่</h3>
    <input type="file" accept="image/*" id="file"/>
    <textarea id="cap" placeholder="คำบรรยาย" style="width:100%;margin-top:8px"></textarea>
    <div style="margin-top:8px"><button id="btn">โพสต์</button></div>
</div>`);
    el.querySelector('#btn').onclick=()=>{
        const f=el.querySelector('#file').files[0]; const cap=el.querySelector('#cap').value;
        if(!f){ alert('เลือกรูปก่อน'); return; }
        const r=new FileReader(); r.onload=()=>{ state.posts=state.posts||[]; state.posts.push({id:Date.now(), user: state.currentUser.username, img:r.result, caption:cap, likes:0, liked:false, comments:[], ts:Date.now()}); save(); navigate('#/feed'); };
        r.readAsDataURL(f);
    };
    return el;
}

function renderForm(cfg){
    const el=h('<div class="card"></div>');
    const form=h('<form></form>');
    (cfg.fields||[]).forEach(f=>{
        const row=h('<div style="margin:6px 0"></div>');
        const label=h(`<div style="margin-bottom:4px">${escapeHtml(f.label||f.name)}</div>`);
        let input; const t=(f.type||'text').toLowerCase();
        if(t==='textarea'){ input=h('<textarea style="width:100%"></textarea>'); }
        else { input=h('<input style="width:100%"/>'); input.type=t; }
        input.name=f.name||f.id||'field';
        row.appendChild(label); row.appendChild(input);
        form.appendChild(row);
    });
    const btn=h('<button type="submit">ส่ง</button>'); form.appendChild(btn);
    form.onsubmit=(e)=>{
        e.preventDefault();
        // pass a config for handleAction('submit') with the form element for extraction
        handleAction('submit', { __formEl: form, collection: (cfg.collection || (cfg.submit&&cfg.submit.collection) || 'forms'), redirect: (cfg.redirect || (cfg.submit&&cfg.submit.to) || null) });
    };
    el.appendChild(form);
    return el;
}

function renderInbox(){ const list=h('<div class="card"></div>'); (state.messages||[]).forEach(m=> list.appendChild(h(`<div>${m.with}: ${m.last}</div>`)) ); return list; }
function renderNotifications(){ const list=h('<div class="card"></div>'); (state.notifications||[]).forEach(n=> list.appendChild(h(`<div>${n.text}</div>`)) ); return list; }
function renderProfile(){ const el=h('<div></div>'); const head=h(`<div class="card"><h3>@${state.currentUser.username}</h3><p>${state.currentUser.name||''}</p></div>`); el.appendChild(head); const grid=h('<div class="grid"></div>'); (state.posts||[]).filter(p=>p.user===state.currentUser.username).forEach(p=>{ const im=new Image(); im.src=p.img; grid.appendChild(im); }); el.appendChild(grid); return el; }

function renderTodo(){ const root=h('<div class="card"></div>'); root.innerHTML='<h3>Todo</h3><input id=t placeholder="เพิ่มงาน"><button id=b>เพิ่ม</button><ul id=list></ul>'; let todos=JSON.parse(localStorage.getItem('todos')||'[]'); function paint(){ list.innerHTML=''; todos.forEach((t,i)=>{ const li=h(`<li>${t}</li>`); li.onclick=()=>{ todos.splice(i,1); saveTodos(); }; list.appendChild(li); }); } function saveTodos(){ localStorage.setItem('todos', JSON.stringify(todos)); paint(); } root.querySelector('#b').onclick=()=>{ const v=root.querySelector('#t').value.trim(); if(v){ todos.push(v); saveTodos(); root.querySelector('#t').value=''; } }; const list=root.querySelector('#list'); paint(); return root; }
