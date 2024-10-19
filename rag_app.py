import os
import time
from models import Document, Prompt
import lancedb
from rich import print
from openai import OpenAI, Stream
import toml
from logger import log


class RagApp:
    def __init__(
        self, table_name: str, base_url: str, prompt_path: str = "prompts.toml"
    ) -> None:
        self.table_name = table_name
        self.init_db()
        self.client = OpenAI(api_key="fake", base_url=base_url)
        self.prompt = self._load_prompt_from_toml(prompt_path)[0]

    def _load_prompt_from_toml(self, file: str) -> list[Prompt]:
        prompts = []
        with open(file or "prompts.toml") as f:
            raw_list = toml.load(f)
            prompts = [
                Prompt(id=id, **raw_prompt) for id, raw_prompt in raw_list.items()
            ]

        return prompts

    def init_db(self):
        log.info("Setting up db")
        t_start = time.time()
        db = lancedb.connect("./data/lance")

        self.tbl = db.create_table(self.table_name, schema=Document, exist_ok=True)
        t_total = time.time() - t_start
        log.info(f"Fnished setting up db - took {t_total:.2f} seconds")

    def search(self, query: str) -> tuple[Stream, Document]:
        """Main entry point for chat completion.
        This function will search the database for the query and then start the chat completion woith the retrieved document.
        """

        dense_result = self._db_search(query)

        log.info("Starting chat completion")
        resp = self.client.chat.completions.create(
            messages=[
                dict(
                    role="system",
                    content=self.prompt.template.replace(
                        "__DOCS__", dense_result.text
                    ).replace("__DATE__", "17.10.2024, 12 PM"),
                ),
                dict(role="user", content=query),
            ],
            model=os.environ["MODEL"],
            max_tokens=250,
            stream=True,
        )

        return resp, dense_result

    def _db_search(self, query: str):
        log.info("Vector Search start")
        result = self.tbl.search(query, query_type="hybrid").limit(1).to_list()[0]

        return Document.model_validate(result)
