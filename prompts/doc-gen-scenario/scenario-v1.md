# You will be ingesting the user’s information and following the below instruction to output an instruction file for another LLM to generate the legal document specified.


## Stage 1: Research from <data> and analyse legal nuances and details that this particular document will need to include when generating. 


The following are some * NON-EXHAUSTIVE * examples:
> “What specific statutes must the document adhere to”
> “Whether specific clauses should be grounded on statutes explicitly.”
> “Whether the specific clauses might limited or rendered void/ineffective by law”
> “Other areas of law the document may touch upon”
> “Whether specific terms/wording/object should follow the statutory definition”
> “Whether there are any parts/sections/clauses/terms that must be defined/described in greater details.”


## Stage 2: Use the document summary and your research to write a Scenario Description (the “SD”) and a Document Generation Memo (the “DGM”) that is COMPLETE, STRUCTURED, and VERIFIED.


The Scenario Description outlines the user’s expectations, detailing everything that they have set out to achieve. The Scenario Description should act as a preliminary guideline, instructing the LLM to generate the legal document in accordance with a list of terms, conditions, specifications, etc as per the user’s request. They must at least include, and not be limited to the following:
- Document Name
- Parties Involved
- Roles & Responsibilities
- Ownership / Financial Terms
- Key Dates & Timeline
- Document Requirements
- Constraints / Special Conditions
- Explicit Assumptions Confirmed by User
- Other Extracted Details
- Missing Information


The Document Generation Memo is a list of actionable and practical instructions/statements/requirements that helps to generate more comprehensive, specific, precise and more legally grounded legal documents. The DGM may include but is not limited to: 
- What specific clauses must the document include; 
- What specific clauses must be “pursuant to” what law);
- In what way specific clauses must be worded to avoid attracting liability;
- In what way specific clauses must be worded to avoid being limited/rendered void/rendered ineffective;
- What specific term should follow what statutory definition;
- Which of the user’s required terms/conditions/specifications should be flagged in generation due to illegality, errors in logic, and contradictions.


YOU MUST FOLLOW THIS LIST OF REQUIREMENTS IN GENERATING THE SD AND DGM:
- Must be EXTREMELY detailed and exhaustive
- Must NOT summarize or compress
- Must include EVERY piece of user-provided information
- Must preserve original meaning exactly
- Must NOT contain any case citation
- Must NOT use IRAC to analyse the query
- "Missing Information" MUST NOT be empty if anything is unclear
- DO NOT guess or infer missing values
- DO NOT merge or simplify user inputs
- Repeat details if necessary to avoid information loss


## Stage 3: Final MANDATORY Validation:


Before outputting:
- Re-read the entire conversation
- Ensure ZERO missing details
- Ensure NOTHING is generalized or shortened


## Stage 4: Output in this example json format


EXAMPLE STRUCTURE (use exact section headers):
{
 "Scenario Description": {
   "Document Name":
   "Parties Involved":
   "Roles & Responsibilities":
   "Ownership / Financial Terms":
   "Key Dates & Timeline":
   "Document Requirements":
   "Constraints / Special Conditions":
   "Explicit Assumptions Confirmed by User":
   "Other Extracted Details":
   "Missing Information":
 }
 "Document Generation Memo": {
 }
}
