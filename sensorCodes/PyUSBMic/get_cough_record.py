import sounddevice as sd
import soundfile as sf

class RecordCough():
    def __init__(self):
        self.samplerate = 44100  # Hertz
        self.duration = 10  # seconds
        self.filename = 'cough_output.wav'

    def record_audio(self):
        print("Starting Audio Recording")
        mydata = sd.rec(int(self.samplerate * self.duration), samplerate=self.samplerate,
                channels=2, blocking=True)
        sf.write(self.filename, mydata, self.samplerate)
        print("Ending Audio Recording")







