import os
import time
from lib.models.models import Document, Prompt, RetreivedDocument
import lancedb
from openai import OpenAI, Stream
import toml
from lib.logger import log
from lancedb.rerankers import RRFReranker


class RagApp:
    def __init__(
        self,
        table_name: str = "",
        base_url: str = "",
        prompt_path: str = "prompts.toml",
    ) -> None:
        self.table_name = os.environ["DB_NAME"]
        self.init_db()
        self.client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"] or "",
            base_url=os.environ["OPENAI_BASE_URL"],
        )
        self.prompt = self._load_prompt_from_toml(prompt_path)[0]
        self.model = os.environ["MODEL"]
        self.latest_prompt = ""
        self.reranker = RRFReranker(return_score="all")
        self.doc_list = []

    def _load_prompt_from_toml(self, file: str) -> list[Prompt]:
        prompts = []
        with open(file or "prompts.toml") as f:
            raw_list = toml.load(f)
            prompts = [
                Prompt(id=id, **raw_prompt) for id, raw_prompt in raw_list.items()
            ]

        return prompts

    def get_latest_prompt(self) -> Prompt:
        if not self.latest_prompt:
            return ""
        else:
            return self.latest_prompt

    def get_openai_base_url(self) -> str:
        return self.client.base_url

    def set_openai_base_url(self, base_url: str):
        self.client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"] or "fake_key",
            base_url=base_url,
        )

    def set_model(self, model: str):
        self.model = model

    def get_model(self) -> str:
        return self.model

    def get_available_models(self) -> list:
        return self.client.models.list()

    def get_docs(self) -> list:
        return self.doc_list or []

    def init_db(self):
        log.info("Setting up db")
        t_start = time.time()
        db = lancedb.connect("./data/lance")

        self.tbl = db.create_table(self.table_name, schema=Document, exist_ok=True)
        t_total = time.time() - t_start
        log.info(f"Fnished setting up db - took {t_total:.2f} seconds")

    def prompt_llm(self, query: str) -> Stream:
        prompt = self.prompt.template

        resp = self.client.chat.completions.create(
            messages=[
                dict(
                    role="system",
                    content=prompt,
                ),
                dict(role="user", content=query),
            ],
            model=self.model,
            max_tokens=250,
            stream=True,
        )

        self.latest_prompt = prompt

        return resp

    def search(self, query: str) -> tuple[Stream, Document]:
        """Main entry point for chat completion.
        This function will search the database for the query and then start the chat completion woith the retrieved document.
        """

        # Get top three search results and put them into the prompt...
        top_k = self.db_search(query, top_k=3)
        top_k_string = "".join(
            [
                f"\n\nSearch result: {i}:\n{str(text.text).strip()}"
                for i, text in enumerate(top_k)
            ]
        )

        log.info("Starting chat completion")
        prompt = self.prompt.template.replace("__DOCS__", top_k_string).replace(
            "__DATE__", "17.10.2024, 12 PM"
        )
        resp = self.client.chat.completions.create(
            messages=[
                dict(
                    role="system",
                    content=prompt,
                ),
                dict(role="user", content=query),
            ],
            model=self.model,
            max_tokens=250,
            stream=True,
        )

        self.latest_prompt = prompt

        return resp, top_k

    def db_search(
        self, query: str, limit: int = 10, top_k: int | None = None
    ) -> list[Document]:
        log.info("Vector Search start")

        results = (
            self.tbl.search(query, query_type="hybrid")
            .limit(limit)
            .rerank(self.reranker)
            .to_list()
        )

        doc_list = [RetreivedDocument.model_validate(r) for r in results]

        top_k = doc_list[
            : top_k or limit
        ]  # sorted(doc_list, key=lambda x: x.score)[: top_k or limit]

        self.doc_list = top_k

        return top_k
