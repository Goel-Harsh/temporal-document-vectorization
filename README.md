# Temporal Document Processing

This project automates the processing of documents from a given URL using Temporal.io. It consists of a workflow that fetches a document, parses its content, generates embeddings, and stores the data in a Milvus vector database.

## Project Structure

```
temporal_doc_processing
├── src
│   ├── activities
│   │   ├── fetch_document.py       # Activity to fetch document content from a URL
│   │   ├── parse_document.py       # Activity to parse document content into chunks
│   │   ├── generate_embeddings.py   # Activity to generate embeddings for text chunks
│   │   └── store_data.py           # Activity to store text and embeddings in Milvus
│   ├── workflows
│   │   └── document_workflow.py     # Main workflow orchestrating the activities
│   ├── workers
│   │   └── worker.py                # Temporal worker to execute activities
│   └── utils
│       └── __init__.py              # Utility functions and constants
├── requirements.txt                  # Project dependencies
└── README.md                         # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd temporal_doc_processing
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Set your PYTHONPATH (required for imports):**
   On Windows (Command Prompt):
   ```
   set PYTHONPATH=src
   ```
   On macOS/Linux:
   ```
   export PYTHONPATH=src
   ```

4. **Start the Temporal server (required):**
   If you have Docker installed, run:
   ```
   curl -O https://raw.githubusercontent.com/temporalio/docker-compose/main/docker-compose.yml
   docker-compose up
   ```
   Or use your own docker-compose file if provided.

5. **Set up Milvus:**
   Use Milvus Standalone Docker Compose. You can start Milvus locally by running:
   ```
   curl -O https://raw.githubusercontent.com/milvus-io/milvus-operator/main/config/docker-compose/docker-compose.yml
   docker-compose up
   ```
   This will start Milvus in standalone mode on your machine.

6. **Run the workflow starter script:**
   If you have a `run_worker.py` or similar script to start workflows, run:
   ```
   python src/workers/run_worker.py
   ```

7. **Run the Temporal worker:**
   ```
   python src/workers/worker.py
   ```

8. **Start the workflow:**
   You can start the workflow by invoking it with the required parameters (File ID and File URL) using the Temporal SDK.
   ```

7. **Start the workflow:**
   You can start the workflow by invoking it with the required parameters (File ID, File URL, and File Type) using the Temporal SDK.
   For example, if you have a CLI or script, you may be prompted for:
   - File ID (a unique identifier for your document)
   - File URL (the direct download link)
   - File Type (e.g., `pdf`, `docx`, `xlsx`)

   Example:
   ```sh
   python src/workers/worker.py
   ```
   Then follow the prompts for file ID, URL, and type.

## Usage Example

To process a document, call the `document_workflow` with the necessary input parameters. The workflow will handle fetching the document, parsing it, generating embeddings, and storing the results in Milvus.

**Note:**
- For Google Drive or similar links, you must specify the file type manually (e.g., `pdf`, `docx`).
- Ensure your Milvus and Temporal servers are running before starting the workflow.

## Activities Overview

- **Fetch Document:** Retrieves the content of a document from a specified URL.
- **Parse Document:** Uses the Unstructured.io library to break down the document into meaningful chunks.
- **Generate Embeddings:** Utilizes the OpenAI SDK to create vector embeddings for each text chunk.
- **Store Data:** Saves the original text and its corresponding embedding vector into a Milvus vector database.
