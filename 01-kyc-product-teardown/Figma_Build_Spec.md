# Figma Build Spec

This package includes a working HTML prototype, not a native `.fig` file or a live Figma document. Use these instructions to make the Figma design editable and share a Figma prototype URL.

## File and page setup
- File name: `FlexiPay — KYC Redesign (Portfolio Concept)`
- Pages: `00 Cover`, `01 Current-state hypothesis`, `02 Redesigned flow`, `03 Components`, `04 Prototype notes`
- Create 390 × 844 mobile frames first; add 1440 × 900 desktop frames if time allows.

## Design tokens
- Ink `#17263C`; primary `#2C5CFF`; background `#F5F7FB`; surface `#FFFFFF`; muted `#64748B`; border `#D9E0EA`; success `#16794B`; error `#B42318`.
- 8 px spacing scale; 16 px body; 24–32 px headings; 12 px radius for cards and inputs; visible 2 px focus ring.
- Use auto layout for cards, form fields, stepper and bottom navigation. Use real labels, not placeholder-only field names.

## Frames to create
1. **Welcome & eligibility:** purpose, requirement checklist, time expectation labelled as an estimate, primary CTA.
2. **Personal details:** name/date example uses visibly fake sample data; required labels and inline error state.
3. **Document upload:** accepted types/size before picker; selected-file state, unsupported-file error, retry state, help link.
4. **Review & confirmation:** summary, edit links, submit confirmation and next-step explanation.
5. **Old-flow comparison:** show the same actions split into six smaller screens to make the design rationale visible; label it as a conceptual baseline, not a captured production interface.

## Prototype wiring
- Welcome → Details → Upload → Review → Confirmation.
- Back links preserve data; error variant links back to the upload state.
- Connect the progress stepper only to completed/active states; do not imply a real KYC decision.
- Add annotations for interaction assumptions and open questions.

## Figma checks
- Test with keyboard/focus order; do not rely on colour alone for errors.
- Verify minimum readable type, touch targets and contrast.
- Share a view-only prototype link after testing; add the actual link to `README.md`.
