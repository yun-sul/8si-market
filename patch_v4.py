# -*- coding: utf-8 -*-
"""v4.0 리뉴얼: 마크업 교체 + 디자인 시스템 CSS 주입 (반복 실행 가능)."""
import io, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, "index.html")
CSS = os.path.join(BASE, "design-v4.css")

src = io.open(HTML, encoding="utf-8").read()
orig = src

# ── 1. 온보딩 역할 선택 스텝 교체 ─────────────────────────────────────────
start = src.index('          <div class="ob-step is-on" id="obStep-role">')
end = src.index('          <!-- step 2-A · 소비자 회원가입 -->')
old_role = src[start:end]

ROLE_NEW = '''          <div class="ob-step is-on" id="obStep-role">
            <div class="ob-top">
              <div class="ob-brand">
                <span class="mark">8</span>
                <span class="ob-bt"><b>8시마켓</b><small>8SI MARKET</small></span>
              </div>
              <button class="ob-topinstall" type="button" data-act="install" data-install aria-label="8시마켓 앱 설치"><i aria-hidden="true" data-install-ic>📲</i><span data-install-label data-compact="1">앱 설치</span></button>
            </div>
            <div class="ob-left">
              <div class="ob-hero">
                <h1 class="sr-only">저녁 8시, 퇴근길 동네 장바구니 — 오늘 남은 좋은 상품, 동네에서 득템</h1>
                <span class="ob-eyebrow">저녁 8시 · 동네 마감특가</span>
                <p class="ob-h1">오늘 남은 좋은 상품,<br><em>반값</em>에 가져가세요</p>
                <p class="ob-sub">퇴근길에 예약하고, 우리 동네 매장에서 픽업.<br>정육·수산·채소·반찬·빵을 마감특가로 만나요.</p>
                <div class="ob-stats">
                  <div><b id="obStatDeal">15<em>개</em></b><small>오늘 마감특가</small></div>
                  <div><b>25<em>곳</em></b><small>전국 거점</small></div>
                  <div><b>60<em>%</em></b><small>최대 할인</small></div>
                </div>
              </div>
            </div>
            <div class="ob-right">
              <p class="ob-q">어떤 방식으로 시작할까요?</p>
              <p class="ob-resume" id="obResume" hidden></p>
              <div class="roles" id="roles">
                <div class="role" role="button" tabindex="0" data-role="consumer" aria-pressed="false">
                  <span class="ri">🛒</span>
                  <span class="rt">
                    <span class="rlabel">Consumer</span>
                    <b>할인 장보기 · 간편 가입</b>
                    <small>내 동네 마감특가를 예약하고 퇴근길에 픽업해요</small>
                    <span class="rtags">
                      <button class="rtag" type="button" data-rolechip="consumer-nick" aria-label="10초 가입으로 바로 시작"><i aria-hidden="true">✓</i>10초 가입</button>
                      <button class="rtag" type="button" data-rolechip="consumer-dong" aria-label="내 동네를 고르고 가입"><i aria-hidden="true">✓</i>동네 선택</button>
                      <button class="rtag is-skip" type="button" data-rolechip="consumer-skip" aria-label="가입 없이 둘러보기">가입 없이 둘러보기 ›</button>
                    </span>
                  </span>
                  <span class="check" aria-hidden="true">✓</span>
                </div>
                <div class="role" role="button" tabindex="0" data-role="owner" aria-pressed="false">
                  <span class="ri">🏪</span>
                  <span class="rt">
                    <span class="rlabel">Store owner</span>
                    <b>우리 매장 입점 · 마감 등록</b>
                    <small>남은 재고를 AI 가격 결정으로 마감까지 소진해요</small>
                    <span class="rtags">
                      <button class="rtag" type="button" data-rolechip="owner-store" aria-label="상호·업종을 등록하고 입점"><i aria-hidden="true">✓</i>상호·업종 등록</button>
                      <button class="rtag" type="button" data-rolechip="owner-close" aria-label="마감시간을 설정하고 입점"><i aria-hidden="true">✓</i>마감시간 설정</button>
                      <button class="rtag" type="button" data-rolechip="owner-ai" aria-label="AI 10초 상품등록">AI 10초 상품등록 ›</button>
                    </span>
                  </span>
                  <span class="check" aria-hidden="true">✓</span>
                </div>
              </div>
              <button class="btn btn-primary btn-block ob-next" type="button" id="obNext" disabled>다음</button>
              <div class="ob-inapp" id="obInApp" hidden></div>
              <div class="ob-bottom">
                <button class="ob-login-m" type="button" data-act="login">로그인 / 회원가입</button>
                <button class="ob-skip" type="button" id="obSkip">가입 없이 둘러보기</button>
              </div>
              <p class="ob-foot">로그인 없이 체험하는 MVP입니다 · 실제 결제는 발생하지 않아요</p>
              <button class="ob-media" type="button" data-act="promo" aria-label="8시마켓 브랜드 소개와 홍보영상 보기">
                <img src="poster.jpg" alt="8시마켓 브랜드 포스터">
                <span class="om-tx"><b>8시마켓 브랜드 소개</b><small>포스터 · 1분 22초 홍보영상으로 먼저 보기</small></span>
                <span class="om-play" aria-hidden="true">▶</span>
              </button>
            </div>
          </div>

'''
src = src[:start] + ROLE_NEW + src[end:]

# ── 2. 홈 상단: 동네 칩 + 검색 바 ─────────────────────────────────────────
m = re.search(r'              <div class="loc-row">.*?\n              </div>\n', src, re.S)
assert m, "loc-row not found"
LOC_NEW = '''              <div class="loc-row">
                <button class="loc-chip loc-banner" type="button" data-act="radius" aria-label="내 동네 선택 — 현재 대전 둔산동 반경 2km">
                  <span class="lc-pin" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11Z"/><circle cx="12" cy="10" r="2.4"/></svg></span>
                  <span class="lc-tx">
                    <b id="locDong">대전 둔산동</b>
                    <small><span class="rad">반경 <span id="radiusLabel">2km</span></span> 이 동네 기준 픽업</small>
                  </span>
                  <span class="lc-cta">변경<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg></span>
                </button>
                <button class="map-toggle" type="button" data-act="go-map" aria-label="지도로 보기">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11Z"/><circle cx="12" cy="10" r="2.4"/></svg>
                  <span>지도</span>
                </button>
              </div>
              <div class="search-row">
                <div class="searchbar">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/></svg>
                  <input id="qInput" type="search" placeholder="상품·매장 이름으로 찾기" autocomplete="off" aria-label="상품·매장 검색">
                  <button class="q-clear" type="button" id="qClear" aria-label="검색어 지우기" hidden>✕</button>
                </div>
              </div>
'''
src = src[:m.start()] + LOC_NEW + src[m.end():]
# 중복 검색 바 정리(재실행 안전)
src = re.sub(r'(              <div class="search-row">.*?\n              </div>\n)(              <div class="search-row">.*?\n              </div>\n)', r'\1', src, count=1, flags=re.S)

# ── 3. 상품 카드 — 2열 상용 커머스 카드 ───────────────────────────────────
s = src.index('function cardHTML(p){')
e = src.index('function renderFeed(){')
CARD_NEW = '''function cardHTML(p){
  var st = storeById(p.store), d = disc(p), sold = p.left <= 0, fav = state.fav.indexOf(p.id) > -1;
  var demo = demoStore(st);
  var ratio = (p.total ? Math.max(6, Math.round(p.left / p.total * 100)) : 40);
  var low = p.left > 0 && p.left <= 2;
  return '<article class="pcard'+(p.isNew?' is-new':'')+(sold?' is-sold':'')+(low?' urgent':'')+'" data-card="'+p.id+'">'+
    '<div class="thumb '+catClass(p.cat)+'">'+
      '<span class="badge">'+d+'%<small> 할인</small></span>'+
      '<button class="fav'+(fav?' is-on':'')+'" type="button" data-act="fav" data-id="'+p.id+'" aria-pressed="'+fav+'" aria-label="찜하기">'+heartSVG()+'</button>'+
      '<span class="emoji">'+p.emoji+'</span>'+
      (demo ? '<span class="demo-chip">예시</span>' : '')+
      (low ? '<span class="urgent-chip">품절임박</span>' : '')+
      (sold ? '<span class="sold-stamp" aria-label="품절"></span>' : '')+
      '<span class="stockbar" aria-hidden="true"><i class="'+(low?'low':(ratio<45?'mid':''))+'" style="width:'+(sold?0:ratio)+'%"></i></span>'+
    '</div>'+
    '<div class="cbody">'+
      '<span class="sname">'+esc(st.name)+(demo?'<span class="mini">예시</span>':'')+'</span>'+
      '<h3 class="pname">'+esc(p.name)+(p.isNew?' <span class="newtag">NEW</span>':'')+'</h3>'+
      '<div class="prices"><span class="r">'+d+'%</span><strong>'+num(p.sale)+'<small>원</small></strong><s>'+won(p.orig)+'</s></div>'+
      '<div class="cmeta">'+
        (sold ? '<span class="cm-l">오늘 마감</span><span class="cm-r sold">품절</span>' :
          '<span class="cm-l"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8.6"/><path d="M12 7.4v4.8l3.1 1.9"/></svg>'+p.pickup+'</span>'+
          '<span class="cm-r">남은 <b>'+p.left+'</b>개</span>')+
      '</div>'+
      '<button class="reserve" type="button" data-act="reserve" data-id="'+p.id+'"'+(sold?' disabled':'')+'>'+(sold?'품절':'지금 예약')+'</button>'+
    '</div>'+
  '</article>';
}
'''
src = src[:s] + CARD_NEW + src[e:]

# ── 4. 검색어 필터 ───────────────────────────────────────────────────────
if "var q = (ui.q || '').toLowerCase();" not in src:
  src = src.replace(
  "    return inRadius(p) && (ui.cat === '전체' || p.cat === ui.cat) && disc(p) >= ui.deal;",
  "    var q = (ui.q || '').toLowerCase();\n"
  "    var hay = (p.name + ' ' + ((storeById(p.store) || {}).name || '')).toLowerCase();\n"
  "    return inRadius(p) && (ui.cat === '전체' || p.cat === ui.cat) && disc(p) >= ui.deal && (!q || hay.indexOf(q) > -1);", 1)

# ── 5. 검색 입력 배선 ────────────────────────────────────────────────────
anchor = "  /* v3.4 · PC/모바일 폭이 바뀌면 지도·피드 레이아웃을 다시 그린다 */"
WIRE = '''  /* v4.0 · 검색 바 */
  var qIn = $('#qInput'), qClr = $('#qClear');
  if(qIn){
    qIn.addEventListener('input', function(){
      ui.q = this.value.trim();
      if(qClr) qClr.hidden = !ui.q;
      renderFeed();
    });
    qIn.addEventListener('search', function(){ ui.q = this.value.trim(); renderFeed(); });
  }
  if(qClr){
    qClr.addEventListener('click', function(){
      if(qIn){ qIn.value = ''; qIn.focus(); }
      ui.q = ''; this.hidden = true; renderFeed();
    });
  }
'''
if "qIn = $('#qInput')" not in src:
  assert anchor in src
  src = src.replace(anchor, WIRE + anchor, 1)

# 온보딩 통계(오늘 마감특가) 동기화
if "obStatDeal" not in src.split("function renderHomeLive")[1][:2000]:
  src = src.replace(
  "  $('#liveDealCount').textContent = live.length;",
  "  $('#liveDealCount').textContent = live.length;\n"
  "  var obd = $('#obStatDeal'); if(obd) obd.innerHTML = live.length + '<em>개</em>';", 1)

# ── 6. CSS 주입 ─────────────────────────────────────────────────────────
css = io.open(CSS, encoding="utf-8").read()
src = re.sub(r'\n<style id="design-v4">.*?</style>\n', '\n', src, flags=re.S)
src = src.replace('</head>', '<style id="design-v4">\n' + css + '\n</style>\n</head>', 1)

io.open(HTML, "w", encoding="utf-8").write(src)
print("patched:", len(orig), "->", len(src))
