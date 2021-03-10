from flask import Flask
from flask_socketio import SocketIO, emit
from cn2an import transform

from test import predict

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")

answer_dict = {
    "greet": "你好～",
    "name": "我是智能机器人小帅同学",
    "father": "高帅博奥~",
    "feature": "我是中北百事通？不懂的尽管问我！",
    "sc_location": "操场背后，雅贤阁对面",
    "et_location": "校医院背后",
    "rn_location": "沿着奥迈健身一直往下走",
    "b_location": "操场网球场右侧，器材室后侧"
}

@socketio.on("receive")
def recevie_msg(msg):
    if ":" in msg:
        mode, _msg = msg.split(":")
        if mode in ["cn2an", "an2cn"]:
            answer = f"{transform(_msg, mode)} 【by {mode}】"
        else:
            intent = predict(msg)
            answer = answer_dict[intent]
    else:
        intent = predict(msg)
        answer = answer_dict[intent]

    with open("./dialog.txt", "a") as f_dialog:
        f_dialog.write(msg+"\t"+answer+"\n")

    emit("response", {"msg": answer})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8002)
