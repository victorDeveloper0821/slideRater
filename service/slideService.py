## import slides presentation
from pptx import Presentation

def extract_pptx_content(pptx_path):
    # 加載PPT
    prs = Presentation(pptx_path)
    ppt_data = []

    # 遍歷每一張幻燈片
    for slide_number, slide in enumerate(prs.slides, start=1):
        slide_data = {
            'slide_number': slide_number,
            'title': "",
            'footer': "",
            'content': [],
            'bullet_points': []
        }

        # 提取每張幻燈片的主題
        for shape in slide.shapes:
            if shape.has_text_frame:
                # 提取標題
                if shape == slide.shapes.title:
                    slide_data['title'] = shape.text

                # 提取頁腳 (根據假設頁腳有特殊標記或位置)
                if "Footer" in shape.name:
                    slide_data['footer'] = shape.text

                # 遍歷每個 TextFrame 的段落
                for paragraph in shape.text_frame.paragraphs:
                    # 判斷是否為 bullet point
                    if paragraph.level > 0:
                        slide_data['bullet_points'].append({
                            'level': paragraph.level,
                            'text': paragraph.text
                        })
                    else:
                        # 普通文本
                        slide_data['content'].append(paragraph.text)

        ppt_data.append(slide_data)

    return ppt_data


if __name__ == '__main__':
# 使用示例
    pptx_path = 'your_pptx_file.pptx'
    ppt_data = extract_pptx_content(pptx_path)

# 顯示提取的數據
    for slide in ppt_data:
        print(f"Slide {slide['slide_number']} Title: {slide['title']}")
        print(f"Footer: {slide['footer']}")
        print("Content:")
        for text in slide['content']:
            print(f"  - {text}")
            print("Bullet Points:")
        for bullet in slide['bullet_points']:
            print(f"  Level {bullet['level']}: {bullet['text']}")
        print("\n")
