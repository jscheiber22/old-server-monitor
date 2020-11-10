import tkinter as tk
from ethereum import Worker
from time import sleep


class Monitor:
    def __init__(self):
        # Fast and Slow mode TO DO: connect to button in GUI
        self.fastUpdate = False

        # Standard tkinter Setup
        self.window = tk.Tk()
        self.window.rowconfigure([0, 1, 2], minsize = 100, weight = 1)
        self.window.columnconfigure([0, 1, 2], minsize = 100, weight = 1)

        # Miner Defaults and Visible Setup
        self.minerTitle = tk.Label(master=self.window, text="Crypto Miner Stats:")
        self.minerTitle.grid(row=0, column=1, sticky='s')

        tk.Label(master=self.window, text="Current Hashrate:").grid(row=1, column=0, sticky='se')
        tk.Label(master=self.window, text="Average Hashrate:").grid(row=1, column=2, sticky='sw')

        # Have to separate .grid from variable setting bc later problems w nonetype and whatnot
        self.currHashLabel = tk.Label(master=self.window, text="0.0 MH/s")
        self.currHashLabel.grid(row=2, column=0)
        self.avgHashLabel = tk.Label(master=self.window, text="0.0 MH/s")
        self.avgHashLabel.grid(row=2, column=2)

        # Ethereum Library Setup
        self.eth = Worker("0x2E5Acdc5C6F1083c4d6127a6b41e6BDB24b6b8E0", "thotbox")

    def update(self):
        self.window.update()
        skipMiner = False
        minutes = 60

        while True:
            if not skipMiner:
                try:
                    if not self.eth.isActive():
                        self.minerTitle.configure(foreground="hot pink")
                    self.avgHashLabel.configure(text=str(self.eth.getAverageHashrate()) + " MH/s")
                    self.currHashLabel.configure(text=str(self.eth.getCurrentHashrate()) + " MH/s")
                except:
                    print("Miner is most likely broken. Altering color as notice and stopping miner updates.")
                    self.minerTitle.configure(foreground="hot pink")
                    skipMiner = True

            self.window.update() # Want update as often as possible
            if self.fastUpdate:
                for second in range(0, minutes * 0.1):
                    sleep(1) # 1 second per minutes * 0.1 (6)
                    self.window.update()
            else:
                for second in range(0, minutes * 3):
                    sleep(1)
                    self.window.update()
            self.window.update()

            if not skipMiner:
                self.eth.update()

if __name__ == "__main__":
    monitor = Monitor()
    monitor.update()
