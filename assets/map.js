(function () {
  'use strict';

  var HOODS = [
    { id: 'coral-gables', name: 'Coral Gables', county: 'Miami-Dade', lat: 25.7215, lng: -80.2684, report: '2 Kasım', line: 'Ağaçlıklı sokaklar, yürünebilir bir merkez ve Akdeniz tarzı evler.' },
    { id: 'coconut-grove', name: 'Coconut Grove', county: 'Miami-Dade', lat: 25.7280, lng: -80.2430, report: '9 Kasım', line: 'Miami’nin en eski mahallesi: marinalar, körfez parkları ve köy sakinliği.' },
    { id: 'pinecrest', name: 'South Miami & Pinecrest', county: 'Miami-Dade', lat: 25.6680, lng: -80.3020, report: '16 Kasım', line: 'Geniş arsalar ve bahçeli müstakil evler.' },
    { id: 'key-biscayne', name: 'Key Biscayne', county: 'Miami-Dade', lat: 25.6930, lng: -80.1626, report: '23 Kasım', line: 'Şehir merkezine tek bir köprüyle bağlı ada hayatı.' },
    { id: 'south-beach', name: 'South Beach', county: 'Miami-Dade', lat: 25.7826, lng: -80.1341, report: '30 Kasım', line: 'Art Deco binalar, plaj ve Ocean Drive’ın enerjisi.' },
    { id: 'wynwood', name: 'Wynwood & Design District', county: 'Miami-Dade', lat: 25.8060, lng: -80.1960, report: '7 Aralık', line: 'Duvar resimleri, galeriler ve lüks butikler.' },
    { id: 'brickell', name: 'Brickell', county: 'Miami-Dade', lat: 25.7617, lng: -80.1918, report: '14 Aralık', line: 'Miami’nin finans merkezi; arabasız yaşamın gerçekten mümkün olduğu yer.' },
    { id: 'edgewater', name: 'Downtown & Edgewater', county: 'Miami-Dade', lat: 25.7930, lng: -80.1880, report: '21 Aralık', line: 'Biscayne Körfezi’nde en hızlı değişen silüet.' },
    { id: 'little-havana', name: 'Little Havana', county: 'Miami-Dade', lat: 25.7656, lng: -80.2190, report: '4 Ocak', line: 'Calle Ocho ve Miami’nin Latin kalbi.' },
    { id: 'doral', name: 'Doral', county: 'Miami-Dade', lat: 25.8195, lng: -80.3553, report: '11 Ocak', line: 'Yeni yapılar, golf sahaları ve havalimanına hızlı erişim.' },
    { id: 'north-beach', name: 'Mid-Beach & North Beach', county: 'Miami-Dade', lat: 25.8450, lng: -80.1205, report: '18 Ocak', line: 'Miami Beach’in daha sakin yüzü.' },
    { id: 'bal-harbour', name: 'Surfside & Bal Harbour', county: 'Miami-Dade', lat: 25.8840, lng: -80.1220, report: '25 Ocak', line: 'Sakin sahil sokakları ve Bal Harbour Shops.' },
    { id: 'sunny-isles', name: 'Sunny Isles Beach', county: 'Miami-Dade', lat: 25.9420, lng: -80.1220, report: '1 Şubat', line: 'Okyanus kıyısında kuleler ve markalı rezidanslar.' },
    { id: 'aventura', name: 'Aventura', county: 'Miami-Dade', lat: 25.9480, lng: -80.1400, report: '8 Şubat', line: 'Alışveriş, marinalar ve Intracoastal kıyısında yüksek katlı yaşam.' },
    { id: 'hallandale', name: 'Hallandale Beach', county: 'Broward', lat: 25.9812, lng: -80.1484, report: '15 Şubat', line: 'Miami’ye yakın, Broward fiyatlarında.' },
    { id: 'hollywood', name: 'Hollywood', county: 'Broward', lat: 26.0112, lng: -80.1300, report: '22 Şubat', line: 'Broadwalk boyunca bisikletle sahil hayatı.' },
    { id: 'weston', name: 'Weston', county: 'Broward', lat: 26.1004, lng: -80.3998, report: '1 Mart', line: 'Göller, geniş evler ve sakin sokaklarla planlı bir şehir.' },
    { id: 'fort-lauderdale', name: 'Fort Lauderdale', county: 'Broward', lat: 26.1194, lng: -80.1300, report: '8 Mart', line: 'Las Olas, Victoria Park ve kanal kenarında yaşam.' },
    { id: 'wilton-manors', name: 'Wilton Manors', county: 'Broward', lat: 26.1604, lng: -80.1389, report: '15 Mart', line: 'Fort Lauderdale’e dakikalar mesafede renkli, küçük bir şehir.' },
    { id: 'pompano', name: 'Lighthouse Point & Pompano', county: 'Broward', lat: 26.2600, lng: -80.0990, report: '22 Mart', line: 'Derin su kanalları ve tekne sahipleri için tasarlanmış evler.' },
    { id: 'deerfield', name: 'Deerfield Beach', county: 'Broward', lat: 26.3184, lng: -80.0998, report: '29 Mart', line: 'İki büyük şehrin arasında sahil kasabası hissi.' },
    { id: 'boca-raton', name: 'Boca Raton', county: 'Palm Beach', lat: 26.3587, lng: -80.0900, report: '5 Nisan', line: 'Golf sahaları, plajlar ve bakımlı bir şehir merkezi.' }
  ];

  // Approximate county lines (east-west) and extents for the overlay.
  var PB_BR = 26.3220;   // Palm Beach / Broward
  var BR_MD = 25.9567;   // Broward / Miami-Dade (County Line Rd)
  var WEST = -80.90, EAST_LAND = -80.06, EAST = -79.90;
  var COUNTY_BOUNDS = {
    'Palm Beach': [[-80.45, 26.30], [-79.98, 26.50]],
    'Broward': [[-80.48, 25.94], [-80.02, 26.34]],
    'Miami-Dade': [[-80.48, 25.60], [-80.08, 25.98]],
    'All': [[-80.50, 25.60], [-79.95, 26.45]]
  };

  var state = { selected: 'brickell', county: 'All' };
  var map = null;
  var markers = {};
  var countyLabels = {};

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function byId(id) { for (var i = 0; i < HOODS.length; i++) { if (HOODS[i].id === id) return HOODS[i]; } return null; }

  function renderCard(h) {
    var card = $('#hood-card');
    if (!card) return;
    $('.county', card).textContent = h.county;
    $('h3', card).textContent = h.name;
    $('p', card).textContent = h.line;
    $('.report strong', card).textContent = h.report;
  }

  function updateMarkers() {
    HOODS.forEach(function (h) {
      var el = markers[h.id] && markers[h.id].getElement();
      if (!el) return;
      el.classList.toggle('on', h.id === state.selected);
      el.classList.toggle('dim', state.county !== 'All' && h.county !== state.county);
      el.setAttribute('aria-pressed', h.id === state.selected ? 'true' : 'false');
    });
    $all('.chip[data-hood]').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-hood') === state.selected ? 'true' : 'false');
    });
    $all('.counties button').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-county') === state.county ? 'true' : 'false');
    });
    Object.keys(countyLabels).forEach(function (c) {
      countyLabels[c].getElement().classList.toggle('on', c === state.county);
    });
    if (map && map.getLayer('county-shade')) {
      map.setPaintProperty('county-shade', 'fill-opacity', [
        'case', ['any', ['==', state.county, 'All'], ['==', ['get', 'county'], state.county]], 0, 0.55
      ]);
    }
  }

  function select(id, fly) {
    var h = byId(id);
    if (!h) return;
    state.selected = id;
    renderCard(h);
    updateMarkers();
    if (map && fly !== false) {
      var wide = window.matchMedia('(min-width: 901px)').matches;
      map.flyTo({ center: [h.lng, h.lat], zoom: Math.max(map.getZoom(), 12), offset: wide ? [-150, 0] : [0, 0], speed: 1.2 });
    }
  }

  function setCounty(c) {
    state.county = c;
    updateMarkers();
    if (map) {
      var wide = window.matchMedia('(min-width: 901px)').matches;
      map.fitBounds(COUNTY_BOUNDS[c], { padding: wide ? { top: 140, bottom: 110, left: 60, right: 440 } : 30, duration: 1100 });
    }
  }

  function countyGeo() {
    function box(name, s, n) {
      return { type: 'Feature', properties: { county: name }, geometry: { type: 'Polygon', coordinates: [[[WEST, s], [EAST, s], [EAST, n], [WEST, n], [WEST, s]]] } };
    }
    return {
      shade: { type: 'FeatureCollection', features: [box('Palm Beach', PB_BR, 27.0), box('Broward', BR_MD, PB_BR), box('Miami-Dade', 25.0, BR_MD)] },
      lines: { type: 'FeatureCollection', features: [
        { type: 'Feature', properties: {}, geometry: { type: 'LineString', coordinates: [[WEST, PB_BR], [EAST_LAND, PB_BR]] } },
        { type: 'Feature', properties: {}, geometry: { type: 'LineString', coordinates: [[WEST, BR_MD], [-80.115, BR_MD]] } }
      ] }
    };
  }

  function initMap() {
    var shell = $('.map-shell');
    if (!window.maplibregl || !$('#map')) { if (shell) shell.classList.add('no-map'); return; }
    try {
      map = new maplibregl.Map({
        container: 'map',
        style: 'https://tiles.openfreemap.org/styles/dark',
        bounds: COUNTY_BOUNDS['Miami-Dade'],
        fitBoundsOptions: { padding: window.matchMedia('(min-width: 901px)').matches ? { top: 140, bottom: 110, left: 60, right: 440 } : 20 },
        cooperativeGestures: true,
        attributionControl: { compact: true },
        maxZoom: 16,
        minZoom: 7
      });
    } catch (e) {
      if (shell) shell.classList.add('no-map');
      return;
    }
    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'bottom-right');

    map.on('load', function () {
      var g = countyGeo();
      map.addSource('county-shade', { type: 'geojson', data: g.shade });
      map.addLayer({ id: 'county-shade', type: 'fill', source: 'county-shade', paint: { 'fill-color': '#000000', 'fill-opacity': 0 } });
      map.addSource('county-lines', { type: 'geojson', data: g.lines });
      map.addLayer({ id: 'county-lines', type: 'line', source: 'county-lines', paint: { 'line-color': '#8A8378', 'line-width': 1.4, 'line-dasharray': [4, 3] } });
      updateMarkers();
    });

    [['Palm Beach', 26.345], ['Broward', 25.985], ['Miami-Dade', 25.930]].forEach(function (c) {
      var el = document.createElement('div');
      el.className = 'county-label';
      el.textContent = c[0];
      countyLabels[c[0]] = new maplibregl.Marker({ element: el, anchor: 'left' }).setLngLat([-80.62, c[1]]).addTo(map);
    });

    HOODS.forEach(function (h) {
      var el = document.createElement('button');
      el.type = 'button';
      el.className = 'hood-marker';
      el.setAttribute('aria-label', h.name);
      el.innerHTML = '<span class="dot" aria-hidden="true"></span><span class="lbl"></span>';
      el.querySelector('.lbl').textContent = h.name;
      el.addEventListener('click', function (ev) { ev.stopPropagation(); select(h.id); });
      markers[h.id] = new maplibregl.Marker({ element: el, anchor: 'left', offset: [-22, 0] }).setLngLat([h.lng, h.lat]).addTo(map);
    });
    updateMarkers();
  }

  function initControls() {
    $all('.chip[data-hood], .hood-index button[data-hood]').forEach(function (b) {
      b.addEventListener('click', function () {
        select(b.getAttribute('data-hood'));
        if (b.closest('.hood-index')) { $('.map-shell').scrollIntoView({ behavior: 'smooth', block: 'start' }); }
      });
    });
    $all('.counties button').forEach(function (b) {
      b.addEventListener('click', function () { setCounty(b.getAttribute('data-county')); });
    });
    var form = $('#map-search');
    if (form) {
      form.addEventListener('submit', function (ev) {
        ev.preventDefault();
        var q = ($('input', form).value || '').trim().toLocaleLowerCase('tr');
        if (!q) return;
        var hit = HOODS.filter(function (h) { return h.name.toLocaleLowerCase('tr').indexOf(q) !== -1; })[0];
        if (hit) { select(hit.id); return; }
        window.open('https://aleynabozoklar.com/search', '_blank', 'noopener');
      });
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    renderCard(byId(state.selected));
    initControls();
    initMap();
  });
})();
