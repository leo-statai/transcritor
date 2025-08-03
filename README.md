# Sistema de Transcrição de Áudio

Sistema minimalista para transcrever arquivos de áudio e vídeo para texto usando OpenAI Whisper.

## 🚀 Funcionalidades

- ✅ Suporte a múltiplos formatos de vídeo (MP4, AVI, MKV, MOV, FLV, WMV)
- ✅ Suporte a múltiplos formatos de áudio (MP3, WAV, FLAC, AAC, OGG, M4A)
- ✅ Extração automática de áudio de vídeos
- ✅ Transcrição com timestamps opcionais
- ✅ Múltiplos tamanhos de modelo Whisper (tiny, base, small, medium, large)
- ✅ Detecção automática de idioma
- ✅ Interface de linha de comando simples
- ✅ Tratamento robusto de erros

## 📋 Pré-requisitos

- Python 3.8+ (testado com Python 3.13)
- FFmpeg instalado no sistema

### Instalando FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Arch Linux:**
```bash
sudo pacman -S ffmpeg
```

## 🛠️ Instalação

1. **Clone ou baixe o projeto**
```bash
git clone <repo_url>
cd transcritor
```

2. **Crie um ambiente virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

## 🎯 Como usar

### Uso básico

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Transcrever um arquivo de vídeo
python transcriber.py video.mp4

# Transcrever um arquivo de áudio
python transcriber.py audio.mp3
```

### Opções avançadas

```bash
# Especificar arquivo de saída
python transcriber.py video.mp4 -o minha_transcricao.txt

# Usar modelo maior (melhor qualidade)
python transcriber.py audio.wav --model large

# Especificar idioma
python transcriber.py video.mp4 --language pt

# Transcrição sem timestamps
python transcriber.py audio.mp3 --no-timestamps

# Combinar opções
python transcriber.py video.mp4 --model medium --language pt -o resultado.txt
```

### Opções disponíveis

- `--model`: Tamanho do modelo Whisper
  - `tiny`: Mais rápido, menor qualidade (~39M parâmetros)
  - `base`: Balanceado (padrão) (~74M parâmetros)
  - `small`: Boa qualidade (~244M parâmetros)
  - `medium`: Alta qualidade (~769M parâmetros)
  - `large`: Máxima qualidade (~1550M parâmetros)

- `--language`: Código do idioma (ex: `pt`, `en`, `es`, `fr`)
- `--no-timestamps`: Remove timestamps da transcrição
- `-o, --output`: Especifica arquivo de saída

## 📊 Formatos suportados

### Vídeo
- MP4, AVI, MKV, MOV, FLV, WMV

### Áudio
- MP3, WAV, FLAC, AAC, OGG, M4A

## 📄 Formato de saída

A transcrição é salva em formato TXT com a seguinte estrutura:

```
# Transcrição de Áudio
# Modelo: base
# Idioma: pt
# Duração: [00:05:30]
#

[00:00:00] Olá, bem-vindos ao nosso podcast.
[00:00:05] Hoje vamos falar sobre tecnologia.
[00:00:10] O tema é bastante interessante...
```

## 🧪 Executar testes

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar testes
python -m unittest tests.test_transcriber -v
```

## ⚡ Dicas de performance

1. **Tamanho do modelo**: Use `tiny` ou `base` para testes rápidos, `medium` ou `large` para qualidade máxima
2. **Arquivos grandes**: O sistema processa automaticamente em chunks para otimizar memória
3. **Qualidade de áudio**: Áudio limpo e claro resulta em melhor transcrição
4. **Idioma**: Especificar o idioma melhora a precisão

## ❗ Solução de problemas

### Erro: FFmpeg não encontrado
```bash
# Instale o FFmpeg conforme instruções acima
which ffmpeg  # Verificar se está instalado
```

### Erro: Memória insuficiente
- Use um modelo menor (`tiny` ou `base`)
- Processe arquivos menores
- Feche outros programas

### Erro: Formato não suportado
- Verifique se o arquivo está nos formatos suportados
- Converta o arquivo usando FFmpeg se necessário

### Erro: Arquivo não encontrado
- Verifique o caminho do arquivo
- Use caminhos absolutos se necessário

## 📁 Estrutura do projeto

```
transcritor/
├── src/
│   ├── __init__.py
│   ├── main.py              # Interface CLI
│   ├── audio_extractor.py   # Extração de áudio
│   ├── transcriber.py       # Motor de transcrição
│   └── utils.py             # Funções auxiliares
├── tests/
│   ├── __init__.py
│   └── test_transcriber.py  # Testes unitários
├── venv/                    # Ambiente virtual
├── transcriber.py           # Script principal
├── requirements.txt         # Dependências
├── setup.py                # Configuração do pacote
├── .gitignore              # Arquivos ignorados
└── README.md               # Este arquivo
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙏 Agradecimentos

- [OpenAI Whisper](https://github.com/openai/whisper) - Motor de transcrição
- [FFmpeg](https://ffmpeg.org/) - Processamento de áudio/vídeo