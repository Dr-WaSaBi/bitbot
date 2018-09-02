import Utils

class Module(object):
    def __init__(self, bot, events, exports):
        self.bot = bot

        exports.add("channelset", {"setting": "automode",
            "help": "Disable/Enable automode",
            "validate": Utils.bool_or_none})

        events.on("channel").on("mode").hook(self.on_mode)
        events.on("received").on("join").hook(self.on_join)

    def on_mode(self, event):
        if event["channel"].get_setting("automode", False):
            remove = event["remove"]
            channel = event["channel"]
            mode = event["mode"]
            args = event["mode_args"]

    def on_join(self, event):
        if event["channel"].get_setting("automode", False):
            pass
