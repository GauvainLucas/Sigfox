import soundfile as sf
import matplotlib.pyplot as plt


class SigfoxFrame:

    def __init__(self, ul_pr=None, ft=None, ul_phy_content=None, ul_container=None,
                 ul_crc=None, ul_auth=None, ul_payload=None, id=None, mc=None, rep=None,
                 bf=None, li=None, ul_message_content=None):

        self.ul_pr = ul_pr
        self.ft = ft
        self.ul_phy_content = ul_phy_content
        self.ul_container = ul_container
        self.ul_crc = ul_crc
        self.ul_auth = ul_auth
        self.ul_payload = ul_payload
        self.id = id
        self.mc = mc
        self.rep = rep
        self.bf = bf
        self.li = li
        self.ul_message_content = ul_message_content


if __name__ == "__main__":
    data, samplerate = sf.read("signal_sigfox.wav")
    print(f"Sample rate: {samplerate} Hz")
    print(f"Data shape: {data.shape}")

    # Plot the signal
    plt.plot(data)
    plt.xlabel("Time (samples)")
    plt.ylabel("Amplitude")
    plt.title("Sigfox Signal")
    plt.show()


