function nativeBroadcastText(value, fallback=''){return String(value==null?fallback:value).replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]))}
function nativeBroadcastTask(){return typeof window.getNativeBroadcastContext==='function'?window.getNativeBroadcastContext():(typeof currentTask==='function'?currentTask():null)}
function exitNativeBroadcast(){if(typeof window.closeNativeBroadcast==='function'){window.closeNativeBroadcast();return}if(typeof goBack==='function')goBack()}
function nativeBroadcastDraft(task){
 const draft=typeof window.getNativeBroadcastDraft==='function'?window.getNativeBroadcastDraft(task):null;
 if(!draft||typeof draft!=='object')return {recipientCount:0,message:'',material:null,missing:true};
 return {recipientCount:Number(draft.recipientCount)||0,message:String(draft.message||''),material:draft.material&&typeof draft.material==='object'?draft.material:null,missing:false};
}
function nativeWecomAttachment(draft){
 const material=draft.material;
 if(!material)return `<div class="native-add" aria-label="添加素材">+</div>`;
 if(material.kind==='image'){
   const preview=material.previewSrc?`<img src="${nativeBroadcastText(material.previewSrc)}" alt="${nativeBroadcastText(material.alt||material.title||'图片素材')}">`:`<span class="native-image-placeholder" aria-label="${nativeBroadcastText(material.alt||material.title||'图片素材')}" role="img"></span>`;
   return `<div class="native-image-thumb">${preview}</div><div class="native-add" aria-label="添加素材">+</div>`;
 }
 if(material.kind==='mini-program'){
   const mark=nativeBroadcastText(material.mark||material.programName?.slice(0,1)||'小');
   const name=nativeBroadcastText(material.programName||material.title||'小程序卡片');
   const logo=material.logoSrc?`<img class="native-mini-logo" src="${nativeBroadcastText(material.logoSrc)}" alt="">`:`<span class="native-mini-mark" aria-hidden="true">${mark}</span>`;
   return `<div class="native-mini-card">${logo}<span class="native-mini-title">${name}</span><svg class="native-link-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7.1.1l2-2a5 5 0 0 0-7.1-7.1l-1.1 1.1"/><path d="M14 11a5 5 0 0 0-7.1-.1l-2 2a5 5 0 0 0 7.1 7.1l1.1-1.1"/></svg></div><div class="native-add" aria-label="添加素材">+</div>`;
 }
 return `<div class="native-add" aria-label="添加素材">+</div>`;
}
function chooseNativeBroadcastMaterial(task){
 if(typeof window.openNativeBroadcastMaterialPicker==='function'){window.openNativeBroadcastMaterialPicker(task);return}
 if(typeof window.toast==='function')window.toast('请从素材库选择');
}
function inspectNativeBroadcastRecipients(draft){
 if(typeof window.openNativeBroadcastRecipientList==='function'){window.openNativeBroadcastRecipientList();return}
 if(typeof window.toast==='function')window.toast(draft.recipientCount?`已选择 ${draft.recipientCount} 位客户`:'尚未选择客户');
}
function finishNativeTask(){
 const task=nativeBroadcastTask(),draft=nativeBroadcastDraft(task);
 if(typeof window.commitNativeBroadcast==='function'){window.commitNativeBroadcast({task,draft});return}
 if(typeof window.toast==='function')window.toast('群发草稿尚未绑定完成回调');
}
function renderWecomExecute(){
 const task=nativeBroadcastTask(),draft=nativeBroadcastDraft(task),attachment=nativeWecomAttachment(draft),message=draft.message||'请选择发送内容',count=draft.recipientCount||'—';
 return `<div class="native-exec"><div class="native-head"><button onclick="exitNativeBroadcast()">取消</button><div class="native-head-title">新建群发</div><span></span></div><div class="native-content"><button class="native-recipient" onclick="inspectNativeBroadcastRecipients(nativeBroadcastDraft(nativeBroadcastTask()))"><span>分别发送给</span><span>${count} 位客户 ›</span></button><div class="native-label-row"><span>将发送以下内容</span><button class="native-link" onclick="chooseNativeBroadcastMaterial(nativeBroadcastTask())">从素材库选择</button></div><div class="native-message-card"><div class="native-message-text${draft.missing?' native-message-missing':''}">${nativeBroadcastText(message)}</div><div class="native-attachment-line">${attachment}</div></div><button class="native-primary" ${draft.missing?'disabled':''} onclick="finishNativeTask()">发送</button></div><div class="native-note">每位客户每天可接收1条群发消息</div></div>`
}
