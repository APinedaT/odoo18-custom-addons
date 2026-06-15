/* Pineda theme — render Lucide line icons used in the homepage sections.
 * Lucide replaces every <i data-lucide="name"></i> with an inline SVG.
 * We re-run on load and whenever Odoo injects/edits DOM (snippets, editor).
 */
(function () {
    "use strict";

    function renderIcons() {
        if (window.lucide && typeof window.lucide.createIcons === "function") {
            window.lucide.createIcons();
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", renderIcons);
    } else {
        renderIcons();
    }
    // `load` fires after the Lucide CDN script has executed, guaranteeing
    // window.lucide is available even if this script ran first.
    window.addEventListener("load", renderIcons);

    // Re-render after dynamic DOM changes (website editor, lazy sections).
    if (window.MutationObserver) {
        let scheduled = false;
        const observer = new MutationObserver(function () {
            if (scheduled) {
                return;
            }
            scheduled = true;
            window.requestAnimationFrame(function () {
                scheduled = false;
                renderIcons();
            });
        });
        observer.observe(document.documentElement, { childList: true, subtree: true });
    }
})();
