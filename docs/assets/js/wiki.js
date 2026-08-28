/* Western Defense — pegamento del sitio.
 *
 * El contenido canónico (GDD.md, TECH.md, WIKI.md, wiki/README.md) se publica
 * SIN tocarlo, así que dos cosas que en GitHub funcionan solas hay que
 * arreglarlas acá, en el navegador:
 *
 *  1. ENLACES. El markdown canónico enlaza a archivos del repo (`../WIKI.md`,
 *     `wiki/README.md`, `../../tools/wiki_to_resources.py`). Servidos tal cual
 *     bajarían markdown crudo. Los mapeamos a las páginas del sitio, y lo que
 *     no sea documento del sitio se manda al repo en GitHub.
 *
 *  2. ANCLAS. kramdown (el renderizador de GitHub Pages) genera ids ASCII y sin
 *     los números de sección: "### 2.1 Categoría ladron" -> "categora-ladron".
 *     El índice de la wiki enlaza con el id estilo GitHub ("#21-categoría-ladron"),
 *     que es el que vale en el repo. Añadimos ese id como alias para que los
 *     enlaces canónicos funcionen sin editar ni una línea del markdown.
 *
 * Todo esto es progresivo: sin JS el contenido igual se ve completo y
 * renderizado; solo pierde el remapeo de enlaces y los alias de ancla.
 */
(function () {
  'use strict';

  var script = document.currentScript;
  var BASE = (script && script.getAttribute('data-base')) || '';

  /* Ruta del repo -> página del sitio. Las claves son relativas a la raíz del
     repositorio, que es como resolvemos los enlaces del markdown. */
  var PAGES = {
    'docs/GDD.md': '/gdd/',
    'docs/TECH.md': '/tech/',
    'docs/WIKI.md': '/wiki/fichas/',
    'docs/wiki/README.md': '/wiki/'
  };

  var REPO_BLOB = 'https://github.com/lordiwa/western-defense/blob/main/';

  var content = document.querySelector('.content');
  if (!content) return;

  var srcdir = (content.getAttribute('data-srcdir') || 'docs').replace(/^\/+|\/+$/g, '');

  /* ---------- 1. Enlaces ---------- */

  function repoPath(href) {
    // Resolvemos contra un origen ficticio para que el navegador haga el
    // trabajo de normalizar los "../" por nosotros.
    try {
      var u = new URL(href, 'https://repo.invalid/' + srcdir + '/');
      return {
        path: decodeURIComponent(u.pathname).replace(/^\/+/, ''),
        hash: u.hash
      };
    } catch (e) {
      return null;
    }
  }

  Array.prototype.forEach.call(content.querySelectorAll('a[href]'), function (a) {
    var href = a.getAttribute('href');

    // Anclas internas, rutas absolutas del propio sitio y URLs completas
    // (http:, mailto:, …) se quedan como están.
    if (!href || href.charAt(0) === '#' || href.charAt(0) === '/' || /^[a-z][a-z0-9+.-]*:/i.test(href)) {
      return;
    }

    var r = repoPath(href);
    if (!r) return;

    if (Object.prototype.hasOwnProperty.call(PAGES, r.path)) {
      a.setAttribute('href', BASE + PAGES[r.path] + r.hash);
    } else {
      // No es una página del sitio: es un archivo del repo (script, datos,
      // escena). Que lo abra en GitHub, donde se lee bien.
      a.setAttribute('href', REPO_BLOB + r.path + r.hash);
      a.classList.add('ext-repo');
      a.setAttribute('rel', 'noopener');
    }
  });

  /* ---------- 2. Alias de ancla estilo GitHub ---------- */

  function githubSlug(text) {
    var s = text.toLowerCase().trim();
    try {
      s = s.replace(/[^\p{L}\p{N}\s-]/gu, '');
    } catch (e) {
      // Navegador sin property escapes: al menos limpiamos el ASCII.
      s = s.replace(/[^a-z0-9À-ɏ\s-]/g, '');
    }
    return s.replace(/\s+/g, '-');
  }

  var used = {};
  var headings = content.querySelectorAll('h1, h2, h3, h4, h5, h6');

  Array.prototype.forEach.call(headings, function (h) {
    var slug = githubSlug(h.textContent || '');
    if (!slug) return;

    // GitHub desambigua repeticiones con -1, -2, …
    if (Object.prototype.hasOwnProperty.call(used, slug)) {
      used[slug] += 1;
      slug = slug + '-' + used[slug];
    } else {
      used[slug] = 0;
    }

    if (h.id !== slug && !document.getElementById(slug)) {
      // Ancla invisible ANTES del título: así no pisamos el id de kramdown,
      // del que cuelga el índice de contenidos de la página.
      var anchor = document.createElement('span');
      anchor.id = slug;
      anchor.className = 'anchor-alias';
      anchor.style.cssText = 'display:block;position:relative;top:-5rem;visibility:hidden';
      h.parentNode.insertBefore(anchor, h);
    }

    // Enlace permanente clicable sobre el propio título.
    if (h.id && !h.querySelector('.anchor-link')) {
      var link = document.createElement('a');
      link.className = 'anchor-link';
      link.href = '#' + h.id;
      link.setAttribute('aria-label', 'Enlace a esta sección');
      link.textContent = '§';
      h.appendChild(link);
    }
  });

  // Si llegamos con un #ancla que solo existe tras crear los alias, el
  // navegador ya intentó (y falló) el scroll. Lo repetimos ahora.
  if (location.hash.length > 1) {
    var target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (target) target.scrollIntoView();
  }

  /* ---------- 3. Detalles de lectura ---------- */

  // El índice de contenidos se escribe arriba del todo (kramdown necesita el
  // marcador {:toc} en el markdown de la página, antes del include). Leerlo
  // antes del título es raro, así que lo bajamos debajo del h1.
  var toc = content.querySelector('.toc');
  var firstH1 = content.querySelector('h1');
  if (toc && firstH1 && firstH1.compareDocumentPosition(toc) & Node.DOCUMENT_POSITION_PRECEDING) {
    firstH1.parentNode.insertBefore(toc, firstH1.nextSibling);
  }

  // Las tablas del índice son anchas: que scrolleen solas en móvil.
  Array.prototype.forEach.call(content.querySelectorAll('table'), function (t) {
    if (t.parentNode.classList.contains('table-scroll')) return;
    var box = document.createElement('div');
    box.className = 'table-scroll';
    t.parentNode.insertBefore(box, t);
    box.appendChild(t);
  });

  var toTop = document.getElementById('to-top');
  if (toTop) {
    toTop.addEventListener('click', function (e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    var sync = function () {
      toTop.classList.toggle('visible', window.scrollY > 600);
    };
    window.addEventListener('scroll', sync, { passive: true });
    sync();
  }
})();
