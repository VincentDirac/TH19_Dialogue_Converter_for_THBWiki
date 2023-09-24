import os
import CreateDatabase
import sqlite3

def main():
    CreateDatabase.CreateDatabase("data/TH19_BossTitles.xlsx", "data/TH19_BGM_Map.xlsx",
                "data/TH19_Story.xlsx", "data/TH19_CharaNo.xlsx", "data/TH19_database.db")
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
                        print("xx\n\n== Stage {} ==\n".format(stageNo))
                    elif stageID == 1:
                        g.write("status\n弹幕开始！\nstatus\n[[{}]] 被击败\n".format(charaResult[stageNo+3]))
                        print("status\n弹幕开始！\nstatus\n[[{}]] 被击败\n".format(charaResult[stageNo+3]))
                        if stageNo == 6:
                            g.write("status\n[[#{0}|{0}]]\n".format(charaResult[10]))
                            print("status\n[[#{0}|{0}]]\n".format(charaResult[10]))
                    elif stageID == 2:
                        g.write("status\n如果玩家被击败\n")
                        print("status\n如果玩家被击败\n")
            elif "\t7;0" in line:
                # 判定战前自机
                if "\t19;" in fileList[item+2]:
                    line, fileList[item+2] = fileList[item+2], line
                    if "\t19;22" in line or "\t19;23" in line:
                        pass
                    else:
                        writeBGM(TH19_database, line, g)
                elif "\t19;" in fileList[item+3]:
                    line, fileList[item+3] = fileList[item+3], line
                    if "\t19;22" in line or "\t19;23" in line:
                        pass
                    else:
                        writeBGM(TH19_database, line, g)
                elif "\t20;" in fileList[item+2]:
                    line, fileList[item+2] = fileList[item+2], line
                    writeBossTitle(TH19_database, charaResult, stageNo, g)
                elif "\t20;" in fileList[item+3]:
                    line, fileList[item+3] = fileList[item+3], line
                    writeBossTitle(TH19_database, charaResult, stageNo, g)
                else:
                    g.write("char\n{}\n".format(charaResult[3]))
                    print("char\n{}\n".format(charaResult[3]))
            elif "\t8;0" in line:
                # 判定战前敌机
                if "\t19;" in fileList[item+2]:
                    line, fileList[item+2] = fileList[item+2], line
                    if "\t19;22" in line or "\t19;23" in line:
                        pass
                    else:
                        writeBGM(TH19_database, line, g)
                elif "\t19;" in fileList[item+3]:
                    line, fileList[item+3] = fileList[item+3], line
                    if "\t19;22" in line or "\t19;23" in line:
                        pass
                    else:
                        writeBGM(TH19_database, line, g)
                elif "\t20;" in fileList[item+2]:
                    line, fileList[item+2] = fileList[item+2], line
                    writeBossTitle(TH19_database, charaResult, stageNo, g)
                elif "\t20;" in fileList[item+3]:
                    line, fileList[item+3] = fileList[item+3], line
                    writeBossTitle(TH19_database, charaResult, stageNo, g)
                else:
                    g.write("char\n{}\n".format(charaResult[stageNo+3]))
                    print("char\n{}\n".format(charaResult[stageNo+3]))
            elif "\t55" in line:
                # 敌机点阵图出现
                if "\t17;" not in fileList[item+6] and "\t17;" not in fileList[item+4]:
                    pass
                else:
                    if "\t19;" in fileList[item+2]:
                        line, fileList[item+2] = fileList[item+2], line
                        if "\t19;22" in line or "\t19;23" in line:
                            pass
                        else:
                            writeBGM(TH19_database, line, g)
                    elif "\t19;" in fileList[item+3]:
                        line, fileList[item+3] = fileList[item+3], line
                        if "\t19;22" in line or "\t19;23" in line:
                            pass
                        else:
                            writeBGM(TH19_database, line, g)
                    elif "\t20;" in fileList[item+2]:
                        line, fileList[item+2] = fileList[item+2], line
                        writeBossTitle(TH19_database, charaResult, stageNo, g)
                    else:
                        g.write("char\n{}\n".format(charaResult[stageNo+3]))
                        print("char\n{}\n".format(charaResult[stageNo+3]))
            elif "\t42;" in line:
                # 判定战后胜者
                if stageID == 1:
                    g.write("char\n{}\n".format(charaResult[3]))
                    print("char\n{}\n".format(charaResult[3]))
                elif stageID == 2:
                    g.write("char\n{}\n".format(charaResult[stageNo+3]))
                    print("char\n{}\n".format(charaResult[stageNo+3]))
            elif "\t43;" in line:
                # 判定战后败者
                if stageID == 1:
                    g.write("char\n{}\n".format(charaResult[stageNo+3]))
                    print("char\n{}\n".format(charaResult[stageNo+3]))
                elif stageID == 2:
                    g.write("char\n{}\n".format(charaResult[3]))
                    print("char\n{}\n".format(charaResult[3]))
            elif "\t17;" in line:
                # 判定对话文本
                if "\t17;" not in fileList[item-1]:
                    g.write("ja\n")
                    print("ja\n")
                if "\t17;|" in line:
                    g.write(line.replace("\t17;|", "ruby-ja||").rstrip("\n") + "<br>")
                    print(line.replace("\t17;|", "ruby-ja||").rstrip("\n") + "<br>")
                else:
                    if "\t17;" in fileList[item+1]:
                        g.write(line.replace("\t17;", "").rstrip("\n") + "<br>")
                        print(line.replace("\t17;", "").rstrip("\n") + "<br>")
                    else:
                        g.write(line.replace("\t17;", "") + "zh\n\n")
                        print(line.replace("\t17;", "") + "zh\n\n")
            elif "\t19;" in line:
                if "\t19;22" in line or "\t19;23" in line:
                    pass
                else:
                    writeBGM(TH19_database, line, g)
            elif "\t20;" in line:
                writeBossTitle(TH19_database, charaResult, stageNo, g)
            else:
                pass

# 条件块太多了。还有bgm和name比较麻烦。又不想手调，也许可以考虑二次替换emmm睡了（
def writeBossTitle(dbName, charaResult, stageNo, writeFile):
    dbCursorTitles = dbName.cursor()
    dbCursorTitles.execute("""SELECT * FROM BossTitles
        Where CharaWikiName = '{}'""".format(charaResult[stageNo+3]))
    bossTitle = dbCursorTitles.fetchone()[3]
    bossTitle = bossTitle.replace("\\n", "\n")
    writeFile.write(bossTitle)
    print(bossTitle)

def writeBGM(dbName, line, writeFile):
    dbCursorBGM = dbName.cursor()
    dbCursorBGM.execute("""SELECT bgmWikitext FROM BGMMap
        Where bgmZUNMsgText = '{}'""".format(line.replace("\n", "\\n").replace("\t", "\\t")))
    BGM = dbCursorBGM.fetchone()
    BGM = BGM[0].replace("\\n", "\n")
    writeFile.write("BGM: " + BGM)
    print("BGM: " + BGM)

if __name__ == "__main__":
    main()
