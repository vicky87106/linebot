import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,StickerMessage,StickerSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", "state1", "rice","chicken"],
    transitions=[#狀態
        { "trigger": "advance",  "source": "user", "dest": "state1",  "conditions": "is_going_to_state1",},
        { "trigger": "advance",  "source": "user", "dest": "rice",   "conditions":"is_going_to_rice",},
        { "trigger": "advance",  "source": "rice", "dest": "chicken",  },
        {"trigger": "go_back", "source": ["state1", "chicken"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)




app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=["POST"]) #接收POST方法請求
def callback():
    signature = request.headers["X-Line-Signature"] #取得HTTP標頭的密鑰欄位
    # get request body as text
    body = request.get_data(as_text=True) #取得HTTP訊息本體並轉成文字格式
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)


@handler.default()

#接收貼圖事件並回覆相同貼圖
@handler.add(MessageEvent,message=StickerMessage)
def handle_sticker_message(event):
    pid=event.message.package_id #收到的貼圖包編號
    sid=event.message.sticker#貼圖編號
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(package_id=pid,sticker_id=sid)
    )


