/* Fire & Light Stellenbosch — interactions
   Progressive enhancement only: every page works with JS disabled. */
(function () {
  'use strict';

  /* --- Mobile navigation ------------------------------------------------ */

  var burger = document.querySelector('.fl-burger');
  var nav = document.getElementById('fl-nav');

  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
      document.body.style.overflow = !open ? 'hidden' : '';
    });
  }

  /* --- Dropdowns -------------------------------------------------------- */

  var toggles = document.querySelectorAll('.fl-nav__toggle');

  Array.prototype.forEach.call(toggles, function (btn) {
    var item = btn.closest('.fl-nav__item');

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var open = item.classList.contains('is-open');
      closeAll();
      if (!open) {
        item.classList.add('is-open');
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });

  function closeAll() {
    Array.prototype.forEach.call(document.querySelectorAll('.fl-nav__item.is-open'), function (i) {
      i.classList.remove('is-open');
      var t = i.querySelector('.fl-nav__toggle');
      if (t) t.setAttribute('aria-expanded', 'false');
    });
  }

  document.addEventListener('click', function (e) {
    if (!e.target.closest('.fl-nav__item')) closeAll();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    closeAll();
    if (nav && nav.classList.contains('is-open') && burger) {
      nav.classList.remove('is-open');
      burger.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
      burger.focus();
    }
  });

  /* --- Hero intro video --------------------------------------------------
     Silent 5s brand loop. If the file is missing, the codec is unsupported,
     autoplay is blocked, or the visitor prefers reduced motion, the video is
     removed and the poster still remains — the hero never ends up blank. */

  var brandVideos = document.querySelectorAll(
    '.fl-hero__markvideo, .fl-tagline-band__video');

  var reduceMotion = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  Array.prototype.forEach.call(brandVideos, function (vid) {
    if (reduceMotion) {
      vid.removeAttribute('autoplay');
      vid.pause();                     // the static artwork stays in place
      return;
    }

    // Only reveal a video once it is genuinely playing; until then the static
    // artwork holds the space, so there is never a blank or half-lit frame.
    vid.addEventListener('playing', function () { vid.classList.add('is-ready'); });

    var play = vid.play();
    if (play && typeof play.catch === 'function') {
      play.catch(function () { /* autoplay refused — static artwork stays */ });
    }
  });

  /* --- Sticky header shadow --------------------------------------------- */

  var header = document.querySelector('.fl-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-stuck', window.scrollY > 8);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* --- Reveal on scroll -------------------------------------------------- */

  var reveals = document.querySelectorAll('.fl-reveal');

  function revealAll() {
    Array.prototype.forEach.call(reveals, function (el) { el.classList.add('is-in'); });
  }

  if (reveals.length) {
    if (!('IntersectionObserver' in window)) {
      revealAll();
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });

      Array.prototype.forEach.call(reveals, function (el) { io.observe(el); });

      /* Safety net: an observer that never fires (backgrounded tab, prerender,
         an aggressive extension) must never leave the page permanently blank.
         After 3s, show everything regardless. */
      window.setTimeout(revealAll, 3000);
    }
  }

  /* --- Contact form ------------------------------------------------------
     The form has no backend yet. Rather than pretend to send, it hands the
     message to the visitor's mail client with everything pre-filled, so a
     submission is never silently lost.                                    */

  var form = document.getElementById('fl-contact-form');

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var url = window.flComposeMailto(form);
      if (!url) return;                     // honeypot tripped — silently drop

      window.location.href = url;

      var note = document.getElementById('fl-form-note');
      if (note) {
        note.textContent = 'Opening your email app with the message ready to send. ' +
          'If nothing happens, email info@fireandlight.co.za directly.';
      }
    });
  }
})();

/* --- Contact form -> mailto ----------------------------------------------
   Pure function so the composed URL can be verified without navigating away.
   Returns null when the honeypot field has been filled in. */
function flComposeMailto(form) {
  var hp = form.querySelector('[name="fl-website"]');
  if (hp && hp.value !== '') return null;

  var name = form.elements.name.value.trim();
  var email = form.elements.email.value.trim();
  var message = form.elements.message.value.trim();

  var body = 'Name: ' + name + '\n' + 'Email: ' + email + '\n\n' + message;

  return 'mailto:info@fireandlight.co.za' +
    '?subject=' + encodeURIComponent('Website enquiry from ' + name) +
    '&body=' + encodeURIComponent(body);
}

/* --- Sermon title tidier -------------------------------------------------
   Channel uploads are filed as "2026/08/02 The Vascular System of Faith".
   Strips the date prefix and re-cases ALL-CAPS titles, leaving mixed-case
   titles alone so speaker names survive. Exposed for future use when a
   sermon list is rendered as text rather than through the YouTube embed. */
function flTidyTitle(raw) {
  var t = String(raw || '').replace(/^\s*\d{4}[\/.-]\d{2}[\/.-]\d{2}\s*/, '').trim();

  if (t && t === t.toUpperCase()) {
    t = t.toLowerCase().replace(/(^|[\s(\-–—"'])([a-z])/g, function (m, p, c) {
      return p + c.toUpperCase();
    });
  }
  return t;
}
