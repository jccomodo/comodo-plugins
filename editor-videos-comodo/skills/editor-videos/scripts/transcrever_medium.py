import sys,json
from faster_whisper import WhisperModel
m=WhisperModel("medium",device="cpu",compute_type="int8")
segs,info=m.transcribe(sys.argv[1],language="pt",word_timestamps=True,vad_filter=False,initial_prompt="Cômodo, planejados, móveis planejados, lojistas, projetistas.")
out=[]
for s in segs:
    out.append({"start":s.start,"end":s.end,"text":s.text.strip(),"words":[{"w":x.word.strip(),"s":x.start,"e":x.end} for x in s.words]})
json.dump(out,open(sys.argv[2],"w",encoding="utf-8"),ensure_ascii=False,indent=1)
for o in out: print(f'[{o["start"]:6.2f}-{o["end"]:6.2f}] {o["text"]}')

