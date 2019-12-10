from transitions.extensions import GraphMachine

from utils import send_text_message

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    
    def is_going_to_choose(self, event): #吃甚麼?
        text = event.message.text
        return text.lower() == "eat"

    def on_enter_choose(self, event):
        print("I'm entering choose")
        reply_token = event.reply_token
        id = event.source.user_id
        send_text_message(reply_token, "要吃長榮路的嗎? y/n?")

    def is_going_to_happy(self, event): #吃長榮路
            text = event.message.text
            return text.lower() == "y"
    
    def on_enter_happy(self, event):
        print("I'm entering happy")
        reply_token = event.reply_token
        send_text_message(reply_token, "你今天開心嗎? y/n?")
    
    def is_going_to_dance(self, event): #不開心
            text = event.message.text
            return text.lower() == "n"

    def on_enter_dance(self,event):
        print("I'm entering dance")
        reply_token = event.reply_token
        send_text_message(reply_token, "那去舞春好好吃一波吧!!對面甜點聽說不錯~")
        self.go_back() #回到user 
    
    def is_going_to_box(self, event): #開心
            text = event.message.text
            return text.lower() == "y"
    
    def on_enter_box(self, event):
        print("I'm entering box")
        reply_token = event.reply_token
        send_text_message(reply_token, "想吃便當類的嗎? y/n?")
    
    def is_going_to_eye(self, event): #吃便當
            text = event.message.text
            return text.lower() == "y"
    
    def on_enter_eye(self,event):
        print("I'm entering eye")
        reply_token = event.reply_token
        send_text_message(reply_token, "那就吃目白吧!有機會遇到認識的人喔!XD")
        self.go_back() #回到user 
    
    def is_going_to_earn(self, event): #不吃便當
            text = event.message.text
            return text.lower() == "n"
    
    def on_enter_earn(self,event):
        print("I'm entering earn")
        reply_token = event.reply_token
        send_text_message(reply_token, "吃吃吃...饌前!肉羹還不錯")
        self.go_back() #回到user 
    
    def is_going_to_rice(self, event): #不吃長榮路
            text = event.message.text
            return text.lower() == "n"
    
    def on_enter_rice(self, event):
        print("I'm entering rice")
        reply_token = event.reply_token
        send_text_message(reply_token, "想吃飯類的嗎? y/n?")
    
    def is_going_to_chicken(self, event): #要吃飯
        text = event.message.text
        return text.lower() == "y"
    
    def on_enter_chicken(self,event):
        print("I'm entering chicken")
        reply_token = event.reply_token
        send_text_message(reply_token, "雙城烤雞飯~真的超好吃~\n特別是雞片飯...不過晚到就沒了喔!\n貼心提醒:只有中午有開喔!!\n\n施家火雞肉飯也不錯，傍晚郵局下的麻糬也很好吃!!")
        self.go_back() #chicken回到user   

    def is_going_to_dumpling(self, event): #不要吃飯
        text = event.message.text
        return text.lower() == "n"
    
    def on_enter_dumpling(self, event):
        print("I'm entering dumpling")
        reply_token = event.reply_token
        send_text_message(reply_token, "想吃餃子嗎? y/n?") 

    def is_going_to_eight_cloud(self, event): #要吃水餃
        text = event.message.text
        return text.lower() == "y"
    
    def on_enter_eight_cloud(self,event):
        print("I'm entering eight_cloud")
        reply_token = event.reply_token
        send_text_message(reply_token, "吃八方雲集吧~前陣子新出的雞肉鍋貼還不錯~")
        self.go_back() #回到user   
    
    def is_going_to_braised(self, event): #不要吃水餃
        text = event.message.text
        return text.lower() == "n"
    
    def on_enter_braised(self,event):
        print("I'm entering braised")
        reply_token = event.reply_token
        send_text_message(reply_token, "食神滷味...愛店!! 但晚上才開..人多會等有點久!")
        self.go_back() #回到user  

    def on_exit_chicken(self):
        print("Leaving chicken")

    def on_exit_eight_cloud(self):
        print("Leaving eight_cloud")
    
    def on_exit_braised(self):
        print("Leaving braised")


    def on_exit_rice(self,event):
        print("Leaving rice")
   
    def on_exit_choose(self,event):
        print("Leaving choose")
    
    def on_exit_dumpling(self,event):
        print("Leaving dumpling")

    

