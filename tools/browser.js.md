# Browser-Snippets (javascript_tool)

Statt `get_page_text` / `read_page` auf Formularseiten. Diese Snippets liefern nur Labels und Werte, ohne Länder- und Vorwahl-Listen.

## Formular scannen (Labels + Werte + kurze Optionen)
```js
[...document.querySelectorAll('input:not([type=hidden]),select,textarea')].filter(e=>e.offsetParent||e.type=='file').map(e=>{var l=(e.labels&&e.labels[0]?e.labels[0].innerText:e.getAttribute('aria-label')||e.name||e.id||'').trim().slice(0,45);var v=e.tagName=='SELECT'?e.options[e.selectedIndex]?.text+(e.options.length<12?' ['+[...e.options].map(o=>o.text).join('/')+']':' (+'+e.options.length+')'):(/checkbox|radio/.test(e.type)?e.checked:e.value.slice(0,40));return e.type+'|'+l+'='+v}).join('\n')
```
Beim Setzen per nativem Setter immer `e.maxLength` prüfen, weil maxlength sonst ignoriert wird (sonst kommt beim Absenden oft nur "Ein Fehler ist aufgetreten").
Wird die Ausgabe als "BLOCKED: Cookie/query string data" geblockt, steht meist die E-Mail in einem Wert. Dann `.filter(e=>e.type!='email')` ergänzen.

## Seitentext ohne Select-Optionen, ab Stichwort
```js
var c=document.body.cloneNode(true);c.querySelectorAll('select').forEach(s=>s.remove());var t=c.innerText.replace(/\s+/g,' ');var i=t.indexOf('STICHWORT');t.slice(i,i+1500)
```

## Stellenanzeige: nur Eckdaten (Ort, Dauer, Studiengang, Start)
```js
var t=document.body.innerText.replace(/\s+/g,' ');(t.match(/.{0,80}(Studiengang|studierst|Studium der|Monate|Dauer|Beginn|ab \d|Standort|Hybrid|Homeoffice|Stunden).{0,120}/gi)||[]).slice(0,10).join('\n')
```

## Datei-Input aus Shadow DOM holen (KPMG u. a.)
Danach mit `find "KPMG-Upload-N"` die Ref holen und `file_upload` aufrufen. Pro Datei wiederholen, weil die Komponente nach jedem Upload ein neues Input erzeugt.
```js
var f=[];(function w(r){r.querySelectorAll('*').forEach(e=>{if(e.shadowRoot)w(e.shadowRoot);if(e.tagName=='INPUT'&&e.type=='file'&&e.getRootNode()!==document)f.push(e)})})(document);f.map((x,i)=>{var h=x.getRootNode().host;x.setAttribute('aria-label','UP-'+h.id+'-'+Date.now()%1000);x.style.cssText='display:block;width:200px;height:30px';h.insertAdjacentElement('afterend',x);return x.getAttribute('aria-label')}).join(', ')
```

## StepStone-Trefferliste (Titel | Firma | Ort | volle URL)
StepStone-Detailseiten gehen nur mit voller Slug-URL, sonst kommt 403.
```js
[...document.querySelectorAll('article')].filter(a=>a.querySelector('a[href*="stellenangebote--"]')).map(a=>{var t=a.innerText.split('\n');return t[0].slice(0,60)+'|'+t[1].slice(0,22)+'|'+t[2].slice(0,22)+' '+a.querySelector('a[href*="stellenangebote--"]').href.split('?')[0]}).filter(s=>/prakti|intern|werkstud/i.test(s)).slice(0,15).join('\n')
```

## Medien stumm
```js
document.querySelectorAll('video,audio').forEach(m=>m.muted=true)
```
