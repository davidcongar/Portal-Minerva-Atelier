// /static/js/system/calendar.js
// Requires: FullCalendar 6.x (with locales), flatpickr (range mode), your dynamic_modal.js (openActions/closeActions)
(function () {
  let calendar;                // FullCalendar instance (singleton per page)
  let initialized = false;     // avoid double init/renders

  /**
   * Utility: read table endpoint + columns from the hidden #table-data element.
   */
  function getTableMeta() {
    const el = document.getElementById('table-data');
    if (!el) return null;
    const url = el.getAttribute('data-table');          // e.g. /dynamic/<table_name>/data
    let columns;
    try { columns = JSON.parse(el.getAttribute('data-columns') || '[]'); }
    catch { columns = []; }
    // Try to infer table_name from the path so we can call openActions('dynamic/<table_name>', id, estatus)
    let tableName = '';
    if (typeof url === 'string') {
      const parts = url.split('/').filter(Boolean);
      // .../dynamic/<name>/data  OR  .../report_queries/<name>/data
      const nameIndex = parts.findIndex(p => p === 'dynamic' || p === 'report_queries');
      if (nameIndex > -1 && parts[nameIndex + 1]) tableName = parts[nameIndex + 1];
    }
    return { url, columns, tableName };
  }


  /**
   * Utility: pick a decent title field from available columns.
   * Falls back to first non-id/non-fecha column, else "Registro <id>".
   */
  function chooseTitleField(columns) {
    if (!Array.isArray(columns) || !columns.length) return null;
    const lowered = columns.map(c => String(c).toLowerCase());
    // preferred common title-ish columns:
    const candidates = ['titulo', 'title','id_empleado_nombre_completo', 'id_cliente_nombre', 'name', 'descripcion', 'description', 'asunto', 'concepto'];
    for (const c of candidates) {
      const i = lowered.indexOf(c);
      if (i !== -1) return columns[i];
    }
    // otherwise first that isn't obviously an id/fecha/estatus/monto-type
    for (let i = 0; i < columns.length; i++) {
      const c = lowered[i];
      if (!/^(id|fecha|estatus|status|monto|importe|precio)$/.test(c)) return columns[i];
    }
    return null;
  }
  const employeeColors = {};
  function getColorForEmpleado(id) {
    if (!id) return '#999'; // fallback gray
    if (!employeeColors[id]) {
      // generate a color (HSL cycle)
      const hue = Object.keys(employeeColors).length * 47 % 360; // spread hues
      employeeColors[id] = `hsl(${hue}, 70%, 50%)`;
    }
    return employeeColors[id];
  }

  /**
   * Fetch items from the same endpoint as the table.
   * Tries to pass start/end as query params; if backend ignores them, we’ll filter client-side.
   */
  async function fetchItems(url, search = '') {
    const u = new URL(url, window.location.origin);
    if (search) u.searchParams.set('search', search);
    const res = await fetch(u.toString(), { headers: { 'Accept': 'application/json' } });
    if (!res.ok) throw new Error(`Error al obtener datos (${res.status})`);
    const data = await res.json();
    // Common server shapes: {items: [...], total: n} OR just [...]
    return Array.isArray(data) ? data : (Array.isArray(data.items) ? data.items : []);
  }

  /**
   * Transform table items -> FullCalendar events.
   * Expects each record to have at least: id, fecha (date or datetime), estatus (optional).
   * Title is inferred from columns.
   */
  function toEvents(items, columns) {
    const titleField = chooseTitleField(columns);
    return items
      .filter(r => r && r[date_variable_back])
      .map(r => {
        const date = new Date(`${r[date_variable_back]}T${'00:00'}`);
        let start_date;
        let end_date;
        let allDay;
        start_date=`${r[date_variable_back]}`
        allDay=false;
        end_date=null
        const baseTitle =(titleField && r[titleField]) ? String(r[titleField]) : `Registro ${r.id ?? ''}`.trim();
        const title = `${baseTitle}`;
        return {
          id: r.id,
          title,
          start: start_date,
          end: end_date,
          allDay,
          
          backgroundColor: getColorForEmpleado(r.id_empleado || r.id_cliente), 
          borderColor: getColorForEmpleado(r.id_empleado || r.id_cliente),     
          textColor: '#fff', // optional contrast
          extendedProps: {
            estatus: r.estatus ?? r.status ?? null,
            record: r
          }
        };
      })
      .filter(e => e.start);
  }

  /**
   * PUBLIC: Initialize (or refresh) the Calendar view.
   * Options:
   *   - calendarEl: HTMLElement or selector (defaults to '#calendar_view')
   *   - locale: FullCalendar locale string, defaults 'es'
   */
  window.InitCalendar = async function InitCalendar(opts = {}) {
    const { calendarEl = '#calendar_view', locale = 'es' } = opts;
    const meta = getTableMeta();
    if (!meta || !meta.url) {
      console.warn('[InitCalendar] No se encontró #table-data con atributos data-table / data-columns.');
      return;
    }

    const calEl = (typeof calendarEl === 'string') ? document.querySelector(calendarEl) : calendarEl;
    if (!calEl) {
      console.warn('[InitCalendar] No existe el contenedor para el calendario.');
      return;
    }
    // Read optional search and date range UI if present
    const searchInput = document.getElementById('search');

    // Show calendar container (in case it's hidden) before render
    calEl.style.display = 'block';
    if(!calendar){
      showLoader(); 
    }
    // Fetch records and build events
    let items = [];
    try {
      items = await fetchItems(meta.url, searchInput?.value || '');
    } catch (e) {
      console.error('[InitCalendar] Error al cargar datos:', e);
    }
    const events = toEvents(items, meta.columns);
    // (Re)create calendar instance
    if (calendar) {
      calendar.removeAllEvents();
      calendar.addEventSource(events);
      calendar.refetchEvents();
      // Ensure it's visible and sized correctly
      calendar.updateSize();
      calendar.render();
    } else {
      calendar = new FullCalendar.Calendar(calEl, {
        initialView: 'dayGridMonth',
        locale,
        eventDisplay: 'block',   // 👈 force block rendering in month view
        height: 'auto',
        slotMinTime: '08:00:00',     // 👈 start of business hours
        slotMaxTime: '22:00:00',  
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        buttonText: {
          today: 'Hoy',
          month: 'Mes',
          week: 'Semana',
          day: 'Día',
        },
        navLinks: true,
        nowIndicator: true,
        weekNumbers: false,
        events,
        eventClick(info) {
          try {
            const id = info?.event?.id;
            const estatus = info?.event?.extendedProps?.estatus ?? null;
            if (typeof window.openActions === 'function' && id != null) {
              // dynamic/<table_name>
              const base = meta.tableName ? `dynamic/${meta.tableName}` : 'dynamic';
              window.openActions(base, id, estatus);
            } else {
              console.warn('[InitCalendar] openActions no está disponible o faltan datos del evento.');
            }
          } catch (err) {
            console.error('[InitCalendar] Error al abrir modal dinámico:', err);
          }
        },
      });
      calendar.updateSize();
      calendar.render();
    }

    // Only wire listeners once
    if (!initialized) {
      initialized = true;

      // Rebuild calendar when search or date range changes
      if (searchInput) {
        searchInput.addEventListener('input', debounce(() => {
          window.InitCalendar({ calendarEl: calEl, locale });
        }, 300));
      }


      // When the container becomes visible again (e.g., toggling from table -> calendar), force a resize
      const visObs = new IntersectionObserver(() => {
        if (calendar) {
          calendar.updateSize();
          calendar.render();
        }
      }, { threshold: 0.1 });
      visObs.observe(calEl);

      // Optional: expose a destroy helper
      window.DestroyCalendar = function () {
        try { visObs.disconnect(); } catch {}
        if (calendar) { calendar.destroy(); calendar = null; }
        initialized = false;
      };
    }
    hideLoader(); 
  };

  // Small debounce helper
  function debounce(fn, wait) {
    let t;
    return function (...args) {
      clearTimeout(t);
      t = setTimeout(() => fn.apply(this, args), wait);
    };
  }
})();
// Alpine component to toggle between table and calendar
window.calendarComponent = function () {
  return {
    mode: 'table',      // 'table' | 'calendar'
    loading: false,

    init() {
      this._applyVisibility();
      // this.calendar_view(); // uncomment to default to calendar
    },

    table_view() {
      this.mode = 'table';
      this._applyVisibility();
    },

    async calendar_view() {
      this.mode = 'calendar';
      this._applyVisibility();
      this.loading = true;

      try {
        await Promise.resolve(); // microtask
        await window.InitCalendar(); // renders into #calendar_view by default
      } finally {
        this.loading = false;
      }
    },

    _applyVisibility() {
      const tableEl     = document.getElementById('table_view');     // <-- unified id
      const calendarEl  = document.getElementById('calendar_view');  // <-- unified id
      if (tableEl)    tableEl.style.display    = (this.mode === 'table') ? '' : 'none';
      if (calendarEl) calendarEl.style.display = (this.mode === 'calendar') ? '' : 'none';
    }
  };
};

function calendar_view() {
  // Try to find any element whose x-data contains 'calendarComponent'
  const root = Array.from(document.querySelectorAll('[x-data]'))
    .find(el => (el.getAttribute('x-data') || '').includes('calendarComponent'));

  // If Alpine is ready and the method exists, use it
  if (root && root.__x && root.__x.$data?.calendar_view) {
    root.__x.$data.calendar_view();
    const btn = document.getElementById('calendar_button');
    if (btn) btn.textContent = 'Tabla';
    return;
  }

  // If Alpine isn't ready yet, queue after init once
  if (!root || !root.__x) {
    document.addEventListener('alpine:initialized', () => calendar_view(), { once: true });
    // Fallback manual toggle now (optional)
  }

  // Fallback: manual DOM toggle
  const tabla = document.getElementById('table_view');
  const pagination = document.getElementById('pagination');
  const wrap = document.getElementById('calendar_wrapper');
  const btn = document.getElementById('calendar_button');

  if (tabla) tabla.style.display = 'none';
  if (pagination) pagination.style.display = 'none';
  if (wrap)  wrap.style.display  = 'block';
  if (btn)   btn.textContent = 'Tabla';
  if (typeof window.InitCalendar === 'function') {
    window.InitCalendar();
  }
}

function table_view() {
  const root = Array.from(document.querySelectorAll('[x-data]'))
    .find(el => (el.getAttribute('x-data') || '').includes('calendarComponent'));
  if (root && root.__x && root.__x.$data?.table_view) {
    root.__x.$data.table_view();
    const btn = document.getElementById('calendar_button');
    if (btn) btn.textContent = 'Calendario';
    return;
  }

  // Fallback
  const tabla = document.getElementById('table_view');
  const pagination = document.getElementById('pagination');
  const wrap = document.getElementById('calendar_wrapper');
  const btn = document.getElementById('calendar_button');

  if (tabla) tabla.style.display = 'block';
  if (pagination) pagination.style.display = 'block';
  if (wrap)  wrap.style.display  = 'none';
  if (btn)   btn.textContent = 'Calendario';
}
