// Narração com a voz do Daniel (ElevenLabs, voz "Daniel v4").
//
// Roteiro inteiro (um MP3 por "## CENA ..."; sem cabeçalhos = um MP3 só):
//   node narrar.js ROTEIRO.txt --saida PASTA [--style 0.5] [--stability 0.35] [--pular 1,2] [--so 3]
// Uma frase só, com o contexto antes/depois para manter a entonação (para emendar com emendar.py):
//   node narrar.js --frase "e eu acabei de ganhar." --antes "texto anterior" --depois "texto seguinte" --saida trecho.mp3 [--style 0] [--stability 0.5]
//
// Custo: cerca de 1 crédito ElevenLabs por caractere. O script mostra o total de caracteres.
const fs = require('fs');
const path = require('path');

// .env: COMODO_VIDEO_ENV, ou ~/Comodo-Videos-Daniel/.env (criado pelo setup), ou o .env dos podcasts
const os = require('os');
const envPath = [process.env.COMODO_VIDEO_ENV, path.join(os.homedir(), 'Comodo-Videos-Daniel', '.env'),
  path.join(os.homedir(), 'Claude', 'podcasts', '.env')].find((p) => p && fs.existsSync(p));
if (!envPath) { console.error('não achei o .env: rode o setup da skill'); process.exit(1); }
const env = {};
for (const l of fs.readFileSync(envPath, 'utf8').split(/\r?\n/)) {
  const m = l.match(/^\uFEFF?([A-Z0-9_]+)=(.*)$/);
  if (m) env[m[1]] = m[2].trim().replace(/^"|"$/g, '');
}
const key = env.ELEVENLABS_API_KEY, voice = env.ELEVENLABS_VOICE_A, model = env.ELEVENLABS_MODEL_A;
if (!key || !voice || !model) { console.error('faltam ELEVENLABS_API_KEY / _VOICE_A / _MODEL_A no .env'); process.exit(1); }

const arg = (n) => { const i = process.argv.indexOf(n); return i > 0 ? process.argv[i + 1] : null; };
let settings = env.ELEVENLABS_SETTINGS_A ? JSON.parse(env.ELEVENLABS_SETTINGS_A) : {};
if (arg('--style')) settings.style = Number(arg('--style'));
if (arg('--stability')) settings.stability = Number(arg('--stability'));
const saida = arg('--saida');
if (!saida) { console.error('informe --saida'); process.exit(1); }

async function tts(text, extra = {}) {
  const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voice}?output_format=mp3_44100_128`, {
    method: 'POST',
    headers: { 'xi-api-key': key, 'content-type': 'application/json' },
    body: JSON.stringify({ text, model_id: model, voice_settings: settings, ...extra }),
  });
  if (!r.ok) throw new Error(`${r.status} ${(await r.text()).slice(0, 300)}`);
  return Buffer.from(await r.arrayBuffer());
}

(async () => {
  console.log('voz', voice, 'modelo', model, 'ajustes', JSON.stringify(settings));
  if (arg('--frase')) {
    const extra = {};
    if (arg('--antes')) extra.previous_text = arg('--antes');
    if (arg('--depois')) extra.next_text = arg('--depois');
    fs.writeFileSync(saida, await tts(arg('--frase'), extra));
    console.log(`ok ${saida} (${arg('--frase').length} caracteres)`);
    return;
  }
  const arquivo = process.argv[2];
  const texto = fs.readFileSync(arquivo, 'utf8').replace(/^\uFEFF/, '');
  let cenas = texto.split(/^## /m).slice(1).map((b) => {
    const [cab, ...resto] = b.split('\n');
    return { id: cab.split('|')[0].replace(/CENA/i, '').trim(), texto: resto.join('\n').trim() };
  });
  if (!cenas.length) cenas = [{ id: '1', texto: texto.trim() }];
  const pular = new Set((arg('--pular') || '').split(',').filter(Boolean));
  const so = arg('--so') ? new Set(arg('--so').split(',')) : null;
  fs.mkdirSync(saida, { recursive: true });
  let total = 0;
  for (const [i, c] of cenas.entries()) {
    const nome = cenas.length === 1 ? 'narracao.mp3' : `cena_${String(i + 1).padStart(2, '0')}_${c.id}.mp3`;
    if (pular.has(c.id) || (so && !so.has(c.id))) { console.log('pulei', nome); continue; }
    fs.writeFileSync(path.join(saida, nome), await tts(c.texto));
    total += c.texto.length;
    console.log(`ok ${nome} (${c.texto.length} caracteres)`);
  }
  console.log(`total ${total} caracteres`);
})().catch((e) => { console.error('erro', e.message); process.exit(1); });
