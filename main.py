import re
import subprocess
import os.path
import json


def get_extension(lines):
    regex = re.compile("Audio: (...)|$")
    for line in lines:
        extension = regex.findall(line)[0]
        if extension:
            return extension


def get_audio_file_name(video_file_name):
    ffprobe_call = subprocess.run(["ffprobe", video_file_name], capture_output=True)
    filename_without_extension = os.path.splitext(video_file_name)[0]
    ffprobe_output = ffprobe_call.stderr.decode("utf-8")
    audio_file_extension = "." + get_extension(ffprobe_output.splitlines())
    return filename_without_extension + audio_file_extension


def extract_audio(video_file_name, audio_file_name, audio_length=str(10 * 60)):
    subprocess.run(
        ["ffmpeg", "-y", "-i", video_file_name, "-vn", "-acodec", "copy", "-ss", "0", "-t", str(audio_length), audio_file_name])


filename = "file2.mkv"
audio_filename = get_audio_file_name(filename)
extract_audio(filename, audio_filename)

# testing
ffprobe_call = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,codec_type", "-of", "json", filename], capture_output=True)
streams = json.loads(ffprobe_call.stdout.decode("utf-8"))["streams"]
print(streams)
audio_extension = streams[1]["codec_name"]
print(audio_extension)

