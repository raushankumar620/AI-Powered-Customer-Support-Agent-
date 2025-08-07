# audio_utils.py
import requests
import os
from pydub import AudioSegment
import uuid
import logging

logger = logging.getLogger(__name__)

def download_audio(url, save_dir="temp_audio"):
    """Download audio from URL and save to local file"""
    try:
        os.makedirs(save_dir, exist_ok=True)
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            filename = f"{uuid.uuid4()}.mp3"
            filepath = os.path.join(save_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            logger.info(f"Downloaded audio to {filepath}")
            return filepath
        else:
            logger.error(f"Failed to download audio: HTTP {response.status_code}")
            raise Exception(f"Failed to download audio: HTTP {response.status_code}")
    except Exception as e:
        logger.error(f"Error downloading audio: {str(e)}")
        raise

def convert_mp3_to_wav(mp3_path):
    """Convert MP3 file to WAV format"""
    try:
        wav_path = mp3_path.replace(".mp3", ".wav")
        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(wav_path, format="wav")
        logger.info(f"Converted {mp3_path} to {wav_path}")
        return wav_path
    except Exception as e:
        logger.error(f"Error converting audio: {str(e)}")
        raise

def convert_audio_format(input_path, output_path, output_format="wav"):
    """Convert audio file to specified format"""
    try:
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format=output_format)
        return output_path
    except Exception as e:
        logger.error(f"Error converting audio format: {str(e)}")
        raise

def clean_temp_audio(save_dir="temp_audio"):
    """Clean up temporary audio files"""
    try:
        if os.path.exists(save_dir):
            for file in os.listdir(save_dir):
                file_path = os.path.join(save_dir, file)
                os.remove(file_path)
            logger.info(f"Cleaned up temporary files in {save_dir}")
    except Exception as e:
        logger.error(f"Error cleaning temp audio: {str(e)}")

def get_audio_duration(file_path):
    """Get duration of audio file in seconds"""
    try:
        audio = AudioSegment.from_file(file_path)
        return len(audio) / 1000.0  # Convert milliseconds to seconds
    except Exception as e:
        logger.error(f"Error getting audio duration: {str(e)}")
        return 0
