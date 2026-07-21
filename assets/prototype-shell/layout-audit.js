/* WeCom Clienteling visible-layout audit · V4.0
 * Copy unchanged beside the prototype. It measures the rendered phone; it does
 * not replace visible Chrome review or user design acceptance.
 */
(() => {
  let timer = 0;

  const rect = (node) => {
    const value = node?.getBoundingClientRect();
    return value ? { left: value.left, top: value.top, right: value.right, bottom: value.bottom, width: value.width, height: value.height } : null;
  };
  const intersects = (a, b, tolerance = 1) => Boolean(a && b && a.left < b.right - tolerance && a.right > b.left + tolerance && a.top < b.bottom - tolerance && a.bottom > b.top + tolerance);
  const visible = (node) => {
    if (!node) return false;
    const style = getComputedStyle(node);
    const box = node.getBoundingClientRect();
    return style.display !== "none" && style.visibility !== "hidden" && Number(style.opacity) !== 0 && box.width > 0 && box.height > 0;
  };

  function audit() {
    const page = document.querySelector("#app > .app-page, #app > [data-native-wecom]");
    const body = page?.querySelector(":scope > .body");
    const actions = page?.querySelector(":scope > .sticky-actions, :scope > .ux-sticky-action");
    const tabbar = page?.querySelector(":scope > .tabbar");
    const screen = document.querySelector(".screen");
    const failures = [];
    const warnings = [];

    if (!page || !screen) failures.push("missing-active-page-or-screen");
    if (body && body.scrollWidth > body.clientWidth + 1) failures.push("horizontal-overflow");
    if (actions && tabbar && intersects(rect(actions), rect(tabbar))) failures.push("sticky-action-overlaps-tabbar");

    if (body && actions) {
      const previous = body.scrollTop;
      body.scrollTop = body.scrollHeight;
      const last = [...body.children].reverse().find(visible);
      if (last && intersects(rect(last), rect(actions))) failures.push("sticky-action-covers-last-content");
      body.scrollTop = previous;
    }

    const undersized = [...(page?.querySelectorAll("button, a[href], input, select, textarea") || [])]
      .filter(visible)
      .filter((node) => !node.closest(".wx-capsule"))
      .filter((node) => {
        return node.offsetWidth < 44 || node.offsetHeight < 44;
      });
    if (undersized.length) failures.push(`touch-targets-under-44px:${undersized.length}`);

    const brokenImages = [...(page?.querySelectorAll("img") || [])].filter((node) => node.complete && node.naturalWidth === 0);
    if (brokenImages.length) failures.push(`broken-images:${brokenImages.length}`);
    const assetCards = [...(page?.querySelectorAll('[data-ux-component="asset-card"]') || [])];
    const missingRealAssets = assetCards.filter((card) => !card.querySelector("img[data-asset-source]"));
    if (missingRealAssets.length) failures.push(`asset-cards-without-real-image:${missingRealAssets.length}`);

    const native = page?.matches("[data-native-wecom]") || page?.querySelector("[data-native-wecom]");
    if (native && page.querySelector(".wx-nav, .tabbar, .sticky-actions")) failures.push("native-wecom-wrapped-in-business-shell");

    const counters = [...(page?.querySelectorAll("[data-count-for]") || [])];
    for (const counter of counters) {
      const field = document.getElementById(counter.dataset.countFor);
      if (!field) { failures.push("counter-target-missing"); continue; }
      const actual = String(field.value || field.textContent || "").length;
      if (Number(counter.dataset.countValue) !== actual) failures.push("visible-counter-mismatch");
    }

    if (screen && screen.clientWidth !== 390 && document.body.classList.contains("mobile")) warnings.push("mobile-screen-not-390-css-px");
    const components = [...new Set([...(page?.querySelectorAll("[data-ux-component]") || [])].map((node) => node.dataset.uxComponent).filter(Boolean))];
    const report = {
      skillVersion: "4.0",
      pageId: page?.dataset.pageId || page?.querySelector("[data-page-id]")?.dataset.pageId || (native ? "native-wecom" : "unknown"),
      viewport: { width: screen?.clientWidth || 0, height: screen?.clientHeight || 0 },
      status: failures.length ? "fail" : "pass",
      failures,
      warnings,
      components,
      metrics: {
        bodyClientHeight: body?.clientHeight || 0,
        bodyScrollHeight: body?.scrollHeight || 0,
        actionHeight: actions?.offsetHeight || 0,
        tabbarHeight: tabbar?.offsetHeight || 0,
        visibleControls: [...(page?.querySelectorAll("button, a[href], input, select, textarea") || [])].filter(visible).length,
        brokenImages: brokenImages.length
      }
    };
    window.__wecomLayoutReport = report;
    document.documentElement.dataset.layoutAudit = report.status;
    if (document.body.classList.contains("review-mode")) {
      const controls = document.getElementById("stageControls");
      if (controls) {
        let output = controls.querySelector("[data-layout-audit-output]");
        if (!output) {
          output = document.createElement("output");
          output.dataset.layoutAuditOutput = "";
          output.className = "stage-status";
          controls.append(output);
        }
        output.textContent = report.status === "pass"
          ? `Layout PASS · ${report.pageId} · ${components.join(" / ") || "native frozen UI"}`
          : `Layout FAIL · ${failures.join(", ")}`;
      }
    }
    window.dispatchEvent(new CustomEvent("wecom-layout-audit", { detail: report }));
    return report;
  }

  function schedule() {
    clearTimeout(timer);
    timer = setTimeout(() => requestAnimationFrame(() => requestAnimationFrame(audit)), 50);
  }

  window.addEventListener("load", schedule);
  window.addEventListener("resize", schedule);
  window.WeComLayoutAudit = Object.freeze({ run: audit, schedule });
})();
