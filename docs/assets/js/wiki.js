/* Western Defense — mejoras de lectura del sitio.
 *
 * TODO lo importante ya funciona sin JavaScript: GitHub Pages renderiza los
 * documentos canónicos, resuelve los enlaces .md entre ellos (jekyll-relative-links)
 * y genera anclas con el mismo id que en GitHub. Este archivo solo agrega
 * comodidades encima:
 *
 *   1. Índice de contenidos por página (los canónicos no llevan marcador {:toc},
 *      y no se los vamos a meter: son fuente canónica).
 *   2. Los enlaces relativos que NO son documentos (../../tools/*.py y demás)
 *      apuntan a archivos del repo que no se publican: los mandamos a GitHub.
 *   3. Enlace permanente al pasar por un título, tablas con scroll en móvil y
 *      botón de volver arriba.
 *
 * Si el JS no carga, la página se lee igual de bien: solo pierde estos extras.
 */
(function () {
  'use strict';

  var REPO_BLOB = 'https://github.com/lordiwa/western-defense/blob/main/';

  var content = document.querySelector('.content');
  if (!content) return;

  var srcdir = (content.getAttribute('data-srcdir') || 'docs').replace(/^\/+|\/+$/g, '');

  /* ---------- 1. Índice de contenidos ---------- */

  var headings = [].slice.call(content.querySelectorAll('h2[id], h3[id]'));

  if (headings.length >= 4) {
    var toc = document.createElement('nav');
    toc.className = 'toc';
    toc.setAttribute('aria-label', 'Contenido de la página');

    var label = document.createElement('p');
    label.textContent = 'Contenido';
    toc.appendChild(label);

    var root = document.createElement('ul');
    toc.appendChild(root);
    var sub = null;

    headings.forEach(function (h) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = '#' + h.id;
      // Sin el "§" que añadimos más abajo ni espacios de sobra.
      a.textContent = (h.textContent || '').replace(/\s*§\s*$/, '').trim();
      li.appendChild(a);

      if (h.tagName === 'H2') {
        root.appendChild(li);
        sub = null;
      } else {
        if (!sub) {
          sub = document.createElement('ul');
          (root.lastElementChild || root).appendChild(sub);
        }
        sub.appendChild(li);
      }
    });

    var firstH1 = content.querySelector('h1');
    if (firstH1) {
      firstH1.parentNode.insertBefore(toc, firstH1.nextSibling);
    } else {
      content.insertBefore(toc, content.firstChild);
    }
  }

  /* ---------- 2. Enlaces a archivos del repo que no se publican ---------- */

  [].forEach.call(content.querySelectorAll('a[href]'), function (a) {
    var href = a.getAttribute('href');

    // Anclas, rutas ya resueltas del sitio y URLs completas: no se tocan.
    if (!href || href.charAt(0) === '#' || href.charAt(0) === '/' ||
        /^[a-z][a-z0-9+.-]*:/i.test(href)) {
      return;
    }

    var path;
    try {
      // Resolvemos contra un origen ficticio para que el navegador normalice
      // los "../" por nosotros, y quedarnos con la ruta relativa al repo.
      path = decodeURIComponent(new URL(href, 'https://repo.invalid/' + srcdir + '/').pathname)
        .replace(/^\/+/, '');
    } catch (e) {
      return;
    }

    a.setAttribute('href', REPO_BLOB + path);
    a.classList.add('ext-repo');
    a.setAttribute('rel', 'noopener');
  });

  /* ---------- 3. Detalles de lectura ---------- */

  [].forEach.call(content.querySelectorAll('h2[id], h3[id]'), function (h) {
    if (h.querySelector('.anchor-link')) return;
    var link = document.createElement('a');
    link.className = 'anchor-link';
    link.href = '#' + h.id;
    link.setAttribute('aria-label', 'Enlace a esta sección');
    link.textContent = '§';
    h.appendChild(link);
  });

  // Las tablas del índice de la wiki son anchas: que scrolleen solas en móvil.
  [].forEach.call(content.querySelectorAll('table'), function (t) {
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
    var sync = function () { toTop.classList.toggle('visible', window.scrollY > 600); };
    window.addEventListener('scroll', sync, { passive: true });
    sync();
  }
})();
