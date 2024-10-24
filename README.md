# Blender Manual RAG-Tool

This project is a Retrieval-Augmented Generation (RAG) tool designed to assist with the Blender manual. It integrates with various custom OpenAI endpoints to provide detailed and contextually relevant information about Blender's features, workflows, and best practices.

## Prerequisites:

Before you start, ensure you have the following installed:

- go-task (https://github.com/go-task/task)
- uv (https://github.com/astral-sh/uv).
- ollama (might change in the future - for now embedder is used from ollama)
- custom openai endpoint with served model -- example tools (you can also use your own openai key - take a look into `rag_app.py` for more):
  - https://github.com/oobabooga/text-generation-webui
  - https://ollama.com/
  - https://github.com/vllm-project/vllm
  - https://github.com/PygmalionAI/aphrodite-engine

## Example

![Screen recording](docs/screen_recording.gif)


## How to start

1. *Copy and setup `.evn`:*
```bash
cp .env.example .env
```


2. *Install Python environment:**
```bash
uv sync
```

3. **Clone Blender manual into `data` directory:**
```bash
cd ./data
git clone https://projects.blender.org/blender/blender-manual.git
```

4. **Fill the vector database with task:**
```bash
task db-fill
```

5. **Start the Streamlit UI server with task:**
```bash
task ui
```

## Project Structure

- `app.py`: Main application entrypoint for streamlit.
- `data/`: Directory for Blender manual and lancedb data.
- `docs/`: Documentation and media files.
- `rag_app.py`: Core logic for the RAG tool.
- `Taskfile.yaml`: Task definitions for for development workflows.
- `prompts.toml`: Contains the prompt templates used by the RAG tool.
- `routes/`: Contains the route files for different pages.
  - `chat.py`: Chat page route.
  - `prompt.py`: Prompt page route.
  - `retrieval.py`: Retrieval page route.
  - `settings.py`: (WIP)

## Environment Variables

The following environment variables can be used to configure the application in `.env`:

| Variable Name     | Description                      | Example Value              |
| ----------------- | -------------------------------- | -------------------------- |
| `OPENAI_BASE_URL` | Base url for openai client       | http://localhost:5000/v1   |
| `MODEL`           | Model for text generation        | Qwen_Qwen2.5-1.5B-Instruct |
| `DB_NAME`         | Name of the db table for LanceDB | my_table_two               |

## Usage

Once the setup is complete, you can start interacting with the RAG tool through the Streamlit UI. The tool will provide detailed, contextually relevant information about Blender based on the queries you input.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.