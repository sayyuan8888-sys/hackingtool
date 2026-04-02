import os

from core import HackingTool, HackingToolsCollection, console


class AnonymouslySurf(HackingTool):
    TITLE = "Anonymously Surf"
    DESCRIPTION = (
        "It automatically overwrites the RAM when the system shuts down\n"
        "and also changes your IP address."
    )
    # Bug 28 fix: was "cd kali-anonsurf && ./installer.sh && cd .. && sudo rm -r kali-anonsurf"
    # Deleting the source on install means there is no retry if install fails.
    # Now kept in a separate step so failure does not destroy the source.
    INSTALL_COMMANDS = [
        "git clone https://github.com/Und3rf10w/kali-anonsurf.git",
        "cd kali-anonsurf && sudo ./installer.sh",
    ]
    RUN_COMMANDS = ["sudo anonsurf start"]
    PROJECT_URL = "https://github.com/Und3rf10w/kali-anonsurf"
    SUPPORTED_OS = ["linux"]

    def __init__(self):
        super().__init__([("Stop", self.stop)])

    def stop(self):
        import subprocess
        console.print("[bold magenta]Stopping Anonsurf...[/bold magenta]")
        subprocess.run(["sudo", "anonsurf", "stop"])


class Multitor(HackingTool):
    TITLE = "Multitor"
    DESCRIPTION = "How to stay in multi places at the same time."
    INSTALL_COMMANDS = [
        "git clone https://github.com/trimstray/multitor.git",
        "cd multitor && sudo bash setup.sh install",
    ]
    RUN_COMMANDS = [
        "multitor --init 2 --user debian-tor --socks-port 9000 --control-port 9900 --proxy privoxy --haproxy"
    ]
    PROJECT_URL = "https://github.com/trimstray/multitor"
    SUPPORTED_OS = ["linux"]

    def __init__(self):
        super().__init__(runnable=False)


class Nipe(HackingTool):
    TITLE = "Nipe (Tor Default Gateway)"
    DESCRIPTION = (
        "Makes the Tor network your default gateway, routing all traffic through Tor.\n"
        "Usage: sudo perl nipe.pl start"
    )
    INSTALL_COMMANDS = [
        "git clone https://github.com/htrgouvea/nipe.git",
        "cd nipe && sudo cpan install Try::Tiny Config::Simple JSON",
        "cd nipe && sudo perl nipe.pl install",
    ]
    RUN_COMMANDS = ["cd nipe && sudo perl nipe.pl start"]
    PROJECT_URL = "https://github.com/htrgouvea/nipe"
    SUPPORTED_OS = ["linux"]
    REQUIRES_ROOT = True
    TAGS = ["anonymity", "tor", "privacy"]

    def __init__(self):
        super().__init__([("Status", self.status), ("Stop", self.stop)])

    def status(self):
        import subprocess
        from config import get_tools_dir
        console.print("[bold magenta]Checking Nipe status...[/bold magenta]")
        subprocess.run(
            ["sudo", "perl", "nipe.pl", "status"],
            cwd=str(get_tools_dir() / "nipe"),
        )

    def stop(self):
        import subprocess
        from config import get_tools_dir
        console.print("[bold magenta]Stopping Nipe...[/bold magenta]")
        subprocess.run(
            ["sudo", "perl", "nipe.pl", "stop"],
            cwd=str(get_tools_dir() / "nipe"),
        )


class ProxyChainsNG(HackingTool):
    TITLE = "ProxyChains-ng (Proxy Redirector)"
    DESCRIPTION = (
        "Redirect TCP connections through SOCKS4a/5 or HTTP proxies.\n"
        "Usage: proxychains4 <command>"
    )
    INSTALL_COMMANDS = [
        "git clone https://github.com/rofl0r/proxychains-ng.git",
        "cd proxychains-ng && ./configure --prefix=/usr --sysconfdir=/etc && make && sudo make install && sudo make install-config",
    ]
    RUN_COMMANDS = ["proxychains4 --help"]
    PROJECT_URL = "https://github.com/rofl0r/proxychains-ng"
    SUPPORTED_OS = ["linux", "macos"]
    TAGS = ["anonymity", "proxy", "privacy"]

    def __init__(self):
        super().__init__(runnable=False)


class OnionShare(HackingTool):
    TITLE = "OnionShare (Secure File Sharing over Tor)"
    DESCRIPTION = (
        "Securely and anonymously share files, host websites, and chat\n"
        "using the Tor network.\n"
        "Usage: onionshare-cli --help"
    )
    INSTALL_COMMANDS = ["pip install --user onionshare-cli"]
    RUN_COMMANDS = ["onionshare-cli --help"]
    PROJECT_URL = "https://github.com/onionshare/onionshare"
    SUPPORTED_OS = ["linux", "macos"]
    TAGS = ["anonymity", "tor", "file-sharing", "dark-web"]


class AnonSurfTools(HackingToolsCollection):
    TITLE = "Anonymously Hiding Tools"
    TOOLS = [
        AnonymouslySurf(),
        Multitor(),
        Nipe(),
        ProxyChainsNG(),
        OnionShare(),
    ]


if __name__ == "__main__":
    tools = AnonSurfTools()
    tools.show_options()
