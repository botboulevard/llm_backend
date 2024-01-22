# llm-backend

```sh
export CUDA_VISIBLE_DEVICES="1,2,3,4" && python -m vllm.entrypoints.openai.api_server \
    --model TheBloke/OpenHermes-2.5-Mistral-7B-AWQ \
    --port "8090" \
    --host 0.0.0.0 \
    --dtype float16 \
    --download-dir ../hf_models \
    --quantization awq \
     -tp 4 --engine-use-ray

```


TheBloke/Orca-2-7B-GGUF