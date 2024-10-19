# Blender Manual RAG-Tool

This project is a Retrieval-Augmented Generation (RAG) tool designed to assist with the Blender manual. It integrates with various custom OpenAI endpoints to provide detailed and contextually relevant information about Blender's features, workflows, and best practices.

## Prerequisites:

Before you start, ensure you have the following installed:

- go-task (https://github.com/go-task/task)
- uv (https://github.com/astral-sh/uv).
- custom openai endpoint with served model -- example tools (you can also use your own openai key - take a look into `rag_app.py` for more):
  - https://github.com/oobabooga/text-generation-webui
  - https://ollama.com/
  - https://github.com/vllm-project/vllm
  - https://github.com/PygmalionAI/aphrodite-engine

## Example

![Screen recording](docs/screen_recording.gif)


## How to start


1. *Install Python environment:**
```bash
uv sync
```

1. **Clone Blender manual into `data` directory:**
```bash
cd ./data
git clone https://projects.blender.org/blender/blender-manual.git
```

1. **Fill the vector database with task:**
```bash
task db-fill
```

1. **Start the Streamlit UI server with task:**
```bash
task ui
```

## Project Structure

- `app.py`: Main application file for the Streamlit UI.
- `data/`: Directory containing the Blender manual and other data.
- `docs/`: Documentation and media files.
- `rag_app.py`: Core logic for the RAG tool.
- `Taskfile.yaml`: Task definitions for go-task.
- `prompts.toml`: Contains the prompt templates used by the RAG tool.

## Environment Variables

The following environment variables can be used to configure the application in `Taskfile.yaml`:

| Variable Name     | Description                      | Example Value              |
| ----------------- | -------------------------------- | -------------------------- |
| `OPENAI_BASE_URL` | Base url for openai client       | http://localhost:5000/v1   |
| `MODEL`           | Model for text generation        | Qwen_Qwen2.5-1.5B-Instruct |
| `DB_NAME`         | Name of the db table for LanceDB | my_table_two               |

## Usage

Once the setup is complete, you can start interacting with the RAG tool through the Streamlit UI. The tool will provide detailed, contextually relevant information about Blender based on the queries you input.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.