# main.py
from flask import Flask, render_template, request
from db_connection import pic

# Create a Flask app
app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET','POST'])
def upload():
    # Get the uploaded files from the request
    uploaded_files = request.files.getlist('image')

    # List to store file paths
    file_paths = []

    for uploaded_file in uploaded_files:
        # Save each file to a folder within the 'static' directory
        file_path = f"static/uploads/{uploaded_file.filename}"
        uploaded_file.save(file_path)

        # Append the file path to the list
        file_paths.append(file_path)

        # Insert the file path into MongoDB for each file
        pic.insert_one({'image_path': file_path})

    # Get all image paths from MongoDB
    image_data = pic.find()
    image_paths = [data['image_path'] for data in image_data]

    # Render the template with the image paths
    return render_template('index.html', image_paths=image_paths)



# Define the route for displaying uploaded images
@app.route('/display')
def display():
    image_data = pic.find()

    # Extract image paths from MongoDB documents
    image_paths = [data['image_path'] for data in image_data]

    # Print image paths for debugging
    print(image_paths)

    # Render the template with the image paths
    return render_template('display.html', image_paths=image_paths)


# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
