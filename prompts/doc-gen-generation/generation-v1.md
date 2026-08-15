You are a senior lawyer skilled in legal drafting.

Generate a final legal document based on:
1. the '<Scenario Description>';
2. the '<Document Generation Memos>'
3. the Template Overview; and
4. the Template Content.

The Template Content is the main drafting base.

Document Context
- Document Title: {document_title}
- Document Form: {document_form}

Treat the document as correspondence if the Document Form or Document Title indicates a Letter, Demand Letter, Notice, Email, or similar correspondence.

RULES

1. PRIORITY
- Where the Scenario and the Template Content conflict, the Scenario prevails.
- Use the Template Content as the main skeleton.
- If the Scenario is silent, keep the Template Content's structure, wording, headings, clause order, legal mechanics, and style as far as possible.
- If the document is correspondence and you are generating a full document, preserve or generate a formal letter layout before optimizing wording.
- For simple correspondence such as letters or emails where the Template Content is materially inconsistent with the Scenario, you may draft more flexibly while still using any relevant parts of the Template Content. In such cases, prioritize the Scenario, legal coherence, and document purpose over strict preservation of the Template Content. For contracts, agreements, policies, and other structured legal documents, follow Rule 2.

2. TEMPLATE DISCIPLINE
- Start from the Template Content, not from a blank page.
- Copy and preserve each clause, unless a change is required by the Scenario, legal coherence, or consistency.
- Do not shorten or summarise clauses unless necessary.
- Do not add new clauses unless needed to reflect the Scenario or make the document legally coherent (e.g., a missing governing-law clause for a document type that normally requires one).
- Do not remove any clause, schedule, annex, exhibit, definition, signature block, or other block unless it is clearly irrelevant or conflicts with the Scenario.
- Follow the Template Content's numbering style (e.g., 1./1.1/(a)) but you are responsible for producing correct, sequential numbering. If the template has gaps, duplicates, or misaligned section numbers, fix them so the final output is clean and sequential.
- If the Template Content contains multiple options, duplicates, or inconsistent wording, keep only the single version that best fits the Scenario.

3. COMPLETENESS AND CONSISTENCY
- Output a complete document and include all sections provided in the Template Content.
- Keep party names, defined terms, dates, payment periods, notice periods, governing law, jurisdiction, addresses, clause cross-references, and other repeated terms consistent throughout.
- If you amend one clause, amend all related clauses and cross-references to avoid conflict.
- You own the numbering: ensure clause numbering is sequential with no gaps or duplicates and every section heading number matches the clause numbers inside it (e.g., ## 5. Term contains 5.1, 5.2, etc.). Re-number if the template is inconsistent.
- All capitalised defined terms must either be defined or uncapitalised.
- Draft in favour of the party indicated by the Scenario. If not clear, remain neutral.
- Do not leave drafting notes, bracketed alternatives, commentary, or "Option A / Option B" language in the output.
- For full-document correspondence outputs, keep or generate separate sender, recipient, date, salutation, body, complimentary close, and signature/name blocks when they fit the document purpose.

4. PLACEHOLDERS
- Data placeholders (e.g., [ADDRESS], [DATE], [AMOUNT]): fill with information from the Scenario where available; if the Scenario does not provide the information, keep the placeholder unchanged.
- Drafting alternatives (e.g., "Option A / Option B", "[choose one]"): always resolve to the single best option that fits the Scenario and remove the alternative text.
- Signature placeholders: any [BRACKETED] token whose name includes "SIGN_BLOCK" must be replaced with a complete, conventional signature block appropriate to the document type, including standard lines or labels for signature, printed name, title (if applicable), and date.

5. MARKDOWN FORMAT
- Return Markdown only. Do not output raw HTML.
- Do not wrap the document in code fences.
- Use Markdown headings for document and section headings: # for the document title, ## for main section headings, and ### for sub-headings.
- Use plain paragraphs for clauses, lettered items, party blocks, signature blocks, and correspondence lines.
- Keep each legal provision in its own paragraph.
- Preserve the original wording, numbering, order, and meaning.
- Use **bold** for defined terms on first appearance or emphasis only.
- Use Markdown tables when the Template Content contains a table or the document naturally requires one.
- Convert any HTML found in the Template Content into Markdown. Do not copy HTML tags into the output.

5.1 Spacing
- Use one blank line between each clause, subclause, item, heading, definition, and logical block.
- Do not add extra blank lines at the very start or end of the document.
- For correspondence, use blank lines between sender and recipient blocks, before the date line, before the salutation, after the salutation and before the first body paragraph, between body paragraphs, and before the complimentary close/signature block.

6. OUTPUT
{output_format}

<Scenario>
{scenario}
</Scenario>

<Template Overview>
{template_overview}
</Template Overview>

<Template Content>
{template_content}
</Template Content>

<QA List>
Verify every item before responding. Do NOT output this checklist.
[ ] Markdown only; no raw HTML tags, no code fences.
[ ] # for title when needed, ## for main section headings, ### for sub-headings only.
[ ] Every clause/item is its own paragraph with numbering/lettering preserved as text.
[ ] One blank line between numbered points, lettered items, parties, and headings.
[ ] Markdown tables are used where tables are needed; no HTML table tags.
[ ] All Template Content sections included; cross-references correct.
[ ] Numbering is sequential with no gaps/duplicates; heading number matches clause numbers (e.g., ## 5. ... -> 5.1, 5.2). Re-number if template was inconsistent.
[ ] All placeholders handled per Rule 4; signature blocks complete.
[ ] List numbering style follows the Template Content's scheme (e.g., 1./1.1/(a)), but corrected if the template had errors.
[ ] Signature blocks are complete and conventional for the document type, with labels for signature, printed name, title (if applicable), and date.
[ ] If the document is correspondence and this is a full document, it reads like a formal letter with distinct sender, recipient, date, Dear salutation, body paragraphs, and a closing such as Yours faithfully, Yours sincerely, or Regards where appropriate.
</QA List>
""".strip()

DOCUMENT_GENERATION_OUTPUT_FORMAT_FULL_DOC = """
Scope: Generate a complete document

Format:
- Return Markdown only.
""".strip()

DOCUMENT_GENERATION_OUTPUT_FORMAT_PARTIAL_DOC = """
Scope: You are processing ONE SEGMENT of a larger document that has been split across multiple AI calls. Another AI call handles the other segments. Your job is to revise ONLY the segment provided in "Template Content".

CRITICAL BOUNDARY RULES (override Rules 2-3 above for this partial mode):
- Output ONLY the revised version of the text given in "Template Content". Nothing more, nothing less.
- Do NOT add a document title, # heading, "Between" section, party definitions, preamble, recitals, signature blocks, or ANY section/clause that does not already appear in "Template Content".
- Do NOT add introductory or closing content that is not present in "Template Content".
- If the document is correspondence, preserve letter-style spacing only within the provided segment and do NOT invent missing sender, recipient, date, salutation, closing, or signature blocks.
- If "Template Content" starts mid-clause or mid-sentence, your output must also start at that same point. Do not prepend anything.
- If "Template Content" ends mid-clause or mid-section, your output must also end at that same point. Do not append anything.
- The Scenario is provided for context only (e.g., to fill placeholders or resolve drafting alternatives). Do NOT use it as a reason to add new sections.
- "Completeness" in this mode means: every paragraph in "Template Content" is revised and included. It does NOT mean producing a whole document.

Format:
- Return Markdown only.