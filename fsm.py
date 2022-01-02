from transitions.extensions import GraphMachine

from utils import (
    send_text_message, send_template_message, show_movie_thisweek,
    show_movie_intheaters, show_movie_leaderboard, show_movie_comingsoon
)

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_main_menu(self, event):
        text = event.message.text
        return text.lower() == "主選單" or text.lower() == "返回主選單"

    def on_enter_main_menu(self, event):
        #SwitchMenuTo("主選單", event)
        send_text_message(event, "歡迎使用我就爛好想看！")
        send_text_message(event, "請使用下方選單進行操作")

    def is_going_to_movie_menu(self, event):
        text = event.message.text
        return text.lower() == "電影選單" or text.lower() == "返回電影選單"

    def on_enter_movie_menu(self, event):
        #SwitchMenuTo("電影選單", event)
        send_text_message(event, "這裡是電影選單！請選擇右方選項～")

    def is_going_to_movie_thisweek(self, event):
        text = event.message.text
        return text.lower() == "本週新片"

    def on_enter_movie_thisweek(self, event):
        send_text_message(event, "下列是本週新片！")
        show_movie_thisweek(event)
        self.go_back_movie_menu(event)
        

    def is_going_to_movie_intheaters(self, event):
        text = event.message.text
        return text.lower() == "上映中"

    def on_enter_movie_intheaters(self, event):
        send_text_message(event, "下列是上映中！")
        show_movie_intheaters(event)
        self.go_back_movie_menu(event)
    
    def is_going_to_movie_leaderboard(self, event):
        text = event.message.text
        return text.lower() == "排行榜"

    def on_enter_movie_leaderboard(self, event):
        send_text_message(event, "排行榜！")
        show_movie_leaderboard(event)
        self.go_back_movie_menu(event)

    def is_going_to_movie_comingsoon(self, event):
        text = event.message.text
        return text.lower() == "即將上映"

    def on_enter_movie_comingsoon(self, event):
        send_text_message(event, "下列是即將上映！")
        show_movie_comingsoon(event)
        self.go_back_movie_menu(event)

    


    

    
