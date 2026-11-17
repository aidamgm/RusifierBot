A Telegram bot for automated document processing, data classification, and document generation.
RusifierBot is a Python-based Telegram bot designed to automate routine document-related tasks. It combines data processing, rule-based classification, Excel operations, and Word document generation within a single workflow.

## Key Features

- **Telegram integration** — interact with the application through a Telegram bot.
- **Data classification** — categorize incoming data using configurable classification rules.
- **Excel processing** — process and organize spreadsheet data.
- **Document generation** — generate Word documents using predefined DOCX templates.
- **Document formatting** — handle document structure and layout during generation.
- **Modular architecture** — separate processing, classification, formatting, and document generation logic.

## Tech Stack

- Python
- Telegram Bot API
- python-dotenv
- Excel and DOCX document processing

## Project Structure

RusifierBot/
│
├── bot.py
├── main.py
├── config.py
├── processor.py
│
├── categorizer.py
├── classifier.py
├── classification_rules.py
│
├── excel.py
├── formatter.py
├── layout_engine.py
│
├── document_builder.py
├── document_builder_v2.py
├── word_builder.py
├── word_generator.py
│
├── templates/
│   ├── template.docx
│   └── template_v2.docx
│
├── requirements.txt
├── .env.example
└── .gitignore
