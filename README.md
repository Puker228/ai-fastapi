# ai-fastapi

basic fastapi application using llm

## python deps

[uv](https://docs.astral.sh/uv/getting-started/installation/) is used to install dependencies:

```shell
uv sync
```

## run project

Before starting the project, you need to copy .env-example-docker to .env:

```shell
cp .env-example-docker .env
```

After the previous step, run the following command:

```shell
make up
```

## config

The project uses a local model through [ollama](https://ollama.com/).
To replace the model, you need to change the `AI_MODEL` parameter in .env

