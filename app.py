from flask import Flask, render_template, request
from fairseq.checkpoint_utils import load_model_ensemble_and_task_from_hf_hub
from fairseq.models.text_to_speech.hub_interface import TTSHubInterface
import IPython.display as ipd
import re

# Define a regular expression to match sentence-ending punctuation
SENTENCE_END_RE = re.compile(r'[.?!]\s+')

def add_sentence_end(text):
    # Add a period after each sentence-ending punctuation mark
    return SENTENCE_END_RE.sub('. ', text.strip()) + '.'


models, cfg, task = load_model_ensemble_and_task_from_hf_hub(
    "facebook/fastspeech2-en-ljspeech",
    arg_overrides={"vocoder": "hifigan", "fp16": False}
)
model = models[0]
TTSHubInterface.update_cfg_with_data_cfg(cfg, task.data_cfg)
generator = task.build_generator(models, cfg)

app = Flask(__name__)

@app.route('/')
def index():
    text = add_sentence_end(request.args.get('text', ''))
    audio_html = ''
    if text:
        sample = TTSHubInterface.get_model_input(task, text)
        wav, rate = TTSHubInterface.get_prediction(task, model, generator, sample)

        audio = ipd.Audio(wav, rate=rate)

        audio_html = audio._repr_html_()

        print(audio_html, ' <audio')
    
    return render_template('index.html', audio_html=audio_html, text=text)
