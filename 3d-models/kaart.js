/* De projectpagina schakelt deze stand in met ?kaart. */
if (new URLSearchParams(location.search).has('kaart')) {
  document.documentElement.classList.add('kaart');
}

function startKaartrotatie(canvas, onRotate) {
  const viewer = canvas.parentElement;
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let rotating = !motion.matches;
  let visible = false;
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'kaart-rotatie';

  function update() {
    button.textContent = rotating ? 'Pauzeer rotatie' : 'Laat draaien';
    onRotate(visible && rotating);
  }

  button.addEventListener('click', () => {
    rotating = !rotating;
    update();
  });
  function pause() {
    rotating = false;
    update();
  }
  canvas.addEventListener('pointerdown', pause);
  canvas.addEventListener('wheel', pause, { passive: true });
  canvas.addEventListener('keydown', pause);
  motion.addEventListener('change', () => {
    rotating = !motion.matches;
    update();
  });
  viewer.append(button);
  new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting;
    update();
  }).observe(viewer);
  update();
  return () => visible;
}
