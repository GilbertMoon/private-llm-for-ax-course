from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
import json


CHAT_MODEL_ID = "mock-chat-model"
EMBEDDING_MODEL_ID = "mock-embedding-model"


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/v1/models":
            self._send_json(
                {
                    "object": "list",
                    "data": [
                        {"id": CHAT_MODEL_ID, "object": "model"},
                        {"id": EMBEDDING_MODEL_ID, "object": "model"},
                    ],
                }
            )
            return

        self._send_json({"error": "not found"}, status=404)

    def do_POST(self) -> None:  # noqa: N802
        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length) if content_length else b"{}"
        payload = json.loads(raw.decode("utf-8"))

        if self.path == "/v1/chat/completions":
            model = payload.get("model")
            if model != CHAT_MODEL_ID:
                self._send_json({"error": {"message": "model not found"}}, status=404)
                return

            self._send_json(
                {
                    "id": "chatcmpl-mock",
                    "object": "chat.completion",
                    "created": 0,
                    "model": CHAT_MODEL_ID,
                    "choices": [
                        {
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": "Mock local model response",
                            },
                            "finish_reason": "stop",
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 1,
                        "completion_tokens": 1,
                        "total_tokens": 2,
                    },
                }
            )
            return

        if self.path == "/v1/embeddings":
            model = payload.get("model")
            if model != EMBEDDING_MODEL_ID:
                self._send_json({"error": {"message": "model not found"}}, status=404)
                return

            self._send_json(
                {
                    "object": "list",
                    "model": EMBEDDING_MODEL_ID,
                    "data": [
                        {
                            "object": "embedding",
                            "index": 0,
                            "embedding": [0.1, 0.2, 0.3, 0.4],
                        }
                    ],
                    "usage": {"prompt_tokens": 1, "total_tokens": 1},
                }
            )
            return

        self._send_json({"error": "not found"}, status=404)

    def log_message(self, format: str, *args) -> None:
        return


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 1234), Handler)
    print("mock OpenAI-compatible server listening on 127.0.0.1:1234", flush=True)
    server.serve_forever()
