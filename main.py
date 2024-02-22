import tkinter as tk
import random
from time import sleep
import birdinfo
import event
import os


def Sleep():
    sleep(0.3)


# ----- 窗口 -----
# 欢迎窗口
def window_start():
    global window1
    window1 = tk.Tk()
    window1.title("从零开始的城市鸟生活")
    window1.resizable(False, False)  # 禁止宽度和高度调整
    window1.geometry("900x600")

    title = tk.Label(
        window1, text="从零开始的城市鸟生活", height=2, font=("微软雅黑", 32)
    )
    title.place(x=220, y=50)
    text1 = tk.Label(
        window1,
        text="v2.0 (2024.02)\n\n复旦翼缘出品\n\n文案：RV\n\n制作：SYX\n",
        height=8,
        font=("微软雅黑", 16),
    )
    text1.place(x=360, y=160)

    button_start = tk.Button(
        window1, text="开始", font=("微软雅黑", 20), command=window_game
    )
    button_start.place(x=380, y=400, height=50, width=100)

    window1.mainloop()


# 游戏窗口
def window_game():
    window1.destroy()
    global window
    window = tk.Tk()
    window.title("从零开始的城市鸟生活")
    window.resizable(False, False)  # 禁止宽度和高度调整
    window.geometry("900x600")

    # 文本显示框，位于窗口左侧
    global text_box
    text_box = tk.Text(window, wrap=tk.WORD, width=60, font=("微软雅黑", 12))
    text_box.pack(side=tk.LEFT, padx=10, pady=10, fill="y", expand=False)
    # 信息显示框，右上
    global info_box
    info_box = tk.Label(
        window,
        text="【未知】\n\n年龄：0\n食物：0\n经验：0\n",
        height=8,
        font=("微软雅黑", 16),
    )
    info_box.pack(padx=0, pady=10)
    # 游戏主体
    main_game()

    window.mainloop()


# 在文本框里添加一行
def add_line(text):  # 定义添加行的函数
    text_box.insert(tk.END, text + "\n")
    text_box.update()  # 更新Tkinter主循环，以便文本被实时显示
    text_box.yview_moveto(1)  # 滚动到底部
    Sleep()


# 更新属性显示，每次属性变动后都要添加
def update_info_box():
    global info_box
    info_box.destroy()
    info_box = tk.Label(
        window,
        text="【{}】\n\n年龄：{}\n食物：{}\n经验：{}\n".format(
            Myinfo["name"], Mystat["AGE"], Mystat["FOOD"], Mystat["EXP"]
        ),
        height=8,
        font=("微软雅黑", 16),
    )
    info_box.pack(padx=0, pady=10)


# ----- 按钮 -----
def button_click(button_number, var):
    var.set(button_number)


def create_buttons(choice):
    button_var = tk.IntVar()  # 创建一个IntVar变量，用于存储按钮点击的编号

    # 创建三个按钮，并指定点击按钮时调用的函数
    button1 = tk.Button(
        window,
        text="<1>",
        font=("微软雅黑", 16),
        command=lambda: button_click(1, button_var),
    )
    button2 = tk.Button(
        window,
        text="<2>",
        font=("微软雅黑", 16),
        command=lambda: button_click(2, button_var),
    )
    button3 = tk.Button(
        window,
        text="<3>",
        font=("微软雅黑", 16),
        command=lambda: button_click(3, button_var),
    )
    button_list = [button1, button2, button3]

    # 将按钮放置在窗口上
    for i in range(choice):
        button_tmp = button_list[i]
        button_tmp.place(height=30, width=60)
        button_tmp.pack(pady=5)

    # 使用wait_variable方法暂停主程序，直到button_var变量被设置
    window.wait_variable(button_var)

    # 获取按钮点击的编号
    clicked_button_number = button_var.get()
    Sleep()
    for i in range(3):
        button_tmp = button_list[i]
        button_tmp.destroy()

    return clicked_button_number


# ----- 游戏内容 -----
# 游戏开始
def BeginGame():
    add_line("一觉醒来我转生了！我变成了——")
    selected = random.sample(list(birdinfo.birdlist.keys()), 3)
    for i in range(0, 3):
        add_line(f"  <{i+1}> {birdinfo.birdlist[selected[i]]['name']}")
    global Myinfo, Mystat
    # 获取鸟类信息
    Myinfo = birdinfo.birdlist[selected[create_buttons(3) - 1]]
    add_line(" ")
    add_line(f"...一只刚出生的{Myinfo['name']}！")
    add_line(" ")
    # 初始化状态信息
    Mystat = {
        "AGE": 0,
        "EXP": 0,
        "FOOD": 0,
        "LIVE": 1,
        "DANGER": 0,  # 年龄，经验，食物，是否活着，危险值
        "Humanlist": [],
        "Friendlist": [],
        "Giftlist": [],  # 遇到人类，结交朋友，收到礼物
        "Deathcount": 0,
        "Childcount": 0,
    }  # 逃脱死亡次数，后代数

    BeginSpecial()
    update_info_box()


# 出生时选择一项随机修正
def BeginSpecial():
    global Myinfo, Mystat
    match random.choice(range(6)):
        case 0:
            add_line("我的父母似乎结交了一些危险的朋友……")
            add_line(" ")
            Mystat["Friendlist"].append(random.choice([103, 123, 124]))
        case 1:
            add_line("我的父母为我积攒了不少食物。（初始食物+2）")
            add_line(" ")
            Mystat["FOOD"] += 2
        case 2:
            add_line("我的父母从小带我闯荡社会。（初始经验+1）")
            add_line(" ")
            Mystat["EXP"] += 1
        # case 3:  # 无事发生
        # case 4:
        # case 5:


# 新的一年开始
def NewYear():
    global Mystat
    add_line("-" * 70)
    Sleep()
    Mystat["AGE"] += 1
    add_line("这是我出生的第{}年。".format(Mystat["AGE"]))
    add_line(" ")
    update_info_box()


# 一年中的三个事件：朋友，人类，繁殖
def FriendEvent():
    add_line("天气很好，要出门结识新的伙伴吗？")
    Sleep()
    add_line("  <1> 外出探索")
    add_line("  <2> 待在家里")
    add_line(" ")
    Mychoice = create_buttons(2)
    global Myinfo, Mystat
    if Mychoice == 1:  # 外出探索，遇到新朋友
        while 1:
            selected = random.choice(list(event.Friend.keys()))
            if selected not in Mystat["Friendlist"]:
                break
        Mystat["Friendlist"].append(selected)
        Sleep()
        add_line("出行中……")
        Sleep()
        add_line(f"在旅行途中，我认识了一位新朋友——{event.Friend[selected]['name']}！")
        Sleep()
        if event.Friend[selected]["tasty"] == 0:
            add_line("它觉得我很可爱。")
            add_line(" ")
        else:
            add_line("它似乎觉得我很好吃？")
            add_line(" ")
        Sleep()
        DangerCheck(0.6)
    else:  # 待在家里
        if len(Mystat["Friendlist"]) > 0:  # 有朋友，来拜访
            selected = random.choice(Mystat["Friendlist"])
            if event.Friend[selected]["tasty"] == 0:  # 不会吃我的朋友，带来礼物
                gift_id = event.Friend[selected]["gift"]
                if gift_id in Mystat["Giftlist"]:
                    add_line(
                        f"我的朋友 {event.Friend[selected]['name']} 再次来找我玩，我们度过了愉快的时光。"
                    )
                    add_line(" ")
                else:
                    add_line(
                        f"我的朋友 {event.Friend[selected]['name']} 带着礼物来拜访！"
                    )
                    Sleep()
                    add_line(f"获得物品{event.Gift[gift_id]['text']}。")
                    add_line(" ")
                    Mystat["Giftlist"].append(gift_id)
                    Mystat["AGE"] += event.Gift[gift_id]["effect"].get("age", 0)
                    Mystat["EXP"] += event.Gift[gift_id]["effect"].get("exp", 0)
                    Myinfo["fight"][0] += event.Gift[gift_id]["effect"].get("str", 0)
                    Myinfo["fight"][1] += event.Gift[gift_id]["effect"].get("dex", 0)
                    Myinfo["fight"][2] += event.Gift[gift_id]["effect"].get("wis", 0)
                    update_info_box()
                Sleep()
            else:
                add_line(
                    f"我的朋友 {event.Friend[selected]['name']} 出现在我家门口，看起来很饿……"
                )
                add_line(" ")
                Sleep()
                FightEvent(event.Friend[selected])  # 会吃我的朋友，进入战斗
                Sleep()
        else:
            add_line("我在家门口随便转了转。")
            add_line(" ")
            Sleep()
        DangerCheck(0.3)


def HumanEvent():
    add_line("要前往人类生活的区域觅食吗？")
    Sleep()
    add_line("  <1> 靠近")
    add_line("  <2> 远离")
    add_line(" ")
    Mychoice = create_buttons(2)
    global Myinfo, Mystat
    if Mychoice == 1:
        add_line("在城镇中游荡……")
        Sleep()
        if random.choice(["meet", "notmeet"]) == "meet":  # 遇到人类
            while 1:
                selected = random.choice(list(event.Human.keys()))
                if selected not in Mystat["Humanlist"]:
                    break
            add_line(f"我{event.Human[selected]['text']}。")
            add_line(" ")
            Sleep()
            Mystat["Humanlist"].append(selected)
            if random.choice(range(6)) == 0:  # 小概率事件
                add_line(
                    "我发现了一处人类的投喂点，未来的日子吃喝不愁了！！（食物+10）"
                )
                add_line(" ")
                Mystat["FOOD"] += 10
                update_info_box()
                Sleep()
        else:
            add_line(f"我在高楼间自由穿梭，仿佛生来就属于这里。")
            add_line(" ")
            Sleep()
            FoodEvent()
        add_line("在人类居住区的经历让我增长了见识。（经验+1）")
        add_line(" ")
        Mystat["EXP"] += 1
        update_info_box()
        Sleep()
        DangerCheck(0.6)
    else:
        add_line("我没有冒险接近人类的生活区。")
        add_line(" ")
        Sleep()
        FoodEvent()


def BreedEvent():
    add_line(f"繁殖季到了，我有足够的能力养育后代吗？我选择——")
    Sleep()
    add_line("  <1> 谈恋爱")
    add_line("  <2> 单身")
    add_line(" ")
    Mychoice = create_buttons(2)
    global Myinfo, Mystat
    if Mychoice == 1:
        add_line(f"寻找伴侣中...")  # 第一关，经验大于0则成功
        Sleep()
        if Mystat["EXP"] == 0:  # 寻找伴侣失败，原因类型1
            selected = random.choice([101, 102])
            add_line(f"由于{event.Breed[selected]['text']}，寻找伴侣失败。")
            add_line(" ")
            Sleep()
        else:  # 寻找伴侣成功
            add_line(f"筑巢中...孵化中...")  # 第二关，经验检定
            Sleep()
            if MakeRoll(Mystat["EXP"], 5) == 0:  # 孵化失败，原因类型2
                selected = random.choice(range(201, 205))
                add_line(f"由于{event.Breed[selected]['text']}，孵化失败。（食物-1）")
                add_line(" ")
                Mystat["FOOD"] -= 1
                update_info_box()
                Sleep()
            else:  # 孵化成功
                child = random.choice([0, -1]) + Myinfo["childlim"]
                add_line(f"有{child}个蛋成功孵化！")
                add_line(" ")
                Sleep()
                add_line("养育雏鸟中……")  # 第三关，经验检定
                if MakeRoll(Mystat["EXP"], 5) == 0:  # 养育失败，原因类型3
                    selected = random.choice(range(301, 305))
                    add_line(
                        f"由于{event.Breed[selected]['text']}，我没能养大它们。（食物-1）"
                    )
                    add_line(" ")
                    Mystat["FOOD"] -= 1
                    update_info_box()
                    Sleep()
                else:  # 食物检定
                    if Mystat["FOOD"] <= 0:  # 食物不足
                        add_line(f"由于{event.Breed[401]['text']}。（食物-1）")
                        add_line(" ")
                        Mystat["FOOD"] -= 1
                        update_info_box()
                        Sleep()
                    else:  # 成功
                        child_max = min(Mystat["FOOD"], child)
                        child_min = max(1, child_max - 2)
                        child_live = random.choice(range(child_min, child_max + 1))
                        add_line(
                            f"经过一番努力，我养大了{child_live}只健康活泼的雏鸟！（食物-{child_live}）"
                        )
                        add_line(" ")
                        Mystat["Childcount"] += child_live
                        Mystat["FOOD"] -= child_live
                        update_info_box()
                        Sleep()
        add_line("繁殖经历让我积累了经验。（经验+1）")
        add_line(" ")
        Mystat["EXP"] += 1
        update_info_box()
        Sleep()
        DangerCheck(0.6)
    else:
        add_line(f"我决定吃吃喝喝养精蓄锐。（食物+2）")
        add_line(" ")
        Mystat["FOOD"] += 2
        update_info_box()
        Sleep()
        DangerCheck(0.3)


# 觅食--人类事件的附属
def FoodEvent():
    global Mystat
    add_line("觅食中……")
    Sleep()
    selected = random.choice(list(event.Food.keys()))
    foodtoday = random.choice(Myinfo["food"])
    add_line("今天我" + event.Food[selected]["text"].format(foodtoday))
    add_line(" ")
    Mystat["FOOD"] += event.Food[selected]["effect"]["food"]
    Sleep()
    DangerCheck(0.3)
    update_info_box()


# 危险值--三大事件的附属
def DangerCheck(value):
    global Mystat
    Mystat["DANGER"] += random.random() * value
    if Mystat["DANGER"] > 1:
        DeathEvent()
        if Mystat["LIVE"] == 1:  # 如果存活，危险值归零并继续
            Mystat["Deathcount"] += 1
            Mystat["DANGER"] = 0


# 死亡事件--危险值满的结果
def DeathEvent():
    global Myinfo, Mystat
    if Mystat["FOOD"] <= 0:  # 先判定食物
        add_line("由于天气恶劣，我好几天没找到食物，我感到饥饿...")
        Sleep()
        if Mystat["AGE"] <= Myinfo["agelim"]:
            add_line("幸好我体质不错，撑了几天并找到了食物。（食物+2）")
            add_line(" ")
            Mystat["FOOD"] += 2
            update_info_box()
        else:
            add_line("饥饿使我精疲力尽，我倒下了。")
            add_line(" ")
            Mystat["LIVE"] = 0
    else:  # 然后随机事件
        match random.choice(range(1, 4)):
            case 1:  # 捕食者
                selected = random.choice(range(101, 104))
                add_line(f"糟糕，一只{event.Death[selected]['name']}对我虎视眈眈！")
                add_line(" ")
                Sleep()
                FightEvent(event.Death[selected])
            case 2:  # 环境危险
                selected = random.choice(range(201, 205))
                add_line(
                    f"我忙于觅食或飞行，没注意到附近危险的{event.Death[selected]['name']}。"
                )
                Sleep()
                if MakeRoll(Myinfo["agelim"] - Mystat["AGE"], 5) == 0:
                    add_line(
                        f"增长的年岁减缓了我的反应速度，我没能逃脱，成为了{event.Death[selected]['name']}的牺牲品。"
                    )
                    add_line(" ")
                    Mystat["LIVE"] = 0
                elif MakeRoll(Mystat["EXP"], 4) == 0:
                    add_line(
                        f"缺乏经验让我措手不及，我没能逃脱，成为了{event.Death[selected]['name']}的牺牲品。"
                    )
                    add_line(" ")
                    Mystat["LIVE"] = 0
                else:
                    add_line(
                        f"由于经验充足而反应迅速，我幸运地逃离了{event.Death[selected]['name']}。"
                    )
                    add_line(" ")
            case 3:  # 衰老或疾病
                selected = random.choice(range(301, 303))
                if Mystat["AGE"] <= Myinfo["agelim"]:
                    add_line(f"{event.Death[selected]['success']}")
                    add_line(" ")
                else:
                    add_line(f"{event.Death[selected]['fail']}")
                    add_line(" ")
                    Mystat["LIVE"] = 0
    Sleep()


# 战斗--捕食者或危险朋友拜访
def FightEvent(enemy):
    global Myinfo, Mystat
    add_line("----------战斗开始----------")
    Sleep()
    add_line(f"【{enemy['name']} vs. {Myinfo['name']}】")
    Sleep()

    if Mystat["AGE"] >= Myinfo["agelim"]:
        tmp = [2, 2, 0]  # 对手临时修正值
    else:
        tmp = [0, 0, 0]
    result = ""

    # 三轮战斗
    for i in range(1, 4):
        add_line(f"---第{i}/3轮---")
        Sleep()
        add_line(event.Fight[i]["text"].format(enemy["name"]) + "我选择——")
        add_line(" ")
        Sleep()
        skill = ["力量", "敏捷", "智慧"]

        for j in range(1, 4):
            add_line(
                f"  <{j}> {event.Fight[i][skill[j-1]]}（{skill[j-1]}{Myinfo['fight'][j-1]} 目标{enemy['fight'][j-1] + tmp[j-1]}）"
            )
        Mychoice = create_buttons(3)
        Sleep()

        roll_random = random.choice(range(1, 13))
        roll_value = Myinfo["fight"][Mychoice - 1]
        roll = roll_random + roll_value
        target = enemy["fight"][Mychoice - 1] - tmp[Mychoice - 1]
        add_line(" ")
        add_line(f"掷骰<1d12={roll_random}> + 属性<{roll_value}> = 最终结果<{roll}>")
        Sleep()

        if roll >= 2 * target:
            result = "win"  # 大成功
            add_line(f"最终结果大于目标值两倍——")
            add_line(f"对手{event.Fight[i * 10 + Mychoice][result]}，放弃了捕食。")
            add_line(" ")
            break
        elif roll < target / 2:
            result = "lose"  # 大失败
            add_line(f"最终结果小于目标值一半——")
            add_line(f"对手{event.Fight[i * 10 + Mychoice][result]}，然后致命一击。")
            add_line(" ")
            break
        elif roll >= target:
            result = "favoured"  # 普通成功下一轮优势
            add_line(f"最终结果大于目标值——")
            add_line(
                f"对手{event.Fight[i * 10 + Mychoice][result]}，让我在下一轮中占有优势。"
            )
            add_line(" ")
            tmp[Mychoice - 1] -= 3
        else:
            result = "ill-favoured"  # 普通失败下一轮劣势
            add_line(f"最终结果小于目标值——")
            add_line(
                f"对手{event.Fight[i * 10 + Mychoice][result]}，让我在下一轮中处于劣势。"
            )
            add_line(" ")
            tmp[Mychoice - 1] += 3
        Sleep()

    add_line("----------战斗结束----------")
    add_line(" ")
    if result == "win":
        add_line(f"我幸运地逃脱了{enemy['name']}的追捕。")
        add_line(" ")
    else:
        add_line(f"我没能逃脱，成为了{enemy['name']}的美餐。")
        add_line(" ")
        Mystat["LIVE"] = 0
    Sleep()


# 属性检定--繁殖、环境危险的附属
def MakeRoll(value, target):
    result = random.choice(range(1, 5)) + value
    if result >= target:
        return 1
    else:
        return 0


# 游戏结束
def EndGame():
    global Myinfo, Mystat
    add_line("-" * 70)
    add_line(
        f"作为一只{Myinfo['name']}，在我长达{Mystat['AGE']}年的一生中，养育了{Mystat['Childcount']}个后代，\n遇到人类{len(Mystat['Humanlist'])}次，死里逃生{Mystat['Deathcount']}次，"
    )
    Sleep()
    friend_str = ""
    for i in Mystat["Friendlist"]:
        friend_str += event.Friend[i]["name"] + " "
    add_line(
        f"遇见过这些萍水相逢的鸟类朋友：{friend_str}，收到{len(Mystat['Giftlist'])}份特别的礼物。\n"
    )
    Sleep()
    # 结束词
    selected = random.choice(event.Endtext)
    add_line(selected)
    add_line("-" * 70)
    Sleep()
    # 成就
    if Mystat["AGE"] >= 7:
        add_line("恭喜达成【寿比南山】——年龄达到7岁！")
    if Mystat["Childcount"] >= 7:
        add_line("恭喜达成【子孙满堂】——拥有7个后代！")
    if Mystat["Childcount"] == 0:
        add_line("恭喜达成【自然选择】——没有后代！")
    if len(Mystat["Friendlist"]) >= 5:
        add_line("恭喜达成【朋友遍天下】——拥有5个朋友！")
    if len(Mystat["Friendlist"]) == 0:
        add_line("恭喜达成【社恐】——没有朋友！")
    if len(Mystat["Humanlist"]) >= 5:
        add_line("恭喜达成【人类之友】——遇到人类5次！")
    Sleep()
    add_line(" ")
    # 重新开始/退出
    add_line("  <1> 重新开始\n  <2> 退出游戏\n")
    Mychoice = create_buttons(2)
    if Mychoice == 1:
        add_line("\n\n\n")
        main_game()
    else:
        os._exit(0)


# ----- 主程序 -----
def main_game():
    BeginGame()
    global Myinfo, Mystat
    while Mystat["LIVE"] == 1:
        NewYear()
        if Mystat["AGE"] == 1:
            funlist = [FriendEvent, HumanEvent]  # 是繁殖季出生的，不会再有繁殖季
        else:
            funlist = [FriendEvent, HumanEvent, BreedEvent]
        random.shuffle(funlist)  # 三大事件顺序随机
        for f in funlist:
            f()
            add_line(" ")
            Sleep()
            if Mystat["LIVE"] == 0:
                break  # 如果死亡，跳过未发生事件
    EndGame()


if __name__ == "__main__":
    window_start()
