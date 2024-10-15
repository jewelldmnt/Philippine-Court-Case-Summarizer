from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pdfplumber
from sqlalchemy.orm import declarative_base
from bs4 import BeautifulSoup
import requests
import re
import os

import requests
from bs4 import BeautifulSoup
import re

def scrape_court_case(url):
    try:
        result = requests.get(url)
        result.raise_for_status()  # Raises an error for any non-200 status codes
        
        doc = BeautifulSoup(result.text, "html.parser")

        content_class = "entry-content alignfull wp-block-post-content has-global-padding is-layout-constrained wp-block-post-content-is-layout-constrained"
        title_element = doc.find_all("h3")
        
        if not title_element:
            raise ValueError("Title not found in the document")

        title = title_element[0]

        paragraphs = title.find_all("p")
        if not paragraphs:
            raise ValueError("No paragraphs found under title")

        decision_text = paragraphs[-1].text.strip()  # Keep only leading/trailing spaces
        paragraphs[-1].extract()

        content = doc.find(class_=content_class)
        if content is None:
            raise ValueError("Content class not found in the document")

        # Remove unnecessary tags
        for i in content.find_all(["h2", "h3", "sup", "tbody", "strong"]):
            i.extract()
            
        for blockquote in content.find_all("blockquote"):
            prev_sibling = blockquote.find_previous_sibling()


            # Check if the previous sibling is a <p> tag
            if prev_sibling and prev_sibling.name == 'p':

                prev_sibling.append(f" {blockquote.get_text()}")


                # Remove the blockquote after merging its content
                blockquote.extract()

                # Clean up text using regular expressions
                new_content_text = content.get_text()

        patterns_to_clean = [
            r'\[(?:\bx\s+)+x\b\]',  # e.g., [x x]
            r'(?:\b.\s+)+x\b',  # e.g., . x
            r'\.{2,}',  # multiple dots
            r'…',  # ellipsis
            r'x{2,}',  # multiple x's
            r'X{2,}',  # multiple X's
            r'\. \. \. \. '  # spaced dots
        ]
        
        for pattern in patterns_to_clean:
            new_content_text = re.sub(pattern, '', new_content_text)

        # Slice content up to "SO ORDERED"
        sliced_content = new_content_text.strip()
        if "SO ORDERED" in sliced_content:
            sliced_content = sliced_content[:sliced_content.rfind("SO ORDERED") + 11]

        title_text = title.text.strip().replace("\n", " ")

        return {
            "title": title_text,
            "case_text": sliced_content
        }

    except requests.exceptions.RequestException as req_err:
        print(f"Network error: {str(req_err)}")
        return None
    except Exception as e:
        print(f"Error in scrape_court_case: {str(e)}")
        return None






app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


Base = declarative_base()


class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, nullable=False)
    file_text = db.Column(db.String, nullable=False)
    file_content = db.Column(db.LargeBinary)

    def to_json(self):
        return {
            "id": self.id,
            "file_name": self.file_name,
            "file_text": self.file_text,
            "file_content": str(self.file_content)
        }


@app.route("/hello")
def hello():
    return "hello"


@app.route("/get-files", methods=["GET"])
def get_files():
    files = File.query.all()
    result = [file.to_json() for file in files]
    return jsonify(result)



import re

@app.route("/send-file", methods=["POST"])
def send_file():
    try:
        if request.method == "POST":
            data = request.json
            court_case_link = data.get('link')

            if not court_case_link:
                return jsonify({"error": "No court case link provided"}), 400

            court_case = scrape_court_case(court_case_link)

            if not court_case or 'title' not in court_case or 'case_text' not in court_case:
                return jsonify({"error": "Invalid court case data"}), 400

            case_title = court_case["title"]

            # Sanitize the case title to create a valid file name
            case_title = re.sub(r'[\\/*?:"<>|]', "-", case_title)  # Replace invalid characters with '-'
            case_title = re.sub(r'[\.,]', "", case_title)  # Optionally remove commas and periods

            # Limit the filename length (for example, to 150 characters)
            max_length = 150
            txt_case_title = case_title[:max_length] if len(case_title) > max_length else case_title

            txt_file_name = f"{txt_case_title}.txt"

            try:
                # Writing the court case text to a .txt file
                with open(txt_file_name, "w", encoding="utf-8") as f:
                    f.write(court_case["case_text"])

                # Reading the file content for storage
                with open(txt_file_name, "rb") as f:
                    file_content = f.read()

            except IOError as e:
                return jsonify({"error": "File handling error: " + str(e)}), 500

            # Uploading the file to the database
            try:
                upload = File(
                    file_name=case_title,
                    file_text=court_case["case_text"],
                    file_content=file_content
                )

                db.session.add(upload)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                return jsonify({"error": "Database error: " + str(e)}), 500

            # Optionally delete the file after saving to the database
            try:
                os.remove(txt_file_name)
            except OSError as e:
                return jsonify({"error": "File deletion error: " + str(e)}), 500

            return jsonify({"msg": "successful", "file": txt_file_name})

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500





@app.route("/delete-file/<int:id>", methods=["DELETE"])
def delete_file(id):
    try:
        file = db.session.get(File, id)  
        if file is None:
            return jsonify({"error": "File not found"}), 404

        db.session.delete(file)
        db.session.commit()
        return jsonify({"msg": "File deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/update-file/<int:id>", methods=["PATCH"])
def update_file(id):
    try:
        file = db.session.get(File, id)  
        if file is None:
            return jsonify({"error": "File not found"}), 404

        data = request.json
        file.file_name = data.get("file_name", file.file_name)
        file.file_text = data.get("file_text", file.file_text)


        if "file_content" in data:
            file.file_content = bytes(data["file_content"], 'utf-8')  
        
        db.session.commit()
        print("file:", file)

        return jsonify(file.to_json()), 200
    except Exception as e:
        print("error:", e)
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/get-preprocessed/<int:id>", methods=["POST"])
def get_preprocessed(id):
    try:
        from Custom_Modules.TestingPreprocessing import Preprocessing

        file = db.session.get(File, id)
        if file is None:
            return jsonify({"error": "Court case not found"}), 404


        court_case_text = file.file_text


        if not court_case_text:
            return jsonify({"error": "No case text provided"}), 400


        # summary = "TITLE:"+ "\n" + file.file_name+ "\n\n" + summarize_case(court_case_text)
        # print(summary)

        preprocessor = Preprocessing()


        cleaned_text = preprocessor.clean_text(court_case_text)
        tokenized_paragraphs = preprocessor.tokenize_by_paragraph(cleaned_text)


        return jsonify({"cleaned_text": tokenized_paragraphs}), 200

    except Exception as e:
        print("Error during preprocess:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/get-segmented", methods=["POST"])
def get_segmented():
    try:
        from Custom_Modules.TestingParagraphSegmentation import ParagraphSegmentation

        data = request.json
        preprocessed_case = data.get('cleaned_text')


        segmentation = ParagraphSegmentation(model_path='56')
        split_paragraphs = segmentation.split_paragraph(preprocessed_case)
        print(split_paragraphs)
        predicted_labels = segmentation.sequence_classification(split_paragraphs)


        if not preprocessed_case:
            return jsonify({"error": "No case text provided"}), 400


        return jsonify({"segmented_case": predicted_labels}), 200

    except Exception as e:
        print("Error during segmentation:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/get-summarized/<int:id>", methods=["POST"])
def get_summarized(id):
    try:
        from Custom_Modules.LSA import LSA

        data = request.json
        segmented_case = data.get('segmented_case')


        if not segmented_case:
            return jsonify({"error": "No case text provided"}), 400

        lsa = LSA(segmented_case)
        summarize_case = lsa.create_summary()

        file = db.session.get(File, id)

        summary = "TITLE:"+ "\n" + file.file_name+ "\n\n" + summarize_case
        print(summary)


        return jsonify({"summary": summary}), 200

    except Exception as e:
        print("Error during summarization:", e)
        return jsonify({"error": str(e)}), 500




with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
