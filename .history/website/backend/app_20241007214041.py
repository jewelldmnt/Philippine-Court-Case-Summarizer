from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pdfplumber
from sqlalchemy.orm import declarative_base

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

# Route to upload and process files
@app.route("/send-file", methods=["POST"])
def send_file():
    try:
        if request.method == "POST":
            for i in range(len(request.files)):
                file = request.files[f"file{i+1}"]  # Get the file from the request
                file_text = ""

                # Use pdfplumber to extract text from the PDF
                with pdfplumber.open(file) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        file_text += text  # Append the text of each page

                print("Extracted text from file: ", file_text)

                # Save the file information in the database
                upload = File(
                    file_name=file.filename,
                    file_text=file_text,
                    file_content=file.read()  # Read the binary content of the file
                )
                db.session.add(upload)
                db.session.commit()

            return jsonify({"msg": "successful"})
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
@app.route("/get-summarized", methods=["GET"])
def get_summarized():
    pass  # Summarize the submitted text

# Ensure tables are created
with app.app_context():
    db.create_all()

# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True)
