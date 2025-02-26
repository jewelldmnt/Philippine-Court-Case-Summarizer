# =============================================================================
# Program Title: Legal Document Analysis Application
# Programmers: Nicholas Dela Torre, Jewell Anne Diamante, Miguel Tolentino
# Date Written: October 12, 2024
# Date Revised: January 24, 2025
#
# Purpose:
#     This application serves as the main entry point for a comprehensive
#     legal document analysis system, offering segmentation, summarization,
#     and insight generation from court case texts. It utilizes Latent
#     Semantic Analysis (LSA) to extract key information and present
#     a concise summary that highlights essential case elements (facts,
#     issues, and rulings).
#
#     By providing structured, summarized information, this application
#     enables legal professionals and automated systems to quickly review
#     complex legal documents, enhancing efficiency in legal research
#     and document management tasks.
#
# Where the program fits in the general system design:
#     As the main application driver, app.py orchestrates the loading,
#     processing, and summarizing of legal texts within the system. It
#     interacts with other components like the LSA module, topic segmentation,
#     and a document repository to provide end-to-end analysis and summary
#     generation.
#     
#     The application is intended for use in legal research tools, content
#     management systems, or integrated workflows, supporting rapid document
#     retrieval, classification, and recommendation.
#
# Data Structures, Algorithms, and Control:
#     - Data Structures:
#         - **case_data**: A dictionary storing raw and processed text data
#           for legal documents, including segments for facts, issues, and
#           rulings.
#         - **summaries**: A dictionary holding generated summaries for each
#           document, organized by section.
#     - Algorithms:
#         - **Text Preprocessing**: Cleans and prepares raw text for
#           analysis, including tokenization and stopword removal.
#         - **Topic Segmentation**: Divides documents into meaningful sections
#           (facts, issues, rulings) for targeted summarization.
#         - **Latent Semantic Analysis (LSA)**: Applies TF-IDF vectorization
#           and Singular Value Decomposition (SVD) to identify and rank
#           the most relevant sentences in each section.
#     - Control:
#         - The main application flow follows these steps:
#           1. Document loading and preprocessing
#           2. Topic segmentation
#           3. LSA-based summarization
#           4. Summary generation and display
# =============================================================================


# Import required libraries and modules
from flask import Flask, request, jsonify  # Flask for the web server
from flask_sqlalchemy import SQLAlchemy    # For database interactions
from flask_cors import CORS                # To handle cross-origin requests
from sqlalchemy.orm import declarative_base  # For SQLAlchemy models
from bs4 import BeautifulSoup              # For parsing HTML content
import requests                            # For making HTTP requests
import re                                  # For pattern matching
import os                                  # For OS-level interactions
import spacy                               # For NLP tasks
import base64                              # For encoding and decoding data


# Import custom modules
from Custom_Modules.Preprocess import preprocess  
from Custom_Modules.TopicSegmentation import TopicSegmentation  
from Custom_Modules.LSA import LSA                

# Initialize the preprocessor instance
preprocessor = preprocess(is_training=False)

# Set up the Flask application and enable CORS
app = Flask(__name__)
CORS(app)

# Configure the database to use SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

# Define the base for SQLAlchemy models
Base = declarative_base()

# Load the small English model for spaCy
nlp = spacy.load("en_core_web_sm")


def scrape_court_case(url):
    """
    Description:
    Scrapes a court case from the specified URL, extracting the title and main content text,
    while cleaning and formatting the text.

    Parameters:
    - url (str): The URL of the court case to scrape.

    Returns:
    - dict: A dictionary with the following keys:
        - "title" (str): The title of the court case.
        - "case_text" (str): The cleaned text content of the court case.
    - None: Returns None if there was an error during scraping or processing.
    """
    try:
        result = requests.get(url)
        result.raise_for_status()  # Raises an error for any non-200 status codes

        doc = BeautifulSoup(result.text, "html.parser")

        content_class = "entry-content alignfull wp-block-post-content has-global-padding is-layout-constrained wp-block-post-content-is-layout-constrained"
        title_element = doc.find_all("h2")

        if not title_element:
            raise ValueError("Title not found in the document")

        title = title_element[1]
    
        paragraphs = title.find_all("p")
        
        if not paragraphs:
            title_div = title.find_next_sibling("div")
            if title_div:
                paragraphs = title_div.find_all("p")
            else:
                raise ValueError("No <p> tags found under the title or its associated <div>")


        decision_text = paragraphs[
            -1
        ].text.strip()  # Keep only leading/trailing spaces
        paragraphs[-1].extract()

        content = doc.find(class_=content_class)
        if content is None:
            raise ValueError("Content class not found in the document")

        # Remove unnecessary tags
        for i in content.find_all(["h2", "h3", "sup", "tbody", "strong"]):
            i.extract()
        print("court case text",content)

        new_content_text = content.get_text()  # Initialize with the plain text of the content
        for blockquote in content.find_all("blockquote"):
            prev_sibling = blockquote.find_previous_sibling()

            # Check if the previous sibling is a <p> tag
            if prev_sibling and prev_sibling.name == "p":
                prev_sibling.append(f" {blockquote.get_text()}")

                # Remove the blockquote after merging its content
                blockquote.extract()

            # Clean up text using regular expressions
            new_content_text = content.get_text()
        
        if new_content_text == "":
            new_content_text = content

        patterns_to_clean = [
            r"\[(?:\bx\s+)+x\b\]",  # e.g., [x x]
            r"(?:\b.\s+)+x\b",  # e.g., . x
            r"\.{2,}",  # multiple dots
            r"…",  # ellipsis
            r"x{2,}",  # multiple x's
            r"X{2,}",  # multiple X's
            r"\. \. \. \. ",  # spaced dots
        ]

        for pattern in patterns_to_clean:
            new_content_text = re.sub(pattern, "", new_content_text)

        # Slice content up to "SO ORDERED"
        sliced_content = new_content_text.strip()
        if "SO ORDERED" in sliced_content:
            sliced_content = sliced_content[
                : sliced_content.rfind("SO ORDERED") + 11
            ]
        
        title_text = title.text.strip().replace("\n", " ")
        title_text = re.sub(r"\[\s*|\s*\]", "", title.text.strip().replace("\n", " "))

        sliced_content = preprocessor.merge_numbered_lines(sliced_content)

        return {"title": title_text, "case_text": sliced_content}
    
    except requests.exceptions.RequestException as req_err:
        print(f"Network error: {str(req_err)}")
        return None
    except Exception as e:
        print(f"Error in scrape_court_case: {str(e)}")
        return None
    

class File(db.Model):
    __tablename__ = "file"
    
    # Define columns in the database table
    id = db.Column(db.Integer, primary_key=True)    # Unique ID for each file
    file_name = db.Column(db.String, nullable=False)    # Name of the file
    file_orig_text = db.Column(db.String, nullable=False)   # Original file text
    file_text = db.Column(db.String, nullable=False)    # Processed file text
    file_has_summ = db.Column(db.Integer, nullable=False, default=int(0))  # Indicator for whether the file has a summary (0 = No, 1 = Yes)
    file_facts = db.Column(db.String, nullable=False)   # Facts extracted from the file
    file_issues = db.Column(db.String, nullable=False)  # Issues extracted from the file
    file_rulings = db.Column(db.String, nullable=False) # Rulings extracted from the file
    file_content = db.Column(db.LargeBinary)    # Binary content of the file

    def to_json(self):
        """
        Converts the File object to a JSON-compatible dictionary.

        Encodes the binary file content to a Base64 string to ensure 
        compatibility with JSON format.

        Returns:
            dict: A dictionary containing the file's data, including:
                  - id: Unique ID
                  - file_name: Name of the file
                  - file_orig_text: Original file text
                  - file_text: Processed file text
                  - file_summary: Indicates if a summary exists
                  - file_facts: Extracted facts
                  - file_issues: Extracted issues
                  - file_rulings: Extracted rulings
                  - file_content: Base64-encoded binary content
        """
        return {
            "id": self.id,
            "file_name": self.file_name,
            "file_orig_text": self.file_orig_text,
            "file_text": self.file_text,
            "file_summary":self.file_has_summ,
            "file_facts":self.file_facts,
            "file_issues":self.file_issues,
            "file_rulings":self.file_rulings,
            "file_content": base64.b64encode(self.file_content).decode('utf-8') if self.file_content else None,
        }


@app.route("/get-files", methods=["GET"])
def get_files():
    """
    Description:
    Retrieves all file entries from the database and returns them in JSON format.

    Parameters: None

    Returns:
    - JSON: A JSON array of files, where each file is represented as a dictionary.
    """
    files = File.query.all()
    result = [file.to_json() for file in files]

    return jsonify(result)


@app.route("/send-file", methods=["POST"])
def send_file():
    """
    Description:
    Processes a court case from a provided link, saves its text content to a file,
    stores the file in the database, and deletes the temporary file.

    Parameters: None (expects JSON body with "link" field)

    Returns:
    - JSON: A JSON message indicating success and the file name.
    - JSON: Error messages if any part of the process fails (400 or 500 status).
    """

    try:

        if request.method == "POST":
            data = request.json
            court_case_content = data.get("content")
            print(court_case_content)
            court_case_title = data.get("title")[:-4]
            court_case_content = preprocessor.merge_numbered_lines(court_case_content)

            if not court_case_content:
                return jsonify({"error": "No court case content provided"}), 400

            txt_file_name = "test.txt"

            try:
                # Writing the court case text to a .txt file
                with open(txt_file_name, "w", encoding="utf-8") as f:
                    f.write(court_case_content)

                # Reading the file content for storage
                with open(txt_file_name, "rb") as f:
                    file_content = f.read()

            except IOError as e:
                return jsonify({"error": "File handling error: " + str(e)}), 500

            # Uploading the file to the database
            try:
                upload = File(
                    file_name=court_case_title,
                    file_text=court_case_content,
                    file_orig_text=court_case_content,
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
                # Get the file ID after committing
                file_id = upload.id

            except OSError as e:
                return jsonify({"error": "File deletion error: " + str(e)}), 500

            return jsonify({"msg": "successful", "file": txt_file_name})

    except Exception as e:
        print(e)
        db.session.rollback()
        return (
            jsonify({"error": "An unexpected error occurred: " + str(e)}),
            500,
        )
    
        
@app.route("/send-file-link", methods=["POST"])
def send_file_link():
    """
    Description:
    Processes a court case from a provided link, saves its text content to a file,
    stores the file in the database, and deletes the temporary file.

    Parameters: None (expects JSON body with "link" field)

    Returns:
    - JSON: A JSON message indicating success and the file name.
    - JSON: Error messages if any part of the process fails (400 or 500 status).
    """
    import re

    try:
        if request.method == "POST":
            data = request.json
            court_case_link = data.get("link")
            print(court_case_link)
            court_case = scrape_court_case(court_case_link)
            court_case_text = preprocessor.merge_numbered_lines(court_case["case_text"])

            if not court_case_link:
                return jsonify({"error": "No court case link provided"}), 400

            if (
                not court_case
                or "case_text" not in court_case
            ):
                return jsonify({"error": "Invalid court case data"}), 400

            case_title = court_case["title"]
            
            # Sanitize the case title to create a valid file name
            case_title = re.sub(
                r'[\\/*?:"<>|]', "-", case_title
            )  # Replace invalid characters with '-'
            case_title = re.sub(
                r"[\.,]", "", case_title
            )  # Optionally remove commas and periods
            
            # Limit the filename length (for example, to 150 characters)
            max_length = 150
            txt_case_title = (
                case_title[:max_length]
                if len(case_title) > max_length
                else case_title
            )
            
            txt_file_name = txt_case_title
            
            try:
                # Writing the court case text to a .txt file
                with open(txt_file_name, "w", encoding="utf-8") as f:
                    f.write(court_case_text)

                # Reading the file content for storage
                with open(txt_file_name, "rb") as f:
                    file_content = f.read()

            except IOError as e:
                return jsonify({"error": "File handling error: " + str(e)}), 500

            # Uploading the file to the database
            try:
                upload = File(
                    file_name=txt_file_name,
                    file_text=court_case["case_text"],
                    file_orig_text=court_case["case_text"],
                    file_content=file_content,
                )
                db.session.add(upload)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                return jsonify({"error": "Database error: " + str(e)}), 500

            # Optionally delete the file after saving to the database
            try:
                os.remove(txt_file_name)

                # Get the file ID after committing
                file_id = upload.id

            except OSError as e:
                return jsonify({"error": "File deletion error: " + str(e)}), 500

            return jsonify({"msg": "successful", "file": txt_file_name})

    except Exception as e:
        print(e)
        db.session.rollback()
        return (
            jsonify({"error": "An unexpected error occurred: " + str(e)}),
            500,
        )


@app.route("/delete-file/<int:id>", methods=["DELETE"])
def delete_file(id):
    """
    Description:
    Deletes a specified file entry from the database based on its ID.

    Parameters:
    - id (int): The ID of the file to delete.

    Returns:
    - JSON: A success message if the file was deleted.
    - JSON: An error message if the file was not found or if deletion failed.
    """
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
    """
    Description:
    Updates an existing file's name, text, and content in the database.

    Parameters:
    - id (int): The ID of the file to update.

    Returns:
    - JSON: The updated file information in JSON format.
    - JSON: Error messages if the file is not found or if the update failed.
    """
    try:
        file = db.session.get(File, id)
        if file is None:
            return jsonify({"error": "File not found"}), 404

        data = request.json
        file.file_name = data.get("file_name", file.file_name)
        file.file_text = data.get("file_text", file.file_text)
        file.file_has_summ = 0

        if "file_content" in data:
            file.file_content = bytes(data["file_content"], "utf-8")

        db.session.commit()

        return jsonify(file.to_json()), 200
    except Exception as e:
        print("error:", e)
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/get-summarized/<int:id>", methods=["POST"])
def get_summarized(id):
    """
    Description:
    Retrieves and preprocesses the text of a specified court case file using custom preprocessing,
    such as cleaning and tokenizing paragraphs.

    Parameters:
    - id (int): The ID of the court case file.

    Returns:
    - JSON: The cleaned and tokenized paragraphs of the case text.
    - JSON: An error message if preprocessing fails or if the file is not found.
    """
    try:
        # Verify if there are court case
        file = db.session.get(File, id)
        if file is None:
            return jsonify({"error": "Court case not found"}), 404
        
        # Default value is set to none
        summarize_case = {"title": file.file_name, "facts":"", "issues":"", "rulings":""}
        
        # Create a summary if there are no summary
        if file.file_has_summ == 0:
            court_case_text = file.file_text

            if not court_case_text:
                return jsonify({"error": "No case text provided"}), 400

            # Preprocessing and segmentation
            cleaned_text = preprocessor.remove_unnecesary_char(court_case_text)
            segmented_paragraph = preprocessor.segment_paragraph(cleaned_text, court_case_text)
            
            segmentation = TopicSegmentation()


            predicted_labels = segmentation.sequence_classification(
                segmented_paragraph, threshold=0.8
            )
            segmentation_output = segmentation.label_mapping(predicted_labels)

            # Summarization
            lsa = LSA(segmentation_output)
            generated_summary = lsa.create_summary()

            # Ensure generated summary contains required keys
            summarize_case["facts"] = generated_summary.get("facts", "No facts available")
            summarize_case["issues"] = generated_summary.get("issues", "No issues available")
            summarize_case["rulings"] = generated_summary.get("rulings", "No rulings available")

            print("Generated Summary:", summarize_case, "\n\n")
            
            # Update and commit summary to the database
            file.file_has_summ = 1 # 1 = True (summary exists)
            file.file_facts = summarize_case["facts"]
            file.file_issues = summarize_case["issues"]
            file.file_rulings = summarize_case["rulings"]
            db.session.commit()
        else:
            # Retrieve existing summary
            summarize_case["facts"] = file.file_facts 
            summarize_case["issues"] = file.file_issues
            summarize_case["rulings"] = file.file_rulings
        
        return jsonify(summarize_case), 200

    except Exception as e:
        print("Error during summarizing:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/get-preprocess/<int:id>", methods=["POST"])
def get_preprocess(id):
    """
    Description:
    Retrieves and preprocesses the text of a specified court case file using custom preprocessing,
    such as cleaning and tokenizing paragraphs.

    Parameters:
    - id (int): The ID of the court case file.

    Returns:
    - JSON: The cleaned and tokenized paragraphs of the case text.
    - JSON: An error message if preprocessing fails or if the file is not found.
    """
    try:

        file = db.session.get(File, id)
        if file is None:
            return jsonify({"error": "Court case not found"}), 404

        court_case_text = file.file_text

        if not court_case_text:
            return jsonify({"error": "No case text provided"}), 400


        cleaned_text = preprocessor.remove_unnecesary_char(court_case_text)
        doc = nlp(cleaned_text)
        filtered_words = " ".join([token.text for token in doc if token.pos_ in ['NOUN', 'VERB', 'ADJ']])

        return jsonify({"preprocess": filtered_words}), 200
        # print("segmented paragraph", segmented_paragraph)

    except Exception as e:
        print("Error during preprocess:", e)
        return jsonify({"error": str(e)}), 500





with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
