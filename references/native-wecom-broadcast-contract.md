# Native WeCom Broadcast Contract — V4.0

`assets/native-wecom-broadcast-generic/` freezes the native **新建群发** page structure and visual treatments. It is not a static content card and contains no project brand, customer, commercial, image, or copy data.

Keep the marked CSS/JS blocks in `prototype/index.html` exactly equal to the frozen assets. Bind project data through these project-layer callbacks outside the frozen block:

```js
window.getNativeBroadcastDraft = (task) => ({
  recipientCount: selectedRecipientIds.length,
  message: broadcastDraft.message,
  material: broadcastDraft.material
});
window.getNativeBroadcastContext = () => currentTask;
window.closeNativeBroadcast = () => { /* return to the preceding project page */ };
window.openNativeBroadcastMaterialPicker = (task) => { /* choose material, update broadcastDraft, render */ };
window.openNativeBroadcastRecipientList = () => { /* show selected recipients */ };
window.commitNativeBroadcast = ({ task, draft }) => { /* record result, return to source task */ };
```

`material` is either:

```js
{ kind: 'image', previewSrc: './assets/selected.jpg', alt: '活动图片' }
{ kind: 'mini-program', logoSrc: './assets/program-logo.svg', programName: '品牌会员服务', mark: '品' }
```

Mount `renderWecomExecute()` directly into `#app`; it is the complete native page. Do not pass it to `WeComShell.appShell()`, `WeComShell.nativeSendFrame()`, a page wrapper containing `.wx-nav`, or any frame displaying the originating task title. `nativeSendFrame` is not part of the V4.0 runtime API. Its frozen header reserves `var(--status-h)` before the 74px native navigation row; never remove that safe area or overlap 9:41/5G. The frozen page must render an image as a thumbnail plus add affordance, and a mini-program as mark/logo, program name, link indicator and add affordance. “从素材库选择” must call the project picker and re-render the same draft. Never substitute fixed sample copy, a generic fixed mini-card, or a second mini-program header.

Project code may supply only the draft recipient count, message, image/mini-program material, and route callbacks needed to cancel, pick material, inspect recipients, and commit the send. It must not inject a native title, task title, parent navigation, explanatory banner, CRM source, or business rule.

In a visible browser verify: previous task/content selection → selected recipients/message/material shown in **新建群发** → picker changes the material → cancel returns → send records a result and returns.
