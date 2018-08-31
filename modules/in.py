import time
import Utils

SECONDS_MAX = Utils.SECONDS_WEEKS * 8
SECONDS_MAX_DESCRIPTION = "8 weeks"


class Module(object):
    def __init__(self, bot):
        self.bot = bot
        bot.events.on("received").on("command").on("in").hook(
            self.in_command, min_args=2,
            help="Set a reminder", usage="<time> <message>")
        bot.events.on("timer").on("in").hook(self.timer_due)

    def in_command(self, event):
        seconds = Utils.from_pretty_time(event["args_split"][0])
        message = " ".join(event["args_split"][1:])
        if seconds:
            if seconds <= SECONDS_MAX:
                due_time = int(time.time()) + seconds

                self.bot.add_timer("in", seconds,
                                   target=event["target"].name,
                                   due_time=due_time,
                                   server_id=event["server"].id,
                                   nickname=event["user"].nickname,
                                   message=message)
                event["stdout"].write("Saved")
            else:
                event["stderr"].write(
                    "The given time is above the max (%s)" % (
                        SECONDS_MAX_DESCRIPTION))
        else:
            event["stderr"].write(
                "Please provided a valid time above 0 seconds")

    def timer_due(self, event):
        for server in self.bot.servers.values():
            if event["server_id"] == server.id:
                server.send_message(event["target"],
                                    "%s, this is your reminder: %s" % (
                                        event["nickname"], event["message"]))
                break
