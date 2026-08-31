# Capítulo 32: Codificación del frontend

Este capítulo explica cómo se implementa la parte de interfaz de vitalXAI. Las plantillas Jinja2 sirven las vistas definidas en el capítulo 22 y los scripts JavaScript permiten al profesional sanitario y al investigador interactuar con el backend. La aplicación no utiliza un framework de componentes independiente. El contenido se organiza en cuatro apartados: plantillas de presentación, scripts por ámbito, comunicación asíncrona con la API e internacionalización y tema visual.

La presentación se resuelve con las plantillas Jinja2 del directorio `templates/`, que componen las páginas en el servidor, y con los recursos estáticos del directorio `static/`, que incluyen los scripts JavaScript y los estilos. La interactividad se implementa en JavaScript nativo, con módulos por ámbito funcional, y la comunicación con la API se realiza mediante la interfaz de fetch del navegador, con la protección CSRF y la renovación automática de la sesión en las vistas privadas (MDN Web Docs, 2024). El estilo visual se apoya en las utilidades de Tailwind CSS, cargadas mediante CDN y configuradas con el modo oscuro mediante clase (Tailwind CSS, 2024).

La implementación completa de las plantillas, los scripts y los recursos estáticos está disponible en [github.com/eLeCe2611/vitalXAI](https://github.com/eLeCe2611/vitalXAI), en los directorios `templates/` y `static/`. Este capítulo utiliza fragmentos representativos para explicar la estructura de la interfaz y su comunicación con el backend; el repositorio contiene el código completo y su evolución.

## 32.1 Las plantillas de presentación

Las plantillas Jinja2 componen las páginas del sistema en el servidor, inyectando los datos del usuario y los textos de la interfaz. Las páginas principales son el inicio de sesión (`login.html`), el registro (`register.html`), el panel de diagnóstico (`dashboard.html`) y el laboratorio de entrenamiento (`training.html`). Las plantillas combinan la estructura HTML con los atributos de internacionalización `data-i18n`, que el script de idioma traduce dinámicamente, y con las variables de contexto del servidor, como el nombre y el rol del usuario. El fragmento siguiente muestra una sección de la plantilla del panel de diagnóstico.

```html
<div class="p-4 border-b ... bg-blue-50 ...">
    <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-full bg-blue-600 ...">
            <i class="fa-solid fa-user-md text-lg"></i>
        </div>
        <div class="overflow-hidden">
            <p class="text-[10px] font-bold ...">{{ role }}</p>
            <p class="text-sm font-black ...">{{ full_name }}</p>
        </div>
    </div>
</div>

<div class="p-3 space-y-1 border-b ...">
    <a href="/dashboard" class="flex items-center gap-3 px-3 py-2 rounded-lg bg-blue-100 ...">
        <i class="fa-solid fa-stethoscope w-5 text-center"></i>
        <span id="ui-nav-diag" data-i18n="navDiag">Diagnóstico Rápido</span>
    </a>
    <a href="/training" class="flex items-center gap-3 px-3 py-2 rounded-lg ...">
        <i class="fa-solid fa-flask w-5 text-center"></i>
        <span id="ui-nav-lab" data-i18n="navLab">Laboratorio de Entrenamiento</span>
    </a>
</div>
```

*Código 32.1 - Plantilla del panel de diagnóstico (`templates/dashboard.html`)*

La implementación de las plantillas refleja la decisión del diseño de interfaces: las páginas se componen en el servidor con Jinja2, que inyecta el nombre y el rol del usuario, y se sirven como respuestas HTML. Las secciones de la interfaz se identifican con atributos `data-i18n`, que el módulo de idioma traduce sin recargar la página, y la navegación entre el panel y el laboratorio se resuelve con los enlaces de la barra lateral. Las ventanas integran además las vistas del historial, la cola de trabajos y la administración, tal y como se describió en el diseño de interfaces del capítulo 22.

## 32.2 Los recursos JavaScript por ámbito

La interactividad del frontend se implementa en JavaScript nativo, organizado en módulos por ámbito funcional: `dashboard.js` para el panel de diagnóstico, `training.js` para el laboratorio, `admin.js` para la administración y la cola, e `i18n.js` para la internacionalización compartida. Cada módulo se encarga de la interacción de su ventana: la carga y el envío de la radiografía, el sondeo del estado de la cola, el render de los resultados, la gestión de los experimentos del laboratorio y los diálogos de la administración. Los módulos se cargan en las plantillas al final del documento, y se comunican con la API mediante las peticiones asíncronas descritas en el apartado siguiente.

La separación por ámbito refleja la organización del código del frontend: cada módulo conoce los elementos de su ventana y las operaciones de su subsistema, de modo que los cambios de un ámbito no afectan al resto. El módulo `i18n.js` es el único compartido, y se carga en todas las páginas para aplicar el idioma y el tema visual. La coordinación entre módulos se resuelve mediante la ventana global, que expone las funciones de interacción que las plantillas invocan desde los atributos de los elementos, como el envío de la imagen o la apertura del detalle de una consulta.

## 32.3 Comunicación asíncrona con la API

La comunicación con la API se realiza mediante la interfaz de fetch del navegador, con el envío de los formularios de forma asíncrona mediante `FormData`, de modo que las operaciones se procesan sin recargar la página. La protección CSRF se gestiona mediante un interceptor global de peticiones, que añade la cabecera `X-CSRF-Token` a las peticiones que modifican el estado y gestiona la renovación automática de la sesión ante una respuesta de no autenticado. El fragmento siguiente muestra la implementación del interceptor global.

```javascript
(function() {
    const c = document.cookie.match(/csrf_token=([^;]+)/);
    if (!c) return;
    const csrfToken = c[1];
    const origFetch = window.fetch;
    let _isRefreshing = false;
    window.fetch = async function(url, options) {
        if (options && (options.method || 'GET').toUpperCase() !== 'GET') {
            options = Object.assign({}, options);
            options.headers = Object.assign({}, options.headers || {});
            options.headers['X-CSRF-Token'] = csrfToken;
        }
        let response = await origFetch(url, options);
        if (response.status === 401 && !_isRefreshing) {
            _isRefreshing = true;
            try {
                const refreshResp = await origFetch('/api/token/refresh', { method: 'POST', headers: { 'X-CSRF-Token': csrfToken } });
                if (refreshResp.ok) {
                    response = await origFetch(url, options);
                } else {
                    window.location.href = '/';
                    return response;
                }
            } catch (e) {
                window.location.href = '/';
            } finally {
                _isRefreshing = false;
            }
        }
        return response;
    };
})();
```

*Código 32.2 - Interceptor global de peticiones con CSRF y renovación de sesión (`static/js/admin.js`)*

La implementación de la comunicación asíncrona refleja las decisiones de seguridad y de experiencia del sistema. El interceptor reemplaza la función `fetch` global en las vistas que cargan `admin.js`: añade la cabecera `X-CSRF-Token` con el token de la cookie a las peticiones que modifican el estado, en correspondencia con la protección CSRF del backend descrita en el capítulo 28, y ante una respuesta de no autenticado intenta renovar la sesión mediante el endpoint de refresco. Si la renovación tiene éxito reintenta la petición original; en caso contrario redirige a la página de inicio. El mecanismo centraliza esta gestión, aunque no constituye una garantía de disponibilidad continua de la sesión.

## 32.4 Internacionalización y tema visual

La internacionalización y el tema visual se implementan en el módulo `i18n.js`, compartido por todas las páginas. La internacionalización mantiene un diccionario de traducciones en el navegador para los cuatro idiomas soportados, aplica los textos a los elementos `data-i18n` y persiste la preferencia del idioma en el almacenamiento local. El tema visual alterna entre los modos claro y oscuro mediante la clase del elemento raíz y, cuando no existe una preferencia guardada, consulta la preferencia del sistema mediante `matchMedia`; estas APIs de almacenamiento y consulta del entorno pertenecen a la plataforma web del navegador (MDN Web Docs, 2024). El fragmento siguiente muestra la implementación de la traducción y del cambio de idioma.

```javascript
function t(key) {
    const lang = currentLang || localStorage.getItem('appLang') || 'es';
    const langDict = dict[lang] || dict.es;
    return langDict[key] || dict.es[key] || key;
}

function changeLanguage() {
    const selector = document.getElementById('lang-selector');
    if (selector) currentLang = selector.value;
    localStorage.setItem('appLang', currentLang);
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        el.innerText = t(key);
    });
}

function toggleTheme() {
    const html = document.documentElement;
    if (html.classList.contains('dark')) {
        html.classList.remove('dark');
        localStorage.setItem('theme', 'light');
    } else {
        html.classList.add('dark');
        localStorage.setItem('theme', 'dark');
    }
}
```

*Código 32.3 - Internacionalización y tema visual (`static/js/i18n.js`)*

La implementación de la internacionalización refleja las decisiones del diseño del CU-004: el selector de idioma actualiza la preferencia en el almacenamiento local y traduce de forma inmediata los textos de la interfaz marcados con `data-i18n`, sin recargar la página, con el español como valor por defecto. El tema visual alterna la clase del modo oscuro en el elemento raíz, de modo que el cambio se propaga a toda la interfaz, y persiste la preferencia en el almacenamiento local; al cargar la página, se restaura la preferencia guardada y, en ausencia de esta, se respeta la preferencia de color del sistema. Los módulos de las ventanas complementan la traducción re-renderizando las vistas dinámicas, como el historial o los resultados del laboratorio, en el idioma seleccionado.

El frontend de vitalXAI queda descrito en sus elementos principales: las plantillas Jinja2 componen las ventanas en el servidor, los recursos JavaScript por ámbito gestionan la interacción de cada vista, la comunicación asíncrona se protege con el interceptor CSRF y la renovación de sesión, y la internacionalización con el tema visual se aplican de forma transversal. Junto con la codificación del backend, de la ejecución asíncrona y de los motores, este capítulo completa la descripción de la implementación del sistema vitalXAI.
