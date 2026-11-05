from dotenv import load_dotenv

from template import OPENAI_MINI_MODEL, OPENAI_MODEL, call_openai, retry_with_backoff

# Đọc OPENAI_API_KEY từ file .env ở thư mục gốc (nếu có)
load_dotenv()

PROMPT = "Giải thích LLM trong 2 câu"
# Model chính trước, model dự phòng sau (dùng khi model chính lỗi kéo dài)
MODELS = [OPENAI_MODEL, OPENAI_MINI_MODEL]

for model in MODELS:
    try:
        # Chờ 2s, 4s, 8s, 16s giữa các lần thử lại (tối đa ~30s mỗi model)
        text, latency, usage = retry_with_backoff(
            lambda: call_openai(PROMPT, model=model, max_tokens=1024),
            max_retries=4,
            base_delay=2,
        )
        break
    except Exception as e:
        print(f"[{model}] không gọi được: {e}\n")
else:
    raise SystemExit("Tất cả model đều đang lỗi, hãy thử lại sau ít phút.")

print(f"Model: {model}")
print(text)
print(f"Latency: {latency:.2f}s")
print(usage)
