import os
from openai import OpenAI
from pathlib import Path

# OpenAI API 키 설정
base_url = "https://api.aimlapi.com/v1"
api_key = os.getenv("AI_ML_API_KEY")

api = OpenAI(base_url=base_url, api_key=api_key)

if not api_key:
    raise ValueError("AI_ML_API_KEY is not set in the environment variables")

# 프로젝트 폴더 경로
PROJECT_DIR = Path("./src/main/resources/templates")  # Spring Boot HTML 파일 경로
TEST_OUTPUT_DIR = Path("./src/test/java/com/example/selenium")

# 주요 HTML 파일 탐색
html_files = [f for f in PROJECT_DIR.glob("**/*.html")]

# Selenium 테스트 코드 생성 함수
def generate_selenium_test(html_file):
    with open(html_file, "r") as file:
        html_content = file.read()

    prompt = f"""
    Generate a Selenium test in Java for the following HTML file. Include:
    1. Navigating to the page URL.
    2. Interacting with input fields, buttons, and links.
    3. Verifying elements and redirects.

    HTML:
    {html_content}
    """

    response = api.chat.completions.create(
        # model="gpt-4",
        model="mistralai/Mistral-7B-Instruct-v0.2",
        prompt=prompt,
        max_tokens=800
    )
    return response.choices[0].text.strip()

# 생성된 코드를 파일로 저장
for html_file in html_files:
    test_code = generate_selenium_test(html_file)
    test_file_name = TEST_OUTPUT_DIR / f"{html_file.stem.capitalize()}Test.java"

    with open(test_file_name, "w") as test_file:
        test_file.write(test_code)
