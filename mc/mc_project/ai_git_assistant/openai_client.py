def call_openai(system_msg: str, prompt: str) -> str: 
    if not hasattr(call_openai, "_client"):
        from openai import OpenAI
        from dotenv import load_dotenv
        load_dotenv()
        call_openai._client = OpenAI()  # 함수에 속성으로 저장 (전역 변수 안 씀)

    client = call_openai._client
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
