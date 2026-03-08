import os
import json
import subprocess
import tempfile
from flask import Flask, render_template, request, jsonify, send_file, after_this_request

app = Flask(__name__)

# Configuration
DOWNLOAD_FOLDER = tempfile.mkdtemp()
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# Node path for yt-dlp (required for YouTube extraction)
NODE_PATH = '/home/r/.nvm/versions/node/v24.14.0/bin/node'

def get_video_info(url):
    """Extract video information using yt-dlp"""
    try:
        cmd = [
            'yt-dlp',
            '--dump-json',
            '--no-download',
            '--no-playlist',
            '--no-warnings',
            '--js-runtimes', f'node:{NODE_PATH}',
            '--',
            url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            return None, result.stderr

        data = json.loads(result.stdout)

        info = {
            'title': data.get('title', 'Unknown'),
            'thumbnail': data.get('thumbnail', ''),
            'duration': data.get('duration', 0),
            'url': url,
            'id': data.get('id', '')
        }

        # Format duration
        duration_sec = info['duration']
        minutes = duration_sec // 60
        seconds = duration_sec % 60
        info['duration_formatted'] = f"{minutes}:{seconds:02d}"

        return info, None

    except Exception as e:
        return None, str(e)

def download_media(url, format_type, quality='720p'):
    """Download video or audio"""
    try:
        filename = None

        if format_type == 'mp3':
            cmd = [
                'yt-dlp',
                '-x',
                '--audio-format', 'mp3',
                '--postprocessor-args', 'ffmpeg:-b:a 192k',
                '-f', 'bestaudio[ext=m4a]/bestaudio',
                '--no-warnings',
                '--js-runtimes', f'node:{NODE_PATH}',
                '-o', os.path.join(app.config['DOWNLOAD_FOLDER'], 'download.%(ext)s'),
                '--',
                url
            ]
        else:
            # Video quality mapping - use combined format
            quality_map = {
                '1080p': '137+140',
                '720p': '136+140',
                '480p': '135+140',
                '360p': '134+140'
            }
            format_code = quality_map.get(quality, '136+140')

            cmd = [
                'yt-dlp',
                '-f', format_code,
                '--no-warnings',
                '--js-runtimes', f'node:{NODE_PATH}',
                '-o', os.path.join(app.config['DOWNLOAD_FOLDER'], 'download.%(ext)s'),
                '--',
                url
            ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode != 0:
            return None, result.stderr

        # Find the downloaded file
        for f in os.listdir(app.config['DOWNLOAD_FOLDER']):
            if f.startswith('download.'):
                filename = os.path.join(app.config['DOWNLOAD_FOLDER'], f)
                break

        return filename, None

    except Exception as e:
        return None, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    url = data.get('url', '').strip()

    if not url:
        return jsonify({'error': 'Please enter a YouTube URL'}), 400

    # Basic URL validation
    if 'youtube.com' not in url and 'youtu.be' not in url:
        return jsonify({'error': 'Please enter a valid YouTube URL'}), 400

    info, error = get_video_info(url)

    if error:
        return jsonify({'error': f'Error: {error}'}), 400

    return jsonify({'success': True, 'video': info})

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url', '').strip()
    format_type = data.get('format', 'mp4')
    quality = data.get('quality', '720p')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    filename, error = download_media(url, format_type, quality)

    if error:
        return jsonify({'error': f'Download error: {error}'}), 400

    if not filename or not os.path.exists(filename):
        return jsonify({'error': 'Download failed'}), 400

    @after_this_request
    def remove_file(response):
        try:
            if os.path.exists(filename):
                os.remove(filename)
        except Exception:
            pass
        return response

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
