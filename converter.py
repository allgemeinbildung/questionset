import json
import os
import sys

def convert_question(question):
    """
    Converts a single question from the input format to the desired output format.
    """
    converted_question = {}
    options = question.get("options", [])
    correct_answer = question.get("correctAnswer", "")
    explanation = question.get("explanation", "")
    question_text = question.get("question", "")

    # Determine question type
    if set(options) == {"Richtig", "Falsch"} and len(options) == 2:
        # True/False Question
        converted_question["type"] = "TrueFalse"
        converted_question["bloom_level"] = "Erinnern"  # Default value
        converted_question["question"] = f"<p>{question_text}</p>"

        # Map "Richtig" to True and "Falsch" to False
        correct_bool = True if correct_answer == "Richtig" else False
        converted_question["correct_answer"] = correct_bool

        # Feedbacks
        converted_question["feedback_correct"] = "✅ Richtig! " + explanation if correct_bool else "✅ Falsch! " + explanation
        converted_question["feedback_incorrect"] = f"❌ Falsch. {explanation}" if correct_bool else f"❌ Richtig. {explanation}"
    else:
        # Multiple Choice Question
        converted_question["type"] = "MultipleChoice"
        converted_question["bloom_level"] = "Erinnern"  # Default value
        converted_question["question"] = f"<p>{question_text}</p>"

        converted_options = []
        for option in options:
            option_dict = {
                "text": option,
                "is_correct": option == correct_answer
            }
            if option == correct_answer:
                option_dict["feedback"] = "✅ Richtig!"
            else:
                option_dict["feedback"] = f"❌ Falsch. {explanation}"
            converted_options.append(option_dict)
        
        converted_question["options"] = converted_options

    return converted_question

def convert_json(input_data):
    """
    Converts the entire input JSON data to the desired output format.
    """
    output_data = {
        "title": "",  # To be filled later
        "media": {
            "type": "",
            "url": "",
            "source": ""
        },
        "questions": []
    }

    for question in input_data:
        converted = convert_question(question)
        output_data["questions"].append(converted)
    
    return output_data

def get_json_files(input_folder):
    """
    Retrieves a list of JSON files in the specified input folder.
    """
    try:
        files = os.listdir(input_folder)
        json_files = [file for file in files if file.lower().endswith('.json')]
        return json_files
    except Exception as e:
        print(f"Error accessing input folder: {e}")
        sys.exit(1)

def main():
    print("=== Batch JSON Quiz Converter ===\n")

    # Prompt for input folder path
    input_folder = input("Enter the path to the input folder containing JSON files: ").strip()
    while not os.path.isdir(input_folder):
        print("The folder does not exist. Please try again.")
        input_folder = input("Enter the path to the input folder containing JSON files: ").strip()

    # Prompt for output folder path
    output_folder = input("\nEnter the path to the output folder where converted JSON files will be saved: ").strip()
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
            print(f"Created output directory: {output_folder}")
        except Exception as e:
            print(f"Error creating output folder: {e}")
            sys.exit(1)

    # Retrieve list of JSON files
    json_files = get_json_files(input_folder)
    if not json_files:
        print("No JSON files found in the input folder.")
        sys.exit(0)
    
    print(f"\nFound {len(json_files)} JSON file(s) to convert.\n")

    for file in json_files:
        input_path = os.path.join(input_folder, file)
        try:
            with open(input_path, 'r', encoding='utf-8') as infile:
                input_data = json.load(infile)
                if not isinstance(input_data, list):
                    print(f"Skipping {file}: JSON content is not a list of questions.")
                    continue
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue

        # Generate title from file name (without extension)
        title = os.path.splitext(file)[0]

        # Convert data
        output_data = convert_json(input_data)
        output_data["title"] = title  # Set the title

        # Define output file path
        output_file_name = f"converted_{file}"
        output_path = os.path.join(output_folder, output_file_name)

        # Save output JSON data
        try:
            with open(output_path, 'w', encoding='utf-8') as outfile:
                json.dump(output_data, outfile, ensure_ascii=False, indent=2)
            print(f"Successfully converted {file} -> {output_file_name}")
        except Exception as e:
            print(f"Error writing to {output_file_name}: {e}")

    print("\n=== Conversion Completed ===")

if __name__ == "__main__":
    main()
