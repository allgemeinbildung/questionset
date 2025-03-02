import re
import json
import os

def extract_laws(text):
    """
    Extracts law references from the provided text.
    A law reference is indicated by the symbol "➞" followed by a law (e.g., ZGB, OR)
    and one or more article numbers (which may include letters and be comma-separated).
    
    Returns a list of dictionaries, each with keys:
      - "law": The law abbreviation (e.g., "ZGB")
      - "articles": A list of article numbers (e.g., ["2"] or ["11", "12"])
    """
    pattern = r"➞\s*([A-Z]+)\s+((?:\d+[a-z]?)(?:,\s*\d+[a-z]?)*)"
    matches = re.findall(pattern, text)
    laws = []
    for law, articles in matches:
        articles_list = [a.strip() for a in articles.split(",")]
        laws.append({"law": law, "articles": articles_list})
    return laws

def extract_chapters(text):
    """
    Splits the document into chapters using the header "Das weiss ich jetzt! Kapitel <number>".
    Returns a list of dicts with the chapter number and the corresponding content.
    """
    parts = re.split(r"(Das weiss ich jetzt!\s*Kapitel\s*\d+)", text, flags=re.IGNORECASE)
    chapters = []
    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        content = parts[i+1].strip() if i+1 < len(parts) else ""
        chap_match = re.search(r"Kapitel\s*(\d+)", header, re.IGNORECASE)
        chap_number = chap_match.group(1) if chap_match else ""
        chapters.append({"chapter": chap_number, "content": content})
    return chapters

def extract_questions(chapter_text):
    """
    Extracts questions and their answers from the chapter text.
    It looks for lines starting with a question number (e.g., 1.1) and assumes the answer
    is all text until the next question or end of chapter.
    
    If the answer contains subquestions (lines starting with a letter and a closing parenthesis),
    they are parsed into a list. Additionally, any law references (e.g., "➞ ZGB 2")
    found in the answer text or in subquestion text are extracted and stored in a "laws" field.
    """
    question_blocks = re.split(r"(?m)^(?=\d+\.\d+\s)", chapter_text)
    questions = []
    for block in question_blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.splitlines()
        head_match = re.match(r"^(\d+\.\d+)\s+(.*)", lines[0])
        if not head_match:
            continue
        q_number = head_match.group(1)
        q_text = head_match.group(2)
        answer_text = "\n".join(lines[1:]).strip()
        # Extract laws from the overall answer text.
        laws_overall = extract_laws(answer_text)
        
        # Check if there are subquestions (lines starting with a letter and a closing parenthesis)
        if re.search(r"(?m)^[a-z]\)\s", answer_text):
            subq_list = []
            sub_parts = re.split(r"(?m)^(?=[a-z]\))", answer_text)
            for sp in sub_parts:
                sp = sp.strip()
                if not sp:
                    continue
                sp_lines = sp.splitlines()
                sub_match = re.match(r"^([a-z])\)\s*(.*)", sp_lines[0])
                if sub_match:
                    letter = sub_match.group(1)
                    sub_question = sub_match.group(2)
                    sub_answer = "\n".join(sp_lines[1:]).strip() if len(sp_lines) > 1 else ""
                    sub_laws = extract_laws(sp)
                    subq_list.append({
                        "letter": letter,
                        "question": sub_question,
                        "answer": sub_answer,
                        "laws": sub_laws
                    })
            question_obj = {
                "number": q_number,
                "question": q_text,
                "subquestions": subq_list,
                "laws": laws_overall
            }
        else:
            question_obj = {
                "number": q_number,
                "question": q_text,
                "answer": answer_text,
                "laws": laws_overall
            }
        questions.append(question_obj)
    return questions

def extract_document(text):
    """
    Processes the entire document and returns a list of chapters.
    Each chapter is represented as a dict with its number and an array of questions.
    """
    chapters = extract_chapters(text)
    result = []
    for chap in chapters:
        questions = extract_questions(chap["content"])
        result.append({
            "chapter": chap["chapter"],
            "questions": questions
        })
    return result

if __name__ == "__main__":
    # Specify the full path to your document file.
    input_path = r"D:\OneDrive - bbw.ch\Desktop\tests\DWIJ\0. Das weiss ich jetzt V1_2022.txt"
    
    # Read the original text file.
    with open(input_path, "r", encoding="utf-8") as file:
        text = file.read()
    
    # Extract the data structure from the document.
    extracted_data = extract_document(text)
    
    # Determine the directory of the original file.
    base_dir = os.path.dirname(input_path)
    
    # Save each chapter as a separate JSON file in the same folder.
    for chapter in extracted_data:
        chapter_number = chapter["chapter"]
        output_filename = os.path.join(base_dir, f"chapter_{chapter_number}.json")
        with open(output_filename, "w", encoding="utf-8") as outfile:
            json.dump(chapter, outfile, ensure_ascii=False, indent=4)
        print(f"Saved chapter {chapter_number} to {output_filename}")
