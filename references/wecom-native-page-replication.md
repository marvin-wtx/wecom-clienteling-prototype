# WeCom Native Page Replication

Use this when a prototype flow should reproduce a native WeCom page or native-like communication surface instead of designing a custom clienteling mini-program page.

## When To Replicate A Native Page

Replicate a native WeCom page when:
- Source material mentions 企微原生页面, 原生企微, 新建群发, 群发, broadcast, mass send, native send, or native compose.
- A clienteling task hands off to WeCom to send messages, mini-program cards, content, or batch communication.
- The reviewer needs to see the real WeCom send constraints, recipient summary, or frequency rules.
- The action is completed outside the clienteling mini-program but must return a result to the business flow.

Do not replicate a native page when:
- The action is only an internal clienteling form or confirmation page.
- The prototype can show a simple result state without needing the native WeCom interaction.
- The native behavior is unknown and not important to the current review; use a placeholder and list it as an open question.

## Surface Separation

Keep these surfaces distinct:
- **Clienteling mini-program page**: business context, customer insight, task, C360, content, appointment, dashboard.
- **WeCom native replica**: native compose/send/broadcast-like page used for communication execution.
- **Return state**: business page showing completion, failure, or pending result after the native action.

Native replicas should not inherit branded business-page decoration. They should feel plainer and closer to system/native WeCom behavior.

## New Broadcast Replica

Use this pattern for 新建群发 or task-driven batch send.

Required structure:
- Native header:
  - Left action: 取消.
  - Center title: 新建群发.
  - Right side can be empty or native-safe placeholder.
- Recipient row:
  - Label: 分别发送给.
  - Value: `N 位客户` or equivalent, with a chevron to view the customer list.
- Content section:
  - Label: 将发送以下内容.
  - Secondary action: 从素材库选择, if content selection is in scope.
  - Large white message card containing the text copy to send.
  - Attachment line at the bottom of the message card showing mini-program card, H5, image, video, or content asset if present.
- Primary send action:
  - Centered blue button: 发送.
- Native rule note:
  - Example: 每位客户每天可接收1条群发消息.

Required behavior:
- Cancel returns to the previous business page without completing the task.
- Recipient row opens customer-list preview or shows a toast/placeholder if preview is out of scope.
- Asset selection opens content library or shows a scoped placeholder.
- Send marks the communication action as submitted and returns to the business flow.
- Return state updates the originating task or flow, such as 沟通任务已完成.

## Data To Carry Into The Replica

Pass these fields from the business flow:
- Originating flow and page.
- Task or action id.
- Recipient count.
- Recipient eligibility and exclusions.
- Message copy.
- Attachment type and title.
- Frequency or compliance note.
- Completion result to write back.

## Common Native Replica Candidates

Use only if relevant:
- 新建群发 / broadcast compose.
- Customer recipient list preview.
- Send mini-program card confirmation.
- Native chat handoff placeholder.
- Send result / failure / frequency-limit state.

## QA Checks

- The native page is visually and structurally distinct from clienteling business pages.
- The native page should look like a system/native compose page: pale gray background, plain header, white recipient row, large white message editor, attachment row, centered blue send button, and bottom frequency note.
- Required labels and actions match the native behavior the prototype is trying to emulate.
- Recipient count and content payload are carried from the business page.
- Frequency/compliance limits are visible if they affect business decisions.
- Send/cancel paths return to the correct business state.
- Native replica pages hide clienteling bottom navigation and unrelated app tools.
