/* 教學駕駛艙共用程式
 * 單元頁只要定義 window.UNIT（內容）後載入本檔，就會自動長出整個頁面。
 * 全站設定在 window.COCKPIT（見 assets/config.js）。
 */
(function () {
  'use strict';

  var CFG = Object.assign({ teacherPassword: '0000', seatMin: 1, seatMax: 30 }, window.COCKPIT || {});

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === 'class') node.className = attrs[k];
      else if (k === 'html') node.innerHTML = attrs[k];
      else if (k === 'text') node.textContent = attrs[k];
      else if (k.indexOf('on') === 0) node.addEventListener(k.slice(2), attrs[k]);
      else node.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) { if (c) node.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return node;
  }

  /* ── 全螢幕圖片與 QR ── */
  var overlay = el('div', { class: 'overlay', onclick: function () { overlay.classList.remove('show'); overlay.innerHTML = ''; } });
  function showFull(src) {
    overlay.innerHTML = '';
    overlay.appendChild(el('img', { src: src, alt: '' }));
    overlay.classList.add('show');
  }
  function qrSvg(url) {
    if (typeof window.qrcode !== 'function') return '<p>QR 產生器未載入</p>';
    var qr = window.qrcode(0, 'M');
    qr.addData(url);
    qr.make();
    return qr.createSvgTag({ cellSize: 8, margin: 2, scalable: true });
  }
  function showQR(url, title) {
    overlay.innerHTML = '';
    var box = el('div', { class: 'qr-box' });
    box.innerHTML = '<h2>' + (title || '掃描進入') + '</h2>' + qrSvg(url) + '<div class="url">' + url + '</div>';
    overlay.appendChild(box);
    overlay.classList.add('show');
  }

  /* ── 翻頁器 ── */
  function carousel(slides, emptyHint) {
    if (!slides || !slides.length) return el('div', { class: 'carousel' }, [el('div', { class: 'placeholder', text: emptyHint || '尚未放入簡報圖片' })]);
    var idx = 0;
    var inner = el('div', { class: 'carousel-inner' });
    var imgs = slides.map(function (src, i) {
      var img = el('img', { src: src, alt: '簡報第 ' + (i + 1) + ' 頁', loading: 'lazy', class: i === 0 ? 'active' : '', onclick: function () { showFull(src); } });
      inner.appendChild(img);
      return img;
    });
    var count = el('div', { class: 'carousel-count' });
    function go(n) {
      idx = (n + imgs.length) % imgs.length;
      imgs.forEach(function (img, i) { img.classList.toggle('active', i === idx); });
      count.textContent = (idx + 1) + ' / ' + imgs.length;
    }
    go(0);
    return el('div', { class: 'carousel' }, [
      inner,
      el('button', { class: 'carousel-btn prev', 'aria-label': '上一頁', text: '‹', onclick: function () { go(idx - 1); } }),
      el('button', { class: 'carousel-btn next', 'aria-label': '下一頁', text: '›', onclick: function () { go(idx + 1); } }),
      count
    ]);
  }

  /* ── 形成性評量（4 選 1，作答結果不回傳、不儲存） ── */
  var LETTERS = ['A', 'B', 'C', 'D'];
  function quiz(item) {
    var box = el('div', { class: 'quiz' });
    box.appendChild(el('div', { class: 'q', text: item.q }));
    var opts = el('div', { class: 'opts' });
    var fb = el('div', { class: 'feedback' });
    item.options.forEach(function (text, i) {
      opts.appendChild(el('button', {
        class: 'opt', text: LETTERS[i] + '. ' + text,
        onclick: function () {
          var ok = i === item.answer;
          opts.querySelectorAll('.opt').forEach(function (b, j) {
            b.classList.remove('correct', 'wrong');
            if (j === item.answer) b.classList.add('correct');
          });
          if (!ok) this.classList.add('wrong');
          fb.textContent = (ok ? '答對了！' : '再想想，正確答案是 ' + LETTERS[item.answer] + '。') + (item.feedback ? ' ' + item.feedback : '');
          box.classList.add('answered');
        }
      }));
    });
    box.appendChild(opts);
    box.appendChild(fb);
    return box;
  }

  /* ── 互動區 ── */
  var INTERACTIVES = {
    // 範例：拖曳點，顯示座標。各科可仿照這個格式新增自己的互動。
    'drag-demo': function (canvas, out) {
      var ctx = canvas.getContext('2d');
      var p = { x: canvas.width / 2, y: canvas.height / 2 }, dragging = false;
      function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = 'rgba(232,228,216,.15)';
        for (var x = 0; x <= canvas.width; x += 40) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke(); }
        for (var y = 0; y <= canvas.height; y += 40) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke(); }
        ctx.fillStyle = '#ffd54f';
        ctx.beginPath(); ctx.arc(p.x, p.y, 14, 0, Math.PI * 2); ctx.fill();
        out.textContent = '拖曳黃點：(' + Math.round(p.x / 40) + ', ' + Math.round((canvas.height - p.y) / 40) + ')';
      }
      function pos(e) {
        var r = canvas.getBoundingClientRect();
        return { x: (e.clientX - r.left) * canvas.width / r.width, y: (e.clientY - r.top) * canvas.height / r.height };
      }
      canvas.addEventListener('pointerdown', function (e) { var q = pos(e); if (Math.hypot(q.x - p.x, q.y - p.y) < 30) { dragging = true; canvas.setPointerCapture(e.pointerId); } });
      canvas.addEventListener('pointermove', function (e) { if (dragging) { p = pos(e); draw(); } });
      canvas.addEventListener('pointerup', function () { dragging = false; });
      draw();
    }
  };

  function interactive(spec) {
    var canvas = el('canvas', { width: 640, height: 360 });
    var out = el('div', { class: 'result-display' });
    var fn = typeof spec === 'function' ? spec : INTERACTIVES[spec];
    if (!fn) return el('div', { class: 'placeholder', text: '找不到互動：' + spec });
    setTimeout(function () { fn(canvas, out); }, 0);
    return el('div', { class: 'interactive' }, [canvas, out]);
  }

  function teacherBox(label, content) {
    var box = el('div', { class: 'teacher-only teacher-box' }, [el('div', { class: 'label', text: label })]);
    if (Array.isArray(content)) {
      var ul = el('ul', { style: 'padding-left:1.2em' });
      content.forEach(function (t) { ul.appendChild(el('li', { text: t })); });
      box.appendChild(ul);
    } else box.appendChild(el('div', { html: content }));
    return box;
  }

  /* ── 單元頁 ── */
  function renderUnit(U) {
    document.title = U.title + '｜教學駕駛艙';
    var main = el('main', { class: 'cp-main' });

    var head = el('section', { class: 'cp-section', id: 'top' }, [el('h2', { text: '學習目標' })]);
    function secTitle(t, i) {
      return /^(案件|\d+[\.、\s]|第)/.test(t) ? t : (i + 1) + '. ' + t;
    }

    var chips = el('div', { class: 'chips' });
    (U.objectives || []).forEach(function (o) { chips.appendChild(el('span', { class: 'chip', text: o })); });
    head.appendChild(chips);
    var pills = el('nav', { class: 'pills', 'aria-label': '主題導覽' });
    (U.sections || []).forEach(function (s, i) { pills.appendChild(el('a', { class: 'pill', href: '#sec' + (i + 1), text: secTitle(s.title, i) })); });
    pills.appendChild(el('a', { class: 'pill', href: '#summary', text: '總結' }));
    head.appendChild(pills);
    main.appendChild(head);

    if (U.intro) {
      main.appendChild(el('section', { class: 'cp-section', id: 'intro' }, [el('h2', { text: U.intro.title || '開場' }), carousel(U.intro.slides, '把開場簡報圖片放進 assets/，再填到 intro.slides')]));
    }

    (U.sections || []).forEach(function (s, i) {
      var sec = el('section', { class: 'cp-section', id: 'sec' + (i + 1) });
      sec.appendChild(el('h2', { html: (s.standard ? '<span class="tag">' + s.standard + '</span>' : '') + secTitle(s.title, i) }));
      if (s.text) sec.appendChild(el('p', { html: s.text }));
      sec.appendChild(el('h3', { text: '簡報' }));
      sec.appendChild(carousel(s.slides, '把這個重點的簡報圖片填到 slides'));
      if (s.interactive) { sec.appendChild(el('h3', { text: '動手操作' })); sec.appendChild(interactive(s.interactive)); }
      if (s.quizzes && s.quizzes.length) { sec.appendChild(el('h3', { text: '想一想' })); s.quizzes.forEach(function (q) { sec.appendChild(quiz(q)); }); }
      sec.appendChild(el('h3', { text: '資訊圖表' }));
      sec.appendChild(s.infographic
        ? el('img', { src: s.infographic, alt: s.title + '資訊圖表', loading: 'lazy', style: 'cursor:zoom-in;border-radius:8px', onclick: function () { showFull(s.infographic); } })
        : el('div', { class: 'placeholder', text: '把資訊圖表 JPG 填到 infographic' }));
      if (s.teacherTips) sec.appendChild(teacherBox('教學提示', s.teacherTips));
      main.appendChild(sec);
    });

    var sum = el('section', { class: 'cp-section', id: 'summary' }, [el('h2', { text: '總結' })]);
    var ul = el('ul', { style: 'padding-left:1.2em' });
    (U.summary || ['（填入本單元重點整理）']).forEach(function (t) { ul.appendChild(el('li', { html: t })); });
    sum.appendChild(ul);
    main.appendChild(sum);

    var v = U.video || {};
    var vsec = el('section', { class: 'cp-section', id: 'video' }, [el('h2', { text: '影片' })]);
    if (v.youtube) vsec.appendChild(el('div', { class: 'video-wrap' }, [el('iframe', { src: 'https://www.youtube-nocookie.com/embed/' + v.youtube, title: '教學影片', loading: 'lazy', allowfullscreen: '' })]));
    else vsec.appendChild(el('div', { class: 'placeholder', text: '影片請上傳 YouTube（不公開），再把影片 ID 填到 video.youtube' }));
    main.appendChild(vsec);

    var t = U.teacher || {};
    if (t.mistakes || t.links) {
      var tsec = el('section', { class: 'cp-section teacher-only', id: 'teacher' }, [el('h2', { text: '教師專區' })]);
      if (t.mistakes) tsec.appendChild(teacherBox('常見錯誤', t.mistakes));
      if (t.links) tsec.appendChild(teacherBox('相關連結', t.links.map(function (l) { return '<a href="' + l.url + '" target="_blank" rel="noopener">' + l.label + '</a>'; }).join('<br>')));
      main.appendChild(tsec);
    }

    document.body.appendChild(header(U.title, [U.grade, U.subject].filter(Boolean).join('・'), true));
    document.body.appendChild(main);
    mountTools();
  }

  function header(title, sub, withHome) {
    var h = el('header', { class: 'cp-header' });
    var left = el('div', {}, [el('h1', { text: title }), sub ? el('div', { class: 'sub', text: sub }) : null]);
    var right = el('div', { style: 'display:flex;gap:8px;align-items:center' }, [
      withHome ? el('a', { class: 'home-link', href: '../../index.html', text: '回首頁' }) : null,
      withHome ? el('button', { class: 'mode-btn', id: 'modeBtn', text: '學生模式', onclick: toggleMode }) : null
    ]);
    h.appendChild(left);
    h.appendChild(right);
    return h;
  }

  /* ── 教師／學生模式：只用來隱藏教學提示，不是安全機制 ── */
  function toggleMode() {
    var btn = document.getElementById('modeBtn');
    if (document.body.classList.contains('teacher')) {
      document.body.classList.remove('teacher');
      btn.textContent = '學生模式';
      return;
    }
    var pw = window.prompt('請輸入教師密碼');
    if (pw === null) return;
    if (pw === String(CFG.teacherPassword)) {
      document.body.classList.add('teacher');
      btn.textContent = '教師模式';
    } else window.alert('密碼不正確');
  }

  /* ── 浮動工具：抽籤器、計時器、QR ── */
  function mountTools() {
    var panel = el('div', { class: 'tool-panel', id: 'toolPanel' });
    panel.innerHTML =
      '<h4>抽籤器</h4>' +
      '<div class="row">座號 <input type="number" id="seatMin" value="' + CFG.seatMin + '" min="1"> 到 <input type="number" id="seatMax" value="' + CFG.seatMax + '" min="1"></div>' +
      '<div class="row"><label><input type="checkbox" id="noRepeat" checked> 不重複</label></div>' +
      '<div class="big-num" id="seatOut">—</div>' +
      '<div class="row"><button id="drawBtn">抽一位</button><button id="resetDraw">重置</button></div>' +
      '<div class="teacher-note" id="drawnList"></div>' +
      '<hr><h4>計時器</h4>' +
      '<div class="row"><button data-sec="60">1 分</button><button data-sec="180">3 分</button><button data-sec="300">5 分</button><input type="number" id="timerMin" value="10" min="1" style="width:56px"> 分<button id="timerCustom">開始</button></div>' +
      '<div class="big-num" id="timerOut">00:00</div>' +
      '<div class="row"><button id="timerPause">暫停／繼續</button><button id="timerStop">歸零</button></div>' +
      '<hr><button id="qrBtn" style="width:100%">顯示本頁 QR code</button>';
    var toggle = el('button', { class: 'tool-toggle', text: '工具', onclick: function () { panel.classList.toggle('show'); } });
    document.body.appendChild(el('div', { class: 'tools' }, [panel, toggle]));
    document.body.appendChild(overlay);

    var drawn = [];
    function drawSeat() {
      var lo = parseInt(document.getElementById('seatMin').value, 10), hi = parseInt(document.getElementById('seatMax').value, 10);
      if (!(hi >= lo)) return;
      var pool = [];
      for (var n = lo; n <= hi; n++) if (!document.getElementById('noRepeat').checked || drawn.indexOf(n) < 0) pool.push(n);
      var out = document.getElementById('seatOut');
      if (!pool.length) { out.textContent = '抽完了'; return; }
      var pick = pool[Math.floor(Math.random() * pool.length)], spins = 0;
      var t = setInterval(function () {
        out.textContent = pool[Math.floor(Math.random() * pool.length)];
        if (++spins > 12) { clearInterval(t); out.textContent = pick; drawn.push(pick); document.getElementById('drawnList').textContent = '已抽：' + drawn.join('、'); }
      }, 60);
    }
    document.getElementById('drawBtn').onclick = drawSeat;
    document.getElementById('resetDraw').onclick = function () { drawn = []; document.getElementById('seatOut').textContent = '—'; document.getElementById('drawnList').textContent = ''; };

    var remain = 0, timer = null, running = false;
    var tOut = document.getElementById('timerOut');
    function show() { tOut.textContent = String(Math.floor(remain / 60)).padStart(2, '0') + ':' + String(remain % 60).padStart(2, '0'); }
    function tick() {
      remain = Math.max(0, remain - 1); show();
      if (remain === 0) { clearInterval(timer); timer = null; running = false; tOut.classList.add('done'); beep(); }
    }
    function start(sec) { clearInterval(timer); remain = sec; running = true; tOut.classList.remove('done'); show(); timer = setInterval(tick, 1000); }
    panel.querySelectorAll('[data-sec]').forEach(function (b) { b.onclick = function () { start(parseInt(b.dataset.sec, 10)); }; });
    document.getElementById('timerCustom').onclick = function () { var m = parseInt(document.getElementById('timerMin').value, 10); if (m > 0) start(m * 60); };
    document.getElementById('timerPause').onclick = function () {
      if (running) { clearInterval(timer); timer = null; running = false; }
      else if (remain > 0) { running = true; timer = setInterval(tick, 1000); }
    };
    document.getElementById('timerStop').onclick = function () { clearInterval(timer); timer = null; running = false; remain = 0; tOut.classList.remove('done'); show(); };
    document.getElementById('qrBtn').onclick = function () { showQR(location.href.split('#')[0], document.title); };

    mountPen();
  }

  function beep() {
    try {
      var ac = new (window.AudioContext || window.webkitAudioContext)();
      [0, 0.35, 0.7].forEach(function (d) {
        var o = ac.createOscillator(), g = ac.createGain();
        o.frequency.value = 880; o.connect(g); g.connect(ac.destination);
        g.gain.setValueAtTime(0.25, ac.currentTime + d); g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + d + 0.3);
        o.start(ac.currentTime + d); o.stop(ac.currentTime + d + 0.3);
      });
    } catch (e) { /* 不支援音效就略過 */ }
  }

  /* ── 畫筆（5 色） ── */
  function mountPen() {
    var COLORS = ['#24343a', '#e0a100', '#e2574c', '#2f80c9', '#2f9a5c'];
    var canvas = el('canvas', { id: 'penCanvas' });
    document.body.appendChild(canvas);
    var ctx = canvas.getContext('2d'), color = COLORS[0], drawing = false, last = null;
    function resize() {
      var img = canvas.width ? ctx.getImageData(0, 0, canvas.width, canvas.height) : null;
      canvas.width = window.innerWidth; canvas.height = window.innerHeight;
      if (img) ctx.putImageData(img, 0, 0);
    }
    resize();
    window.addEventListener('resize', resize);
    canvas.addEventListener('pointerdown', function (e) { drawing = true; last = { x: e.clientX, y: e.clientY }; canvas.setPointerCapture(e.pointerId); });
    canvas.addEventListener('pointermove', function (e) {
      if (!drawing) return;
      ctx.strokeStyle = color; ctx.lineWidth = 4; ctx.lineCap = 'round'; ctx.globalAlpha = 0.9;
      ctx.beginPath(); ctx.moveTo(last.x, last.y); ctx.lineTo(e.clientX, e.clientY); ctx.stroke();
      last = { x: e.clientX, y: e.clientY };
    });
    canvas.addEventListener('pointerup', function () { drawing = false; });

    var swatches = el('div', { class: 'swatches' });
    COLORS.forEach(function (c, i) {
      swatches.appendChild(el('button', { class: 'swatch' + (i === 0 ? ' active' : ''), style: 'background:' + c, 'aria-label': '粉筆顏色 ' + (i + 1), onclick: function () {
        color = c; swatches.querySelectorAll('.swatch').forEach(function (b) { b.classList.remove('active'); }); this.classList.add('active');
      } }));
    });
    swatches.appendChild(el('button', { class: 'pen-clear', text: '清除', onclick: function () { ctx.clearRect(0, 0, canvas.width, canvas.height); } }));
    document.body.appendChild(el('div', { class: 'pen-bar' }, [swatches, el('button', { class: 'pen-main', text: '畫筆', onclick: function () { document.body.classList.toggle('pen-on'); } })]));
  }

  /* ── 首頁 ── */
  function renderHome(H) {
    document.body.appendChild(header(H.title, H.subtitle, false));
    var main = el('main', { class: 'cp-main' });
    var grid = el('div', { class: 'unit-grid' });
    (H.units || []).forEach(function (u) {
      var card = el('a', { class: 'unit-card', href: u.href }, [
        el('h3', { text: u.title }),
        el('p', { text: u.summary || '' })
      ]);
      (u.badges || []).forEach(function (b) { card.appendChild(el('span', { class: 'badge', text: b })); });
      card.appendChild(el('button', { class: 'qr-btn', text: 'QR', 'aria-label': u.title + ' 的 QR code', onclick: function (e) {
        e.preventDefault(); e.stopPropagation();
        showQR(new URL(u.href, location.href).href, u.title);
      } }));
      grid.appendChild(card);
    });
    main.appendChild(el('section', { class: 'cp-section' }, [el('h2', { text: '單元' }), grid]));

    var siteUrl = location.href.split('#')[0];
    var qrWrap = el('div', { class: 'qr', html: qrSvg(siteUrl) });
    main.appendChild(el('section', { class: 'cp-section', id: 'qr' }, [
      el('h2', { text: '學生掃描進入' }),
      el('div', { class: 'site-qr' }, [qrWrap, el('div', {}, [
        el('p', { text: '用平板相機掃描左邊的 QR code，就能打開這個首頁。' }),
        el('p', { text: '每張單元卡右上角的「QR」可以放大顯示該單元的 QR code，方便投影。' }),
        el('button', { class: 'pill', text: '放大投影', onclick: function () { showQR(siteUrl, H.title); } })
      ])])
    ]));
    document.body.appendChild(main);
    mountTools();
  }

  window.Cockpit = { renderUnit: renderUnit, renderHome: renderHome, interactives: INTERACTIVES };
})();
