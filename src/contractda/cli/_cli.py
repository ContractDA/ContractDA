import cmd

class ContractDACmdShell(cmd.Cmd):
    intro = "ContractDA: Design Automation Tools for Contract-base Designs"
    prompt = "contractda > "
    file = None

    def do_helloworld(self, arg):
        "Say hello"
        print("Hello")

        