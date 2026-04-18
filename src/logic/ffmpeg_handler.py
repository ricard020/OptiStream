import subprocess
import re
import os
import time
import datetime

def get_video_duration(file_path):
    """Gets the duration of a video file in seconds."""
    cmd = ['ffmpeg', '-i', file_path]
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=startupinfo, encoding='utf-8', errors='ignore')
        match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2}\.\d{2})", result.stderr)
        if match:
            h, m, s = match.groups()
            return float(h)*3600 + float(m)*60 + float(s)
    except: pass
    return 0

def compress_video_task(inp, out, crf, on_progress, on_complete, on_error):
    """
    Runs the compression task. This function blocks until completion.
    
    Args:
        inp (str): Input file path.
        out (str): Output file path.
        crf (int): CRF value for quality.
        on_progress (callable): Callback(percent, eta_str)
        on_complete (callable): Callback(inp, out)
        on_error (callable): Callback(error_msg)
    """
    total_dur = get_video_duration(inp)
    
    cmd = ['ffmpeg', '-y', '-i', inp, '-vcodec', 'libx264', '-crf', str(crf), '-preset', 'medium', out]
    
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    start_time = time.time()
    
    try:
        # Use simple Popen
        process = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=startupinfo, encoding='utf-8', errors='replace', universal_newlines=True)
        
        while True:
            line = process.stderr.readline()
            if not line and process.poll() is not None:
                break
            
            if line and total_dur > 0:
                tm = re.search(r"time=(\d{2}):(\d{2}):(\d{2}\.\d{2})", line)
                if tm:
                    h, m, s = tm.groups()
                    cur_dur = float(h)*3600 + float(m)*60 + float(s)
                    perc = (cur_dur / total_dur) * 100
                    
                    elapsed = time.time() - start_time
                    if perc > 0:
                        rem_seconds = (elapsed / perc) * (100 - perc)
                        eta_str = str(datetime.timedelta(seconds=int(rem_seconds)))
                    else:
                        eta_str = "Calculando..."

                    if on_progress:
                        on_progress(perc, eta_str)

        if process.poll() == 0:
            if on_complete:
                on_complete(inp, out)
        else:
            if on_error:
                on_error("Error desconocido durante la compresión.")

    except Exception as e:
        if on_error:
            on_error(str(e))
