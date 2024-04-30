import soundfile as sf
import matplotlib.pyplot as plt


class SigfoxFrame:

    def __init__(self, ul_pr=None, ft=None, ul_phy_content=None, ul_container=None,
                 ul_crc=None, ul_auth=None, ul_payload=None, id=None, mc=None, rep=None,
                 bf=None, li=None, ul_message_content=None):

        self.ul_pr = ul_pr # 19 bits
        self.ft = ft # 13 bits
        self.ul_phy_content = ul_phy_content # 22 octets
        self.ul_container = ul_container # 20 octets
        self.ul_crc = ul_crc # 16 bits
        self.ul_auth = ul_auth # 2 octets
        self.ul_payload = ul_payload # 12 octets = message
        self.id = id # 32 bits
        self.mc = mc # 12 bits
        self.rep = rep # 1 bit
        self.bf = bf # 1 bit
        self.li = li # 2 bits
        self.ul_message_content = ul_message_content # 12 octets


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


