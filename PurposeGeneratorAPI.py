from flask import Flask, request, jsonify
import google.generativeai as genai


app = Flask(__name__)
with open("key.txt", "r") as f:   
    API_KEY  = str(f.read().strip())
print(API_KEY)
genai.configure(api_key = API_KEY)
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

@app.route("/generate", methods = ["POST"])
def purposeGenerate():
    try:
        data = request.get_json()
        question = f"What is the purpose of {data}? Write in simple terms using three sentences."
        response = get_gemini_response(question)
        texts = []
        for resp in response:
            texts.append(resp.text)
        output = ' '.join(texts).strip().replace("\n", "")
        return jsonify({"output ": str(output)})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":

    app.run(debug=True)