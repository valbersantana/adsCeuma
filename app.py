import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="Power BI TV · CEUMA",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Remove todo o chrome do Streamlit
st.markdown("""
<style>
    #MainMenu, header, footer, .stDeployButton { display: none !important; }
    .stAppViewContainer { padding: 0 !important; }
    .stMain > div { padding: 0 !important; }
    section[data-testid="stSidebar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================
#  CONFIGURAÇÃO — edite aqui
# ============================================================
DASHBOARDS = [
    {
        "name": "Home",
        "url": "https://app.powerbi.com/view?r=eyJrIjoiNzMwYWE3Y2EtN2ViMi00MDAyLWE3OTYtYjI4MWRlZmRhZTZmIiwidCI6ImM5M2MyMTE2LWNmMWItNDQ1Ni1hYTMyLTcwMjQ2OGVhZWJlNyJ9&pageName=252089709eb159a1c20d&pageName=252089709eb159a1c20d"
    },
    {
        "name": "Engajamento",
        "url": "https://app.powerbi.com/view?r=eyJrIjoiNzMwYWE3Y2EtN2ViMi00MDAyLWE3OTYtYjI4MWRlZmRhZTZmIiwidCI6ImM5M2MyMTE2LWNmMWItNDQ1Ni1hYTMyLTcwMjQ2OGVhZWJlNyJ9&pageName=252089709eb159a1c20d&pageName=eceb1f8645ab9010a04b"
    },
    {
        "name": "Progresso",
        "url": "https://app.powerbi.com/view?r=eyJrIjoiNzMwYWE3Y2EtN2ViMi00MDAyLWE3OTYtYjI4MWRlZmRhZTZmIiwidCI6ImM5M2MyMTE2LWNmMWItNDQ1Ni1hYTMyLTcwMjQ2OGVhZWJlNyJ9&pageName=252089709eb159a1c20d&pageName=519adeb3067da44a5992"
    },
    {
        "name": "Trilhas",
        "url": "https://app.powerbi.com/view?r=eyJrIjoiNzMwYWE3Y2EtN2ViMi00MDAyLWE3OTYtYjI4MWRlZmRhZTZmIiwidCI6ImM5M2MyMTE2LWNmMWItNDQ1Ni1hYTMyLTcwMjQ2OGVhZWJlNyJ9&pageName=252089709eb159a1c20d&pageName=bbeccbd4827e1b55c213"
    },
    {
        "name": "Ranking",
        "url": "https://app.powerbi.com/view?r=eyJrIjoiNzMwYWE3Y2EtN2ViMi00MDAyLWE3OTYtYjI4MWRlZmRhZTZmIiwidCI6ImM5M2MyMTE2LWNmMWItNDQ1Ni1hYTMyLTcwMjQ2OGVhZWJlNyJ9&pageName=252089709eb159a1c20d&pageName=bdf7712ed070aa51561a"
    },
]

DEFAULT_INTERVAL = 90   # segundos entre slides
# ============================================================

dashboards_json = json.dumps(DASHBOARDS)

HTML = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    background: #000;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    font-family: 'DM Sans', sans-serif;
  }}

  /* ── Iframes ── */
  .frame {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    border: none;
    opacity: 0;
    transition: opacity 0.8s ease;
    pointer-events: none;
    z-index: 1;
  }}
  .frame.active {{
    opacity: 1;
    pointer-events: all;
    z-index: 2;
  }}

  /* ── Barra de controles ── */
  #bar {{
    position: fixed;
    bottom: 18px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 9999;
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(10, 10, 20, 0.88);
    backdrop-filter: blur(12px);
    padding: 10px 18px;
    border-radius: 50px;
    border: 1px solid rgba(255,255,255,0.08);
    opacity: 1;
    transition: opacity 0.4s ease;
  }}
  #bar.hidden {{ opacity: 0; pointer-events: none; }}

  .btn {{
    width: 34px; height: 34px;
    border-radius: 50%;
    border: none;
    background: rgba(255,255,255,0.1);
    color: #fff;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px;
    transition: background 0.2s, transform 0.1s;
    flex-shrink: 0;
  }}
  .btn:hover  {{ background: rgba(255,255,255,0.22); }}
  .btn:active {{ transform: scale(0.92); }}
  .btn.play   {{ width: 38px; height: 38px; background: rgba(201,168,76,0.25); color: #c9a84c; }}
  .btn.play:hover {{ background: rgba(201,168,76,0.4); }}

  /* Dots de navegação */
  #dots {{
    display: flex; gap: 6px; align-items: center; padding: 0 4px;
  }}
  .dot {{
    width: 7px; height: 7px;
    border-radius: 50%;
    background: rgba(255,255,255,0.25);
    cursor: pointer;
    transition: background 0.2s, transform 0.2s;
    border: none; padding: 0;
  }}
  .dot.active {{ background: #c9a84c; transform: scale(1.3); }}
  .dot:hover  {{ background: rgba(255,255,255,0.5); }}

  /* Select de intervalo */
  #intervalSelect {{
    background: rgba(255,255,255,0.08);
    color: rgba(255,255,255,0.7);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 5px 10px;
    font-family: 'Syne', sans-serif;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .06em;
    cursor: pointer;
    outline: none;
  }}
  #intervalSelect option {{ background: #111; color: #fff; }}

  /* Nome do slide */
  #slideName {{
    font-family: 'Syne', sans-serif;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.45);
    min-width: 70px;
    text-align: center;
  }}

  /* Ring de progresso */
  #ring {{
    position: relative;
    width: 34px; height: 34px;
    flex-shrink: 0;
  }}
  #ring svg {{
    width: 100%; height: 100%;
    transform: rotate(-90deg);
  }}
  #ring .track {{ fill: none; stroke: rgba(255,255,255,0.1); stroke-width: 2.5; }}
  #ring .fill  {{ fill: none; stroke: #c9a84c; stroke-width: 2.5; stroke-linecap: round; transition: stroke-dashoffset 0.25s linear; }}
  #ring .num {{
    position: absolute; inset: 0;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Syne', sans-serif;
    font-size: 9px; font-weight: 700;
    color: rgba(255,255,255,0.55);
  }}

  /* Divisor */
  .sep {{ width: 1px; height: 20px; background: rgba(255,255,255,0.1); }}
</style>
</head>
<body>

<!-- Dois iframes em alternância — o ativo mostra, o outro pré-carrega -->
<iframe id="frame-a" class="frame active" allowfullscreen></iframe>
<iframe id="frame-b" class="frame"        allowfullscreen></iframe>

<!-- Barra de controles -->
<div id="bar">

  <button class="btn" id="btnPrev" title="Anterior">&#9664;</button>

  <button class="btn play" id="btnPlay" title="Pausar">&#10074;&#10074;</button>

  <button class="btn" id="btnNext" title="Próximo">&#9654;</button>

  <div class="sep"></div>

  <div id="dots"></div>

  <div class="sep"></div>

  <span id="slideName"></span>

  <div class="sep"></div>

  <select id="intervalSelect">
    <option value="10">10s</option>
    <option value="15">15s</option>
    <option value="20">20s</option>
    <option value="90" selected>90s</option>
    <option value="45">45s</option>
    <option value="60">60s</option>
    <option value="120">2min</option>
  </select>

  <!-- Ring de contagem regressiva -->
  <div id="ring">
    <svg viewBox="0 0 34 34">
      <circle class="track" cx="17" cy="17" r="14"/>
      <circle class="fill"  cx="17" cy="17" r="14" id="ringFill"/>
    </svg>
    <div class="num" id="ringNum"></div>
  </div>

</div>

<script>
  const DASHBOARDS  = {dashboards_json};
  const CIRCUMF     = 2 * Math.PI * 14; // raio 14

  let current   = 0;
  let isPlaying = true;
  let interval  = {DEFAULT_INTERVAL};
  let elapsed   = 0;
  let ticker    = null;
  let hideTimer = null;

  const frameA     = document.getElementById('frame-a');
  const frameB     = document.getElementById('frame-b');
  const btnPlay    = document.getElementById('btnPlay');
  const btnPrev    = document.getElementById('btnPrev');
  const btnNext    = document.getElementById('btnNext');
  const dotsEl     = document.getElementById('dots');
  const nameEl     = document.getElementById('slideName');
  const bar        = document.getElementById('bar');
  const intSelect  = document.getElementById('intervalSelect');
  const ringFill   = document.getElementById('ringFill');
  const ringNum    = document.getElementById('ringNum');

  // ── Setup inicial do ring ──
  ringFill.style.strokeDasharray  = CIRCUMF;
  ringFill.style.strokeDashoffset = CIRCUMF;

  // ── Criar dots ──
  DASHBOARDS.forEach((d, i) => {{
    const btn = document.createElement('button');
    btn.className = 'dot' + (i === 0 ? ' active' : '');
    btn.title = d.name;
    btn.addEventListener('click', () => goTo(i));
    dotsEl.appendChild(btn);
  }});

  // ── Lógica de slides ──
  // Qual iframe está ativo agora
  let activeFrame = frameA;
  let nextFrame   = frameB;

  function goTo(index, resetElapsed = true) {{
    if (index === current && resetElapsed) {{
      // só reseta o timer
      if (resetElapsed) {{ elapsed = 0; updateRing(); }}
      return;
    }}

    const prev = current;
    current = ((index % DASHBOARDS.length) + DASHBOARDS.length) % DASHBOARDS.length;

    // Pré-carrega no frame inativo, depois troca
    nextFrame.src = DASHBOARDS[current].url;
    nextFrame.onload = () => {{
      activeFrame.classList.remove('active');
      nextFrame.classList.add('active');
      // alterna referências
      [activeFrame, nextFrame] = [nextFrame, activeFrame];
    }};

    // Atualiza dots e nome
    document.querySelectorAll('.dot').forEach((d, i) => {{
      d.classList.toggle('active', i === current);
    }});
    nameEl.textContent = DASHBOARDS[current].name;

    if (resetElapsed) elapsed = 0;
    updateRing();
  }}

  function updateRing() {{
    const remaining = interval - elapsed;
    const pct       = elapsed / interval;
    const offset    = CIRCUMF * (1 - pct);
    ringFill.style.strokeDashoffset = offset;
    ringNum.textContent = remaining + 's';
  }}

  function startTicker() {{
    if (ticker) clearInterval(ticker);
    ticker = setInterval(() => {{
      if (!isPlaying) return;
      elapsed++;
      updateRing();
      if (elapsed >= interval) {{
        elapsed = 0;
        goTo(current + 1, false);
      }}
    }}, 1000);
  }}

  function togglePlay() {{
    isPlaying = !isPlaying;
    btnPlay.innerHTML = isPlaying ? '&#10074;&#10074;' : '&#9654;';
    btnPlay.title = isPlaying ? 'Pausar' : 'Retomar';
    if (isPlaying) elapsed = 0;
    updateRing();
  }}

  // ── Auto-esconder barra ──
  function showBar() {{
    bar.classList.remove('hidden');
    if (hideTimer) clearTimeout(hideTimer);
    hideTimer = setTimeout(() => bar.classList.add('hidden'), 4000);
  }}

  document.addEventListener('mousemove', showBar);
  document.addEventListener('keydown',   showBar);

  // ── Eventos ──
  btnPlay.addEventListener('click', togglePlay);
  btnPrev.addEventListener('click', () => goTo(current - 1));
  btnNext.addEventListener('click', () => goTo(current + 1));

  intSelect.addEventListener('change', () => {{
    interval = parseInt(intSelect.value);
    elapsed  = 0;
    updateRing();
  }});

  // Teclado
  document.addEventListener('keydown', e => {{
    if (e.key === 'ArrowRight') goTo(current + 1);
    if (e.key === 'ArrowLeft')  goTo(current - 1);
    if (e.key === ' ')          togglePlay();
  }});

  // ── Inicializar ──
  activeFrame.src = DASHBOARDS[0].url;
  // Pré-carrega o segundo
  if (DASHBOARDS.length > 1) nextFrame.src = DASHBOARDS[1].url;

  nameEl.textContent = DASHBOARDS[0].name;
  updateRing();
  startTicker();
  showBar();
</script>
</body>
</html>
"""

components.html(HTML, height=800, scrolling=False)
