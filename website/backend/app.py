# =============================================================================
# Program Title: Legal Document Analysis Application
# Programmers: Nicholas Dela Torre
# Date Written: October 12, 2024
# Date Revised: October 16, 2024
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


from flask import Flask, request, jsonify, send_file
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
        title_element = doc.find_all("h3")

        if not title_element:
            raise ValueError("Title not found in the document")

        title = title_element[0]

        paragraphs = title.find_all("p")
        if not paragraphs:
            raise ValueError("No paragraphs found under title")

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

        new_content_text = ""
        for blockquote in content.find_all("blockquote"):
            prev_sibling = blockquote.find_previous_sibling()

            # Check if the previous sibling is a <p> tag
            if prev_sibling and prev_sibling.name == "p":

                prev_sibling.append(f" {blockquote.get_text()}")

                # Remove the blockquote after merging its content
                blockquote.extract()

                # Clean up text using regular expressions
                new_content_text = content.get_text()

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
        from Custom_Modules.Preprocess import preprocess
        preprocessor = preprocess(is_training=False)
        sliced_content = preprocessor.merge_numbered_lines(sliced_content)

        return {"title": title_text, "case_text": sliced_content}
    
    

    except requests.exceptions.RequestException as req_err:
        print(f"Network error: {str(req_err)}")
        return None
    except Exception as e:
        print(f"Error in scrape_court_case: {str(e)}")
        return None
    
def create_wordcloud():
    from wordcloud import WordCloud
    text = """
    A word cloud is a collection of words depicted in different sizes.
    The bigger and bolder the word appears, the more frequently it occurs in a dataset.
    This example demonstrates creating a word cloud using Python.
    """
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    output_path = "wordcloud_output.png"
    wordcloud.to_file(output_path)


app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


Base = declarative_base()


class File(db.Model):
    __tablename__ = "file"
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, nullable=False)
    file_text = db.Column(db.String, nullable=False)
    file_content = db.Column(db.LargeBinary)

    def to_json(self):
        return {
            "id": self.id,
            "file_name": self.file_name,
            "file_text": self.file_text,
            "file_content": str(self.file_content),
        }


@app.route("/hello")
def hello():
    """
    Description:
    A simple test endpoint to verify the server is running.

    Parameters: None

    Returns:
    - str: A "hello" message.
    """
    return "hello"


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
    import re

    try:

        if request.method == "POST":
            data = request.json
            court_case_link = data.get("content")
            print(court_case_link)
            court_case_title = data.get("title")[:-4]
            from Custom_Modules.Preprocess import preprocess
            preprocessor = preprocess(is_training=False)
            court_case_link = preprocessor.merge_numbered_lines(court_case_link)
            # print(court_case_link)

            if not court_case_link:
                return jsonify({"error": "No court case link provided"}), 400

            # court_case = scrape_court_case(court_case_link)

            # if (
            #     not court_case
            #     or "title" not in court_case
            #     or "case_text" not in court_case
            # ):
            #     return jsonify({"error": "Invalid court case data"}), 400

            # case_title = court_case["title"]

            # # Sanitize the case title to create a valid file name
            # case_title = re.sub(
            #     r'[\\/*?:"<>|]', "-", case_title
            # )  # Replace invalid characters with '-'
            # case_title = re.sub(
            #     r"[\.,]", "", case_title
            # )  # Optionally remove commas and periods

            # # Limit the filename length (for example, to 150 characters)
            # max_length = 150
            # txt_case_title = (
            #     case_title[:max_length]
            #     if len(case_title) > max_length
            #     else case_title
            # )

            txt_file_name = "test.txt"

            try:
                # Writing the court case text to a .txt file
                with open(txt_file_name, "w", encoding="utf-8") as f:
                    f.write(court_case_link)

                # Reading the file content for storage
                with open(txt_file_name, "rb") as f:
                    file_content = f.read()

            except IOError as e:
                return jsonify({"error": "File handling error: " + str(e)}), 500

            # Uploading the file to the database
            try:
                upload = File(
                    file_name=court_case_title,
                    file_text=court_case_link,
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
            from Custom_Modules.Preprocess import preprocess
            preprocessor = preprocess(is_training=False)
            court_case_link = preprocessor.merge_numbered_lines(court_case_link)
            # print(court_case_link)

            if not court_case_link:
                return jsonify({"error": "No court case link provided"}), 400

            court_case = scrape_court_case(court_case_link)
            

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
                    f.write(court_case_link)
                   
                    

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
                    file_content=file_content,
                )
                print("uploaded")

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

        if "file_content" in data:
            file.file_content = bytes(data["file_content"], "utf-8")

        db.session.commit()
        print("file:", file)

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
        from Custom_Modules.Preprocess import preprocess
        from Custom_Modules.TopicSegmentation import TopicSegmentation
        from Custom_Modules.LSA import LSA

        file = db.session.get(File, id)
        if file is None:
            return jsonify({"error": "Court case not found"}), 404

        court_case_text = file.file_text

        if not court_case_text:
            return jsonify({"error": "No case text provided"}), 400

        # summary = "TITLE:"+ "\n" + file.file_name+ "\n\n" + summarize_case(court_case_text)
        # print(summary)

        preprocessor = preprocess(is_training=False)

        cleaned_text = preprocessor.remove_unnecesary_char(court_case_text)
        segmented_paragraph = preprocessor.segment_paragraph(cleaned_text, court_case_text)
        
        segmentation = TopicSegmentation(model_path="77")


        predicted_labels = segmentation.sequence_classification(
            segmented_paragraph, threshold=0.8
        )
        segmentation_output = segmentation.label_mapping(predicted_labels)
        lsa = LSA(segmentation_output)
        summarize_case = lsa.create_summary()
        


        file = db.session.get(File, id)

        summary = "TITLE:" + "\n" + file.file_name + "\n\n" + summarize_case
        
        return jsonify({"summary": summary}), 200
        # print("segmented paragraph", segmented_paragraph)

        

    except Exception as e:
        print("Error during preprocess:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/wordcloud', methods=['GET'])
def serve_wordcloud():
    # Ensure the word cloud is generated
    create_wordcloud()

    # Path to the word cloud image
    image_path = "wordcloud_output.png"

    # Send the image to the client
    if os.path.exists(image_path):
        return send_file(image_path,download_name='logo.png', mimetype='image/png')  # Correct usage
    else:
        return {"error": "Image not found"}, 404


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
