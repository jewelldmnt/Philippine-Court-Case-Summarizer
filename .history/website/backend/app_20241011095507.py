from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pdfplumber
from sqlalchemy.orm import declarative_base
from bs4 import BeautifulSoup
import requests
import re
import os

# Define a function to process the text and summarize it
def summarize_case(case_text):
    from Custom_Modules.InputConversion import InputConversion
    from Custom_Modules.TestingParagraphSegmentation import ParagraphSegmentation
    from Custom_Modules.TestingPreprocessing import Preprocessing

    # Create an instance of the TextPreprocessor
    preprocessor = Preprocessing()

    # Clean the text
    cleaned_text = preprocessor.clean_text(case_text)

    # Tokenize the text into paragraphs
    tokenized_paragraphs = preprocessor.tokenize_by_paragraph(cleaned_text)

    # Initialize the ParagraphSegmentation class with the path to your fine-tuned model
    segmentation = ParagraphSegmentation(model_path='my_awesome_model/checkpoint-886')

    # Split paragraphs into dictionary form
    split_paragraphs = segmentation.split_paragraph(tokenized_paragraphs)

    # Perform sequence classification on the split paragraphs
    predicted_labels = segmentation.sequence_classification(split_paragraphs)

    # Optionally, return the segmented and labeled paragraphs in dictionary form
    print(predicted_labels)
    return predicted_labels

def scrape_court_case(url):
    try:
        result = requests.get(url)
        if result.status_code != 200:
            raise ValueError(f"Error fetching the court case: {result.status_code}")

        doc = BeautifulSoup(result.text, "html.parser")

        content_class = "entry-content alignfull wp-block-post-content has-global-padding is-layout-constrained wp-block-post-content-is-layout-constrained"
        title_element = doc.find_all("h3")
        
        # Check if title exists
        if not title_element:
            raise ValueError("Title not found in the document")

        title = title_element[0]

        # Ensure there are paragraphs under the title
        paragraphs = title.find_all("p")
        if not paragraphs or len(paragraphs) == 0:
            raise ValueError("No paragraphs found under title")

        decision_text = paragraphs[-1].text.replace(" ", "")
        paragraphs[-1].extract()  # Remove the last paragraph from the title

        # Extract content
        content = doc.find(class_=content_class)
        if content is None:
            raise ValueError("Content class not found in the document")

        # Clean content by removing certain tags
        for i in content.find_all(["h2", "h3", "sup", "tbody", "strong"]):
            i.extract()

        # Remove all elements after the first <hr> tag if it exists
        hr_tag = content.find("hr")
        if hr_tag:
            for sibling in hr_tag.find_next_siblings():
                sibling.extract()

        # Clean and process the extracted content
        new_content = BeautifulSoup(str(content), "html.parser")
        new_content_text = new_content.text  # Get the plain text

        # Apply regex cleaning
        new_content_text = re.sub(r'\[(?:\bx\s+)+x\b\]', '', new_content_text)
        new_content_text = re.sub(r'(?:\b.\s+)+x\b', '', new_content_text)
        new_content_text = re.sub(r'\.{2,}', '', new_content_text)
        new_content_text = re.sub(r'…', '', new_content_text)
        new_content_text = re.sub(r'. . . .', '', new_content_text)
        new_content_text = re.sub(r'x{2,}', '', new_content_text)
        new_content_text = re.sub(r'X{2,}', '', new_content_text)

        # Ensure the content includes "SO ORDERED"
        sliced_content = new_content_text.strip()
        if "SO ORDERED" in sliced_content:
            sliced_content = sliced_content[:sliced_content.rfind("SO ORDERED") + 11]

        # Final cleaning steps
        # sliced_content = sliced_content.replace("\n", " ").replace("\xa0", " ")
        title_text = title.text.strip().replace("\n", " ")

        return {
            "title": title_text,
            "case_text": sliced_content
        }

    except Exception as e:
        print(f"Error in scrape_court_case: {str(e)}")
        return None  # Return None or raise to be handled in the calling function




# Initialize Flask app and configurations
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

# Use the correct base for SQLAlchemy 2.x
Base = declarative_base()

# Define the File model
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
            "file_text": self.file_text,  # Optional: include the extracted text
            "file_content": str(self.file_content)  # Handle binary data appropriately
        }

# Basic hello route for testing
@app.route("/hello")
def hello():
    return "hello"

# Route to fetch all files
@app.route("/get-files", methods=["GET"])
def get_files():
    files = File.query.all()
    result = [file.to_json() for file in files]
    return jsonify(result)



@app.route("/send-file", methods=["POST"])
def send_file():
    try:
        if request.method == "POST":
            data = request.json
            court_case_link = data.get('link')
            print(court_case_link)

            # Scrape the court case
            court_case = scrape_court_case(court_case_link)
            print("Scraped court case:", court_case)  # Debug print

            # Check if court_case is valid
            if not court_case or 'title' not in court_case or 'case_text' not in court_case:
                return jsonify({"error": "Invalid court case data"}), 400

            # Save the court case details into the database
            case_title = court_case["title"].replace('/', '-')  # Replace '/' to avoid directory issues
            case_text = court_case["case_text"]
            txt_file_name = f"{case_title}.txt"

            # Create the file path and write the case text to it
            with open(txt_file_name, "w", encoding="utf-8") as f:
                f.write(case_text)

            # Read the text file as binary
            with open(txt_file_name, "rb") as f:
                file_content = f.read()  # Read the binary content of the file

            # Create a new File entry with title, text, and binary content
            upload = File(
                file_name=case_title,
                file_text=case_text,
                file_content=file_content  # Store the binary content in the database
            )

            db.session.add(upload)
            db.session.commit()

            return jsonify({"msg": "successful", "file": txt_file_name})
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": str(e)})



# Route to delete a file by ID
@app.route("/delete-file/<int:id>", methods=["DELETE"])
def delete_file(id):
    try:
        file = db.session.get(File, id)  # Correct usage: pass model and ID
        if file is None:
            return jsonify({"error": "File not found"}), 404

        db.session.delete(file)
        db.session.commit()
        return jsonify({"msg": "File deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Route to update a file's information
@app.route("/update-file/<int:id>", methods=["PATCH"])
def update_file(id):
    try:
        file = db.session.get(File, id)  # Fetch the file from the database
        if file is None:
            return jsonify({"error": "File not found"}), 404

        data = request.json
        file.file_name = data.get("file_name", file.file_name)
        file.file_text = data.get("file_text", file.file_text)

        # Update file_content if provided
        if "file_content" in data:
            file.file_content = bytes(data["file_content"], 'utf-8')  # Convert to bytes
        
        db.session.commit()
        print("file:", file)

        return jsonify(file.to_json()), 200
    except Exception as e:
        print("error:", e)
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Summarization route placeholder
# Route to summarize the court case text
@app.route("/get-summarized/<int:id>", methods=["GET"])
def get_summarized(id):
    try:
        # Get the court case text from the request
         # Fetch the court case from the database using the provided ID
        file = db.session.get(File, id)  # Retrieve the File object from the database
        if file is None:
            return jsonify({"error": "Court case not found"}), 404

        # Get the court case text from the file record
        court_case_text = file.file_text

        # Validate the input
        if not court_case_text:
            return jsonify({"error": "No case text provided"}), 400

        # Call the summarization function
        summary = summarize_case(court_case_text)
        print(summary)

        # Return the summary as JSON
        return jsonify({"summary": summary}), 200

    except Exception as e:
        print("Error during summarization:", e)
        return jsonify({"error": str(e)}), 500


# Ensure tables are created
with app.app_context():
    db.create_all()

# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True)
