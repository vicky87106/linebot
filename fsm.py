from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state1(self, event): #要去state1只要輸入go to state1就會到on_enter_state1
        text = event.message.text
        return text.lower() == "go to state1"

    def is_going_to_rice(self, event):
        text = event.message.text
        return (text.lower() == "y" )|(text.lower() == "n") 

    def on_enter_state1(self, event): #on_enter + state名稱
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state1")
        self.go_back()

    def on_exit_state1(self):
        print("Leaving state1")

    def on_enter_rice(self, event):
        print("I'm entering rice")
        reply_token = event.reply_token
        if (reply_token == "y"):
            send_text_message(reply_token, "施家火雞肉飯")
            self.go_back()
        elif (reply_token == "n"):
            send_text_message(reply_token, "黑工號")
            self.go_back()

    def on_exit_rice(self):
        print("Leaving rice")
