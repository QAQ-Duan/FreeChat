import pyaudio
import wave

CHUNK = 1024  # 每个缓冲区的帧数
FORMAT = pyaudio.paInt16  # 采样位数
CHANNELS = 1  # 单声道
RATE = 44100  # 采样频率

def record_audio(wave_out_path, record_second):
    """
    the function to record audio
    
    Args:
        wave_out_path: the path file saved
        record_second: how many seconds to record
    """
    p = pyaudio.PyAudio()  # 实例化对象
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)  # 打开流，传入响应参数
    wf = wave.open(wave_out_path, 'wb')  # 打开 wav 文件。
    wf.setnchannels(CHANNELS)  # 声道设置
    wf.setsampwidth(p.get_sample_size(FORMAT))  # 采样位数设置
    wf.setframerate(RATE)  # 采样频率设置

    for _ in range(0, int(RATE * record_second / CHUNK)):
        data = stream.read(CHUNK)
        wf.writeframes(data)  # 写入数据
    stream.stop_stream()  # 关闭流
    stream.close()
    p.terminate()
    wf.close()

def play_audio(wave_input_path):
    """
    The function to play audio

    Args:
        wave_input_path: the path where the audio to play is saved
    """
    p = pyaudio.PyAudio()  # 实例化
    wf = wave.open(wave_input_path, 'rb')  # 读 wav 文件
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)  # 读数据
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()  # 关闭资源
    stream.close()
    p.terminate()

if __name__ == "__main__":
    print("OK")

