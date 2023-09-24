import sqlite3
import pandas as pd


def CreateDatabase(TableName, TableBGM, TableBOSS, TableCharaNo, dbFilename):
    TH19_database = sqlite3.connect(dbFilename)    # 新建TH19数据库
    print("数据库建立成功。")
    CreateTableBossTitles(TableName, TH19_database)
    CreateTableBGMMap(TableBGM, TH19_database)
    CreateTableStory(TableBOSS, TH19_database)
    print("表格创建成功")


def CreateTableBossTitles(txtFileName, dbName):
    # 创建角色名称号表
    sheetBossTitles = pd.read_excel(txtFileName)
    sheetBossTitles.to_sql("BossTitles", dbName, if_exists='replace')


def CreateTableBGMMap(txtFileName, dbName):
    # 创建游戏内BGM对应关系
    sheetBGMMap = pd.read_excel(txtFileName)
    sheetBGMMap.to_sql("BGMMap", dbName, if_exists='replace')


def CreateTableStory(txtFileName, dbName):
    # 创建各故事线自机BOSS结局编号对应关系
    sheetStory = pd.read_excel(txtFileName)
    sheetStory.to_sql("Story", dbName, if_exists='replace')


if __name__ == "__main__":
    CreateDatabase("data/TH19_BossTitles.xlsx", "data/TH19_BGM_Map.xlsx",
                   "data/TH19_Story.xlsx", "data/TH19_CharaNo.xlsx", "data/TH19_database.db")
