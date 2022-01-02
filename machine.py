from fsm import TocMachine


def create_machine():
    machine = TocMachine(
        states=["main_menu", "movie_menu", "movie_thisweek", "movie_intheaters", "movie_comingsoon", "movie_leaderboard"],
        transitions=[
            {
                "trigger": "advance",
                "source": "main_menu",
                "dest": "movie_menu",
                "conditions": "is_going_to_movie_menu",
            },
            {
                "trigger": "advance",
                "source": "movie_menu",
                "dest": "movie_thisweek",
                "conditions": "is_going_to_movie_thisweek",
            },
            {
                "trigger": "advance",
                "source": "movie_menu",
                "dest": "movie_intheaters",
                "conditions": "is_going_to_movie_intheaters",
            },
            {
                "trigger": "advance",
                "source": "movie_menu",
                "dest": "movie_comingsoon",
                "conditions": "is_going_to_movie_comingsoon",
            },
            {
                "trigger": "advance",
                "source": "movie_menu",
                "dest": "movie_leaderboard",
                "conditions": "is_going_to_movie_leaderboard",
            },
            {
                "trigger": "advance",
                "source": ["movie_menu", "movie_thisweek", "movie_intheaters", "movie_comingsoon", "movie_leaderboard"],
                "dest": "main_menu",
                "conditions": "is_going_to_main_menu",
            },
            {
                "trigger": "go_back_movie_menu",
                "source": ["movie_thisweek", "movie_intheaters", "movie_comingsoon", "movie_leaderboard"],
                "dest": "movie_menu",
            },
        ],
        initial="main_menu",
        auto_transitions=False,
        show_conditions=True,
    )
    return machine
