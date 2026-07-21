/*
 * WeCom Clienteling protected shell runtime · V4.0
 *
 * Copy this file unchanged beside a delivered prototype's index.html.
 * Project code belongs in the page/data layer; this runtime owns the review
 * stage, viewport fitting, reviewer controls, and shell event bridge.
 */
(() => {
  const VERSION = "4.0";
  const PHONE_WIDTH = 390;
  const PHONE_HEIGHT = 844;
  const actionHandlers = new Map();
  const kitReviewConfig = {
    labels: { role: "Role", mode: "Mode", entry: "Entry", browse: "Free browse", journey: "Journey demo", chooseJourney: "Configure journeys", configureRole: "Configure roles", reset: "Reset" },
    roles: [], activeRole: "", mode: "browse", journeys: [], activeJourney: "", entries: []
  };
  let reviewConfig = { ...kitReviewConfig };

  function icon(name) {
    const paths = {
      grid: '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
      users: '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
      list: '<path d="M8 6h13M8 12h13M8 18h13"/><path d="M3 6h.01M3 12h.01M3 18h.01"/>',
      calendar: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/>',
      send: '<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
      check: '<path d="m5 12 4 4L19 6"/>'
    };
    return `<svg viewBox="0 0 24 24" aria-hidden="true">${paths[name] || paths.grid}</svg>`;
  }

  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
  }

  function wecomCapsule() {
    return '<div class="wx-capsule" aria-label="WeCom controls"><button class="wx-capsule-dot" type="button" aria-label="More"></button><span class="wx-capsule-line"></span><button class="wx-capsule-circle" type="button" aria-label="Close"></button></div>';
  }

  function optionMarkup(items, selected, fallback) {
    if (!items.length) return `<option value="">${escapeHtml(fallback)}</option>`;
    return items.map((item) => `<option value="${escapeHtml(item.id)}"${item.id === selected ? " selected" : ""}>${escapeHtml(item.label)}</option>`).join("");
  }

  function reviewControls(config) {
    const labels = { ...kitReviewConfig.labels, ...(config.labels || {}) };
    const roles = Array.isArray(config.roles) ? config.roles : [];
    const journeys = Array.isArray(config.journeys) ? config.journeys : [];
    const entries = Array.isArray(config.entries) ? config.entries : [];
    const mode = config.mode === "journey" ? "journey" : "browse";
    return `
      <div class="control-group"><span class="control-label">${escapeHtml(labels.role)}</span><select class="select" data-review-control="role" aria-label="${escapeHtml(labels.role)}"${roles.length < 2 || mode === "journey" ? " disabled" : ""}>${optionMarkup(roles, config.activeRole, labels.configureRole)}</select></div>
      <div class="control-group"><button class="stage-btn" type="button" data-review-control="mode">${escapeHtml(labels.mode)}: ${escapeHtml(mode === "journey" ? labels.journey : labels.browse)}</button><select class="select" data-review-control="journey" aria-label="${escapeHtml(labels.journey)}"${mode !== "journey" || !journeys.length ? " disabled" : ""}>${optionMarkup(journeys, config.activeJourney, labels.chooseJourney)}</select><button class="stage-btn" type="button" data-review-control="journey-reset"${mode !== "journey" || !config.activeJourney ? " disabled" : ""}>${escapeHtml(labels.reset)}</button></div>
      ${entries.length ? `<div class="control-group review-entry"><span class="control-label">${escapeHtml(labels.entry)}</span>${entries.map((entry) => `<button class="stage-btn" type="button" data-review-entry="${escapeHtml(entry.id)}">${icon(entry.icon || "grid")}${escapeHtml(entry.label)}</button>`).join("")}</div>` : ""}
      <div class="control-group"><button class="stage-btn" type="button" data-stage-action="fit">Fit</button></div>`;
  }

  function reviewModeEnabled() {
    return new URLSearchParams(window.location.search).get("review") === "1";
  }

  function applyReviewMode() {
    const enabled = reviewModeEnabled();
    document.body.classList.toggle("review-mode", enabled);
    if (!enabled) {
      const target = document.getElementById("stageControls");
      if (target) target.innerHTML = "";
    }
    return enabled;
  }

  function mountReviewControls(config = kitReviewConfig) {
    reviewConfig = { ...kitReviewConfig, ...config, labels: { ...kitReviewConfig.labels, ...(config.labels || {}) } };
    if (!applyReviewMode()) { requestFit(); return; }
    const target = document.getElementById("stageControls");
    if (target) target.innerHTML = reviewControls(reviewConfig);
    requestFit();
  }

  function emitReviewChange(type, value = "") {
    window.dispatchEvent(new CustomEvent("wecom-review-change", { detail: { type, value, config: reviewConfig } }));
  }

  function tabbar(items = [], activeTab = "") {
    if (!items.length) return "";
    return `<nav class="tabbar" style="--tab-count:${items.length}" aria-label="Primary navigation">${items.map((item) => `<button class="tab${item.id === activeTab ? " active" : ""}${item.center ? " center" : ""}" type="button" data-route="${escapeHtml(item.id)}"><span class="tab-ic">${icon(item.icon || "grid")}</span><span>${escapeHtml(item.label)}</span></button>`).join("")}</nav>`;
  }

  function appShell({ title, back = false, body = "", tabs = [], activeTab = "", actions = "" }) {
    const hasTabbar = tabs.length > 0;
    return `<article class="app-page${hasTabbar ? " has-tabbar" : ""}${actions ? " has-actions" : ""}"><header class="wx-nav"><button class="wx-nav-left${back ? "" : " placeholder"}" type="button" data-back aria-label="Back"></button><div class="wx-nav-title">${escapeHtml(title)}</div>${wecomCapsule()}</header><div class="body${hasTabbar ? "" : " no-tab"}">${body}</div>${actions ? `<footer class="sticky-actions">${actions}</footer>` : ""}${tabbar(tabs, activeTab)}</article>`;
  }

  function detectViewportMode() {
    const requested = new URLSearchParams(window.location.search).get("view");
    if (requested === "mobile") return "mobile";
    if (requested === "desktop") return "desktop";
    return window.matchMedia("(max-width: 767px)").matches || /iPhone|iPad|iPod|Android|Mobile|HarmonyOS|WeChat/i.test(navigator.userAgent) ? "mobile" : "desktop";
  }

  function fitDesktopPhone() {
    const mobile = detectViewportMode() === "mobile";
    document.body.classList.toggle("mobile", mobile);
    const wrap = document.querySelector(".phone-wrap");
    if (!wrap) return;
    if (mobile) {
      document.documentElement.style.setProperty("--desktop-phone-scale", "1");
      wrap.style.width = "100vw";
      wrap.style.height = "100dvh";
      return;
    }
    const stage = document.querySelector(".stage");
    const header = document.querySelector(".stage-header");
    const controls = document.querySelector(".stage-controls");
    const styles = stage ? getComputedStyle(stage) : null;
    const padding = styles ? parseFloat(styles.paddingTop) + parseFloat(styles.paddingBottom) : 32;
    const gap = styles ? parseFloat(styles.rowGap || styles.gap) * 2 : 20;
    const usedHeight = (header?.offsetHeight || 0) + (controls?.offsetHeight || 0) + padding + gap;
    const availableHeight = Math.max(180, window.innerHeight - usedHeight);
    const availableWidth = Math.max(280, Math.min(920, window.innerWidth - 32));
    const scale = Math.max(.25, Math.min(1, availableHeight / PHONE_HEIGHT, availableWidth / PHONE_WIDTH));
    document.documentElement.style.setProperty("--desktop-phone-scale", String(scale));
    wrap.style.width = `${PHONE_WIDTH * scale}px`;
    wrap.style.height = `${PHONE_HEIGHT * scale}px`;
  }

  function requestFit() { requestAnimationFrame(() => requestAnimationFrame(fitDesktopPhone)); }

  function registerAction(id, handler) {
    if (typeof id !== "string" || typeof handler !== "function") throw new Error("WeComShell.registerAction requires an id and function.");
    actionHandlers.set(id, handler);
  }

  function afterRender() { requestFit(); }

  document.addEventListener("click", (event) => {
    const stageAction = event.target.closest("[data-stage-action]")?.dataset.stageAction;
    if (stageAction === "fit") { fitDesktopPhone(); return; }
    const reviewControl = event.target.closest("[data-review-control]")?.dataset.reviewControl;
    if (reviewControl === "mode") { reviewConfig = { ...reviewConfig, mode: reviewConfig.mode === "journey" ? "browse" : "journey" }; if (reviewConfig.mode === "browse") reviewConfig.activeJourney = ""; mountReviewControls(reviewConfig); emitReviewChange("mode", reviewConfig.mode); return; }
    if (reviewControl === "journey-reset") { emitReviewChange("journey-reset", reviewConfig.activeJourney); return; }
    const entry = event.target.closest("[data-review-entry]")?.dataset.reviewEntry;
    if (entry) { emitReviewChange("entry", entry); return; }
    const action = event.target.closest("[data-operating-action]")?.dataset.operatingAction;
    if (action) {
      const handler = actionHandlers.get(action);
      if (handler) handler({ event, element: event.target.closest("[data-operating-action]"), id: action });
      window.dispatchEvent(new CustomEvent("wecom-operating-action", { detail: { id: action, handled: Boolean(handler) } }));
    }
  });

  document.addEventListener("change", (event) => {
    const control = event.target.dataset.reviewControl;
    if (control === "role") { reviewConfig = { ...reviewConfig, activeRole: event.target.value }; emitReviewChange("role", event.target.value); }
    if (control === "journey") { reviewConfig = { ...reviewConfig, activeJourney: event.target.value }; emitReviewChange("journey", event.target.value); }
  });
  window.addEventListener("resize", requestFit);
  applyReviewMode();

  window.WeComShell = Object.freeze({ VERSION, icon, escapeHtml, wecomCapsule, reviewModeEnabled, mountReviewControls, appShell, fitDesktopPhone, requestFit, afterRender, registerAction });
})();
