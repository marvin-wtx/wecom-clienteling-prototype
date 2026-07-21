# Prototype Presentation Spec · V4.0

- Build the confirmed mobile IA before any presentation shell.
- Obtain explicit user acceptance of two to four representative branded screens before styling the complete product or adding the review shell.
- `?view=desktop` shows only the accepted phone product; it contains no version, prototype, review, QA, or Journey language.
- `?review=1&view=desktop` may show compact controls outside the phone for roles and Journeys that already work in mobile.
- Mobile fills the visible viewport; long pages scroll inside their body; bottom navigation and sticky actions never obscure content.
- Native group send is an independent full-screen page without parent navigation or task title.
- A build with one selected Journey may not advertise multiple Journeys; a build with one role may not advertise role switching.

Visible Chrome must check every selected page and the complete primary Journey against the final build hash.
