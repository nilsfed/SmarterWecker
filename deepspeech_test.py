from deepspeech import Model
import scipy.io.wavfile as wav
import sys

def load_model(models, lm, trie):
    BEAM_WIDTH = 500
    LM_ALPHA = 0.75
    LM_BETA = 1.85

    ds = Model(models, BEAM_WIDTH)
    
    ds.enableDecoderWithLM(lm, trie, LM_ALPHA, LM_BETA)
   

    sample_rate = ds.sampleRate()
    

    return [ds, sample_rate]

models = sys.argv[1] 	#.pb
lm = sys.argv[2] 	# lm.binary
trie = sys.argv[3] 	# trie

model_retval = load_model(models, lm, trie)

fs, audio = wav.read(sys.argv[4])
print("sample rate wav file: ", fs)
print("sample rate model:", model_retval[1])

processed_data = model_retval[0].stt(audio)

print(processed_data)

with open('./tmp/data.txt', 'w') as f:

    f.write(processed_data)