# Pip Installs for langgraph

```bash
pip install langchain langchain_community langchain_ollama langgraph pydantic mavsdk
```

## Configuration

### Environment Variables

Create a `.env` file

```
VIRTUAL=true (make this false if you are connecting to the real drone via serial)

OLLAMA_BASE_URL=http://<ollama_machine_ip>:11434

OLLAMA_MODEL=llama3.1:8b
```
