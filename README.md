# health-assistant-chatbox
A local AI-powered health chatbot built with LLaMA 2 and Streamlit, running on Google Colab.

## Requirements

* Python (for `pip` commands)
* Node.js (for `npm` commands)
* Google Colab with T4 GPU enabled

## Setup

### Enable GPU in Colab
1. Click **Runtime** → **Change runtime type**
2. Set Hardware accelerator to **T4 GPU**
3. Click **Save**

---

### Step 1 — Install dependencies

```python
!pip install streamlit
!pip install ctransformers
```

---

### Step 2 — Create app.py

### Step 3 — Download the LLM

```python
!wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q2_K.bin
```

---

### Step 4 — Install cloudflared

```python
!wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
!chmod +x cloudflared
```

---

### Step 5 — Launch the app

```python
import subprocess
import time
import re

subprocess.run(["pkill", "-f", "streamlit"], capture_output=True)
time.sleep(2)

subprocess.Popen([
    "streamlit", "run", "app.py",
    "--server.port=8501",
    "--server.headless=true"
])
time.sleep(4)

tunnel = subprocess.Popen(
    ["./cloudflared", "tunnel", "--url", "http://localhost:8501"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)

print("⏳ Starting tunnel, please wait...")
for line in tunnel.stdout:
    line = line.decode()
    if "trycloudflare.com" in line:
        url = re.search(r'https://\S+\.trycloudflare\.com', line)
        if url:
            print("✅ Your chatbot is live at:", url.group())
            break
```

---

### Step 6 — Open the app
Open the `trycloudflare.com` URL printed in the output above in your browser. Your chatbot is live! 🎉

## Notes

- GPU (T4) is required for fast responses — CPU will be very slow
- This chatbot is for informational purposes only — always consult a real doctor for medical advice
