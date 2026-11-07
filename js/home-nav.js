/* Searchify — Smooth, Jitter-Free Sticky Navbar Scroll Controller with Hysteresis & Refresh Sync */
(function () {
    'use strict';

    function init() {
        var nav = document.getElementById('home-nav') || document.querySelector('.home-nav');
        if (!nav) return;

        var ticking = false;
        var isScrolled = false;

        // Dual thresholds create a hysteresis deadband (15px–45px) to eliminate jitter & oscillation
        var SCROLL_DOWN_THRESHOLD = 45;
        var SCROLL_UP_THRESHOLD = 15;

        // Check initial scroll or anchor position immediately without transition
        var initialY = window.pageYOffset || document.documentElement.scrollTop || 0;
        var hasHash = Boolean(window.location.hash && window.location.hash.length > 1);
        if (initialY > SCROLL_DOWN_THRESHOLD || hasHash) {
            isScrolled = true;
            nav.classList.add('is-scrolled');
        } else {
            isScrolled = false;
            nav.classList.remove('is-scrolled');
        }

        function update() {
            var scrollY = window.pageYOffset || document.documentElement.scrollTop || 0;
            var hasHash = Boolean(window.location.hash && window.location.hash.length > 1);

                if (!isScrolled && (scrollY > SCROLL_DOWN_THRESHOLD || hasHash)) {
                    isScrolled = true;
                    nav.classList.add('is-scrolled');
                } else if (isScrolled && scrollY <= SCROLL_UP_THRESHOLD && !hasHash) {
                    isScrolled = false;
                    nav.classList.remove('is-scrolled');
                }

                ticking = false;
            }

            window.addEventListener('scroll', function () {
                if (!ticking) {
                    window.requestAnimationFrame(update);
                    ticking = true;
                }
            }, { passive: true });

            // Silently enable transitions after initial paint & browser scroll restoration
            var transitionsEnabled = false;
            function enableTransitions() {
                if (transitionsEnabled) return;
                transitionsEnabled = true;
                update();
                nav.classList.remove('no-transition');
            }

            // Lift transition suppression right after initial layout cycle
            if (document.readyState === 'complete' || document.readyState === 'interactive') {
                setTimeout(enableTransitions, 40);
            } else {
                document.addEventListener('DOMContentLoaded', function () {
                    setTimeout(enableTransitions, 40);
                });
                window.addEventListener('load', enableTransitions, { once: true });
            }

            var brand = nav.querySelector('.home-brand');
            if (brand) {
                brand.addEventListener('click', function (e) {
                    var current = window.pageYOffset || document.documentElement.scrollTop || 0;
                    if (current > SCROLL_UP_THRESHOLD) {
                        e.preventDefault();
                        window.scrollTo({ top: 0, behavior: 'smooth' });
                    }
                });
            }
        }

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }
    }) ();
