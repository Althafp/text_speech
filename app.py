from flask import Flask, render_template, request, send_file
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf
import os

app = Flask(__name__)

device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler_tts_mini_v0.1").to(device)
tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler_tts_mini_v0.1")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        prompt = request.form['prompt']
        description = "A female speaker with a slightly low-pitched voice delivers her words quite expressively, in a very confined sounding environment with clear audio quality. She speaks very fast."

        input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
        prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

        generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
        audio_arr = generation.cpu().numpy().squeeze()

        # Save audio to a temporary file
        audio_path = 'static/parler_tts_out.wav'
        sf.write(audio_path, audio_arr, model.config.sampling_rate)

        return render_template('home.html', audio_path=audio_path)
    return render_template('home.html', audio_path=None)

@app.route('/play_audio')
def play_audio():
    audio_path = request.args.get('audio_path', None)
    if audio_path and os.path.exists(audio_path):
        return send_file(audio_path, as_attachment=False)
    return "Audio file not found."

if __name__ == '__main__':
    app.run(debug=True)
