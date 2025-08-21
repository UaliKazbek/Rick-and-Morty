
import os
from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types

API_KEY = "AIzaSyCscYelo1TzjoMDeLs1_N3FENBtf2aEWqk"

client = genai.Client(api_key=API_KEY)

app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/characters")
def characters():
    return render_template("characters.html")

@app.route("/episodes")
def episodes():
    return render_template("episodes.html")

@app.route("/locations")
def locations():
    return render_template("locations.html")

@app.route("/ai")
def ai():
    return render_template("ai.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message") # type: ignore

    model = "gemma-3n-e2b-it"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_message)],
        ),
    ]

    config = types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.9,
        max_output_tokens=300,
    )

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents, # type: ignore
        config=config,
    ):
        if chunk.text:
            response_text += chunk.text

    return jsonify({"reply": response_text})

if __name__ == "__main__":
    app.run(debug=True)


