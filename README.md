

This project uses the Taskfile utility for efficient development.
The taskfile also defines env variables like custom OpenAi api endpoint or Model-Name.

Prerequisites:
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


1. Install python enviroment:
```bash
uv sync
```

1. Clone blender manual into `data` dir.
```bash
cd ./data
git clone https://projects.blender.org/blender/blender-manual.git
```

1. Filling vector dc with task:
```bash
task db-fill
```

1. After that, start Streamlit-ui server with task:
```bash
task ui
```