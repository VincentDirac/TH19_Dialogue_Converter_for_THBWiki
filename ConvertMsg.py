import os
import CreateDatabase
import sqlite3

def main():
    path = "E:/VincentDirac/thtk-Unpack_TH19_All_in_One/dialogue/"
    for root, folders, files in os.walk(path):
        for file in files:
            if file == '.gitignore' or 'vs' in file:
                pass
            elif 'end' in file:
                pass
            else:
                convertMsg(root, file)
            
def convertMsg(root, file):
    TH19_database = sqlite3.connect("data/TH19_database.db")
    dbCursorStory = TH19_database.cursor()
    playerName = file.replace("st.txt", "")
    dbCursorStory.execute("""SELECT * FROM Story
                     Where CharaNo = '{}'""".format(playerName))
    charaResult = dbCursorStory.fetchone()
    with open(root + file, "r+", encoding="utf-8") as f:
        g = open("convertedFiles/" + playerName + "st_converted.txt", "w+", encoding="utf-8")
        fileList = f.readlines()
        stageID = 0
        stageNo = 0
        for item in range(len(fileList)):
            line = fileList[item]
            if "entry" in line:
                entryNo = eval(line.split(" ")[1])  # entry编号
                if entryNo in [0, 1, 2]:
                    g.write("此部分忽略。\n")
                else:
                    stageID = entryNo % 3   # 用于判断处于战前对话还是战胜/战败对话
                    stageNo = entryNo // 3  # 实际的Stage数
                    if stageID == 0:
                        g.write("xx\n\n== Stage {} ==\n".format(stageNo))
                    elif stageID == 1:
                        g.write("status\n[[{}]] 被击败\n".format(charaResult[stageNo+3]))
                        if stageNo == 6:
                            g.write("status\n[[#{0}|{0}]]\n".format(charaResult[10]))
                    elif stageID == 2:
                        g.write("status\n如果玩家被击败\n")
            if "\t7;0" in line:
                # 判定战前自机
                if "\t19;" in fileList[item+2]:
                    pass
                elif "\t20;" in fileList[item+2]:
                    pass
                else:
                    g.write("char\n{}\n".format(charaResult[3]))
            if "\t8;0" in line:
                # 判定战前敌机
                if "\t19;" in fileList[item+2]:
                    pass
                elif "\t20;" in fileList[item+2]:
                    pass
                else:
                    g.write("char\n{}\n".format(charaResult[stageNo+3]))
            if "\t42;" in line:
                # 判定战后胜者
                if stageID == 1:
                    g.write("char\n{}\n".format(charaResult[3]))
                elif stageID == 2:
                    g.write("char\n{}\n".format(charaResult[stageNo+3]))
            if "\t43;" in line:
                # 判定战后败者
                if stageID == 1:
                    g.write("char\n{}\n".format(charaResult[stageNo+3]))
                elif stageID == 2:
                    g.write("char\n{}\n".format(charaResult[3]))
            if "\t17;" in line:
                # 判定对话文本
                if "\t17;" not in fileList[item-1]:
                    g.write("ja\n")
                if "\t17;|" in line:
                    g.write(line.replace("\t17;|", "{{ruby-ja||").rstrip("\n") + "}}<br>")
                else:
                    if "\t17;" in fileList[item+1]:
                        g.write(line.replace("\t17;", "").rstrip("\n") + "<br>")
                    else:
                        g.write(line.replace("\t17;", "") + "zh\n\n")
            if "\t19;" in line:
                pass
            if "\t20;" in line:
                dbCursorTitles = TH19_database.cursor()
                dbCursorTitles.execute("""SELECT * FROM BossTitles
                     Where CharaName = '{}'""".format(charaResult[stageNo+3]))
                bossTitle = dbCursorTitles.fetchone()[3]
                bossTitle = bossTitle.replace("\\n", "\n")
                g.write(bossTitle)

# 条件块太多了。还有bgm和name比较麻烦。又不想手调，也许可以考虑二次替换emmm睡了（

if __name__ == "__main__":
    CreateDatabase.CreateDatabase("data/TH19_BossTitles.xlsx", "data/TH19_BGM_Map.xlsx",
                   "data/TH19_Story.xlsx", "data/TH19_CharaNo.xlsx", "data/TH19_database.db")
    main()