/* particlesJS.load(@dom-id, @path-json, @callback (optional)); */
particlesJS.load('particles-js', '/assets/particles.json');

// var count_particles, stats, update;
// stats = new Stats; stats.setMode(0);
// stats.domElement.style.position = 'absolute';
// stats.domElement.style.left = '0px';
// stats.domElement.style.top = '300px';
// document.body.appendChild(stats.domElement);
// count_particles = document.querySelector('.js-count-particles');
// update = function() {
//   stats.begin(); stats.end();
//   if (window.pJSDom[0].pJS.particles && window.pJSDom[0].pJS.particles.array) {
//     count_particles.innerText = window.pJSDom[0].pJS.particles.array.length;
//   }
//   requestAnimationFrame(update);
// };
// requestAnimationFrame(update);

// window.pJSDom[0].pJS.particles.move.direction = 'top';
// window.pJSDom[0].pJS.particles.move.direction = 'bottom';
// window.pJSDom[0].pJS.particles.move.out_mode = 'bounce';

let lastScrollTop = window.scrollY;
let ticking = false;
var direction = "top";
var default_direction = "top";
var velocity = 4;
window.addEventListener('DOMContentLoaded', function() {
  window.addEventListener('scroll', function(e) {
    if (ticking == false) {
      if (typeof window.pJSDom[0] !== 'undefined') {
        var localpJS = window.pJSDom[0].pJS;
        var st = window.pageYOffset || document.documentElement.scrollTop; // Credits: "https://github.com/qeremy/so/blob/master/so.dom.js#L426"
        velocity = 12
        if (st > lastScrollTop){
          direction = 'top';
        } else {
          direction = 'bottom';
        }
        lastScrollTop = st <= 0 ? 0 : st; // For Mobile or negative scrolling
        window.requestAnimationFrame(function() {
          setTimeout(function(){
            ticking = false;
            lastDirection = direction;
            localpJS.fn.updateParticlesDirection(default_direction);
          }, 1000/60);
          localpJS.fn.particlesScroll(direction, velocity);
        });
        ticking = true;
      };
    }
  });
}, false);

