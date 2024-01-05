from PIL import Image
from openai import OpenAI

import pytesseract

def tesseract_process(path):
    ocr_result = pytesseract.image_to_string(Image.open(path), config='--psm 3', lang='vie')

    client = OpenAI(
        api_key="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",
    )

    chatgpt_prompt = "Chỉnh sửa những từ sai, chỉ chỉnh sửa, không thêm hoặc cắt bỏ nội dung của đoạn sau.\n\n" + ocr_result
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": chatgpt_prompt}]
    )

    return(chat_completion.choices[0].message.content)

