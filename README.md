## Streaming Response Demo
LLM連携のAPIのサンプル

### セットアップ

```bash
uv sync
```

`.env` ファイルを作成してAnthropicのAPIキーを設定

```bash
ANTHROPIC_API_KEY=sk-ant-api03-EXAMPLE
```

### 実行方法

```bash
uvicorn main:app --reload
```
