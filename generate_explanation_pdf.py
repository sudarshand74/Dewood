from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

OUTPUT_PDF = r"c:\Users\desai\Dewood\MCQ_script_explanation.pdf"

content_title = "Concepts360 — MCQ Generator Script: Simple Explanation"

content_sections = []

content_sections.append(("Summary",
"The script automatically creates and validates multiple-choice (MCQ) questions using text retrieved from a Pinecone vector index and an Azure OpenAI chat model. For each topic it retrieves context, asks the LLM to generate questions, validates answers using the same context, and writes results to an Excel file."))

content_sections.append(("Key Pieces",
"Config/secrets (Azure + Pinecone), embedding client, Pinecone index (stores text chunks), LLM (generates + validates), and Excel output (master file)."))

content_sections.append(("Step-by-step Flow",
"1) For each topic: retrieve context from Pinecone. 2) Ask the LLM to generate N MCQs using only that context. 3) Parse the JSON output. 4) For each question, ask the LLM (with same context) to choose A/B/C/D. 5) Compare model answer with declared Correct_Option and mark Pass/Fail/Unknown. 6) Append rows to the master Excel file."))

ascii_flow = '''Start
  |
  v
[Loop: topic]
  |
  v
+-------------------------------+
| 1) search_pinecone(topic)     |
+-------------------------------+
  |
  v
+-----------------------------------------+
| 2) generate_mcq_questions(context, N)   |
+-----------------------------------------+
  |
  v
+----------------------+
| 3) extract_json(...) |
+----------------------+
  |
[Loop: each question]
  |
  v
+-----------------------------------------------+
| 4) get_model_mcq_answer_with_rag(...)         |
+-----------------------------------------------+
  |
  v
+-----------------------------------------------+
| 5) compare model answer vs Correct_Option     |
|    -> Validation Passed / Failed / Unknown    |
+-----------------------------------------------+
  |
  v
+-----------------------------+
| 6) append to Excel file     |
+-----------------------------+
  |
  v
Next topic --> End
'''

mermaid = '''flowchart TD
  A[Start] --> B[For each topic in TOPIC_MAP]
  B --> C{Search Pinecone}
  C --> D[Context (text chunks)]
  D --> E[Generate MCQs (LLM) using CONTEXT]
  E --> F[Parse LLM output → JSON questions]
  F --> G[For each question]
  G --> H[Ask LLM to pick A/B/C/D using CONTEXT]
  H --> I[Model answer]
  I --> J{Compare with Correct_Option}
  J -->|Same| K[Validation Passed]
  J -->|Different| L[Validation Failed]
  J -->|No answer| M[Validation Unknown]
  K --> N[Add Model_Answer & Status to row]
  L --> N
  M --> N
  N --> O[Append rows to Excel (MCQ_<index>_All_Topics.xlsx)]
  O --> P[Next topic]
  P --> B
  B --> Q[End] 
'''

practical_notes = (
    "Practical notes:\n"
    "- Do NOT commit API keys to public repos; use environment variables or a .env excluded by .gitignore.\n"
    "- Running the script calls paid services (Azure OpenAI, Pinecone).\n"
    "- The script relies on the LLM following strict JSON format; parsing may fail if it adds extra text.\n"
)

def build_pdf():
    doc = SimpleDocTemplate(OUTPUT_PDF, pagesize=A4, rightMargin=20*mm, leftMargin=20*mm, topMargin=20*mm, bottomMargin=20*mm)
    styles = getSampleStyleSheet()
    story = []

    title_style = styles['Title']
    normal = styles['BodyText']
    code_style = ParagraphStyle('Code', fontName='Courier', fontSize=9, leading=11)

    story.append(Paragraph(content_title, title_style))
    story.append(Spacer(1, 6))

    for header, text in content_sections:
        story.append(Paragraph(f"<b>{header}</b>", styles['Heading2']))
        story.append(Spacer(1, 2))
        story.append(Paragraph(text, normal))
        story.append(Spacer(1, 6))

    story.append(Paragraph("<b>ASCII Flowchart</b>", styles['Heading2']))
    story.append(Preformatted(ascii_flow, code_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Mermaid Diagram (source)</b>", styles['Heading2']))
    story.append(Preformatted(mermaid, code_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Practical Notes</b>", styles['Heading2']))
    story.append(Paragraph(practical_notes.replace('\n','<br/>'), normal))

    doc.build(story)

if __name__ == '__main__':
    build_pdf()
    print(f"PDF written to: {OUTPUT_PDF}")
