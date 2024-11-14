from app import create_app

app = create_app()

if __name__ == "__main__":
    #run on port 5001 since I have MySQL on port 5000
    app.run(debug=True, host="0.0.0.0", port=5001)
