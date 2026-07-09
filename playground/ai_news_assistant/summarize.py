import ollama

from config import OLLAMA_MODEL


def summarize(news):

    prompt = "请总结今天 Hacker News 前20条新闻。\n\n"

    for item in news:

        prompt += f"- {item['title']}\n"

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]