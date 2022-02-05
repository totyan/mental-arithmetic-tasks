#暗算回答結果のCSVファイルの保存先フォルダの絶対パスの指定
save_path = 'your path'

#問題数
question_number = 2

#１つの問題に対する回答制限時間（単位：秒）
time_limit = 3


import tkinter as tk
from tkinter import messagebox as mbox
from tkinter import font
import time,threading,csv,datetime
import numpy as np


#enterが押された時の挙動（全文字消去）
def del_click(event):
    text.delete(0, tk.END)

def loop():
    date=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    record=[['左','右','答え','入力値','計算時間','問題提示時間','正誤']]
    t1 = time.time() 
    for q in range(question_number):
        global end
        end = 0
        start = time.perf_counter()
        x=str(np.random.randint(5,9))+str(np.random.randint(5,9))
        y=str(np.random.randint(5,9))+str(np.random.randint(5,9))
        label2 = tk.Label(win, text=x, fg="black", font=font1)
        label2.place(x=60+p, y=80+z)
        label3 = tk.Label(win, text=y, fg="black", font=font1)
        label3.place(x=620+p, y=80+z)

        for count in range(time_limit,0,-1):
            label4 = tk.Label(win, text=count, fg="black", font=font1)
            label4.place(x=770+p, y=400+z)
            time.sleep(1)
        
        if end == 0:
            end = time.perf_counter()
        finish = time.perf_counter()
        record.append([x,y,'',text.get(),end-start,finish-start,''])
        text.delete(0, tk.END)
        
    t2 = time.time()
    elapsed_time = t2-t1
    u = 0
    wa = 0
    Nno = 0
    for n in record:
        if  u !=0:
            record[u][2]=str(int(n[0])+int(n[1]))
            if record[u][2] == record[u][3]:
                record[u][6] = '◯'
            else:
                record[u][6] = '×'
            wa = wa + float(record[u][4])
            if record[u][2] == '':
                Nno = Nno+1

        u=u+1

    #TSFの計算
    RT = wa/(len(record)-1)
    Nin = len(record)- 1 - Nno
    Treq = Nin * RT + Nno * (60/20)
    TSF = (Treq/elapsed_time)*100
    record.append(['TSF[%]','=',TSF])
    
    #CSVに保存
    with open(save_path + '/anzan'+date+'.csv', 'w',encoding="utf_8_sig") as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(record)

    #ウィンドウを閉じる
    win.quit()

def starttime(event):
    global end
    end = time.perf_counter()

def callback(event):
    th = threading.Thread(target=del_click, args=(event,))
    th.start()



# ウィンドウを作成
p = 475
z = 170
win = tk.Tk()
win.title("暗算課題")
#win.configure(bg='white')
win.attributes('-topmost',True)
win.attributes('-fullscreen',True)
win.focus_force()
ww=int((win.winfo_screenwidth())/2-500)# 画面の横幅サイズの取得及びx座標の設定
wh=int((win.winfo_screenheight())/2-350)# 画面の縦幅サイズの取得及びy座標の設定
win.geometry("1000x700+"+str(ww)+"+"+str(wh)) # ウィンドウサイズを指定

# ラベルを作成（＋）
font1 = font.Font(family='Helvetica', size=180, weight='bold')
label1 = tk.Label(win, text="＋", fg="black", font=font1)
label1.place(x=360+p, y=80+z)
label4 = tk.Label(win, text="＝", fg="black", font=font1)
label4.place(x=60+p, y=370+z)

# テキストボックスを作成
text = tk.Entry(win,font=font1)
text.place(x=300+p,y=400+z,width=430,height=200)
text.focus_set()

#関数の呼び出し
win.bind('<Return>',callback)
win.bind('<Key>',starttime)

#マルチスレッド開始
th1 = threading.Thread(target=loop)
th1.start()

# ウィンドウを動かす
win.mainloop()