import subprocess
import tkinter as tk
import customtkinter as ctk
from subprocess import CalledProcessError


class RetriveConnectedWifiPasswordApp:
    def __init__(self) -> None:
        self.root = ctk.CTk()

        self.app_width = 700
        self.app_height = 680

        self.color1 = "#D2DE32"
        self.color2 = "#FFFFDD"
        self.bgcolor = "#61A3BA"

        # icon_path = "icons8-wifi-96.ico"
        # self.root.iconbitmap(icon_path)
        self.screenwidth = self.root.winfo_screenwidth()
        self.screenheight = self.root.winfo_screenheight()
        self.x = (self.screenwidth // 2) - (self.app_width // 2) + 120
        self.y = (self.screenheight // 2) - (self.app_height // 2) - 38

        self.root.title("Get Connected Wi-Fi Password")
        self.root.geometry(f"{self.app_width}x{self.app_height}+{self.x}+{self.y}")
        self.root.resizable(False, False)
        self.root.configure(bg=self.bgcolor)

        self.header = None
        self.scrollable = None
        self.letsGoButton = None

        self.resultLabel = None
        self.data = {}

    @staticmethod
    def get_password(name: str) -> str:
        try:
            command = f'netsh wlan show profiles name="{name}" key=clear | findstr Key'
            output = (
                subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                .decode("utf-8")
                .strip()
            )

            if "Key Content" in output:
                password = output.split(":")[1].strip()
                # print(f"Password for '{name}': {password}")
                return password
            else:
                # print(f"No password found for '{name}'")
                return None

        except CalledProcessError as e:
            print(f"Error: {e}")
            print(f"Command output: {e.output.decode('utf-8').strip()}")

    @staticmethod
    def get_all_connected_wifi_profile() -> list[str]:
        all_wifis = subprocess.check_output(
            ["netsh", "wlan", "show", "profiles"]
        ).decode("utf-8")
        profiles = [
            line.split(":")[1].strip()
            for line in all_wifis.split("\n")
            if "All User Profile" in line
        ]
        return profiles

    def letsGoButtonEvent(self):
        self.letsGoButton.configure(state="disabled")
        all_profiles = self.get_all_connected_wifi_profile()

        labelHeader = ctk.CTkLabel(
            self.scrollable,
            text="Connected Networks",
            font=("Arial", 18, "bold"),
            # bg_color="#555555",
            # text_color="#FFFFFF",
            width=200,
        )
        labelHeader.pack(side="top", pady=(8, 10))

        for i, network in enumerate(all_profiles):
            password = self.get_password(network)

            # write data
            self.data[network] = password
            
            if password == None:
                password = str(password).lower()
            else:
                password = "[" + password + "]"
            text = network.rjust(40, " ") + " --> " + password.ljust(40, " ")


            container = ctk.CTkFrame(self.scrollable)
            if i + 1 == len(all_profiles):
                container.pack(side="top", pady=(0, 16))
            else:
                container.pack(side="top")

            number = ctk.CTkLabel(
                container,
                text=f"{(str(i+1) + ' ').rjust(5, ' ')}",
                font=("Consolas", 11, "bold"),
                bg_color="#555555",
            )
            number.pack(side="left", pady=(0, 2), padx=(0, 2))

            label = ctk.CTkLabel(
                container,
                text=text,
                font=("Consolas", 11),
                bg_color="#555555",
                width=200,
            )
            label.pack(side="left", pady=(0, 2))

            self.root.update()

    def initialize(self):
        self.header = ctk.CTkLabel(
            self.root,
            text="Get Connected Wi-Fi Password",
            font=("Arial", 26, "bold"),
            # bg_color=self.color1,
            # text_color="#000000",
            width=self.screenwidth,
            height=30,
        )
        self.header.pack(pady=(24, 0))

        self.scrollable = ctk.CTkScrollableFrame(
            self.root, width=self.app_width - 100, height=500
        )
        self.scrollable.pack(pady=(24, 0))

        self.letsGoButton = ctk.CTkButton(
            self.root,
            text="Let's go",
            command=self.letsGoButtonEvent,
            font=("Arial", 12, "bold"),
            width=150,
            height=34,
            corner_radius=18,
        )
        self.letsGoButton.pack(side="top", pady=(24, 0))

    def run(self):
        self.initialize()
        self.root.mainloop()


if __name__ == "__main__":
    app = RetriveConnectedWifiPasswordApp()
    app.run()
