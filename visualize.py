from cmu_112_graphics import *
import pandas as pd
import numpy as np
import tkinter as tk
from datetime import date
from sportsreference.nfl.boxscore import Boxscores

today = date.today()

def appStarted(app):
    app.margin = 20
    today = date.today()
    app.year = today.year
    app.week = 9
    app.button1X1, app.button1X2, app.button1Y1, app.button1Y2 = (app.margin, app.margin + 80, app.margin + 100, app.margin + 130)
    app.button2X1, app.button2X2, app.button2Y1, app.button2Y2 = (app.margin + 100, app.margin + 180, app.margin + 100, app.margin + 130)
    app.buttonTakingInput = {1:False, 2:False}
    app.currentWeek = getCurrentWeek()
    app.df = weekBoxScores(app.currentWeek, app.year)

def getCurrentWeek():
    year = date.today().year
    for week in range(17, 0, -1):
        df = weekBoxScores(week, year)
        if df.iloc[0]['away_score'] != None or df.iloc[0]['home_score'] != None:
            return week
    return 0

def weekBoxScores(week, year):
    try:
        gamesOnDay = Boxscores(week, year)
    except:
        return 0
    gameValues = gamesOnDay.games.values()
    gameValuesIterator = iter(gameValues)
    gamesDictList = next(gameValuesIterator)
    return pd.DataFrame(gamesDictList)

def createInputBox(app, canvas, x0, x1, y0, y1, txt, num):
    if app.buttonTakingInput[num]: color = "blue"
    else: color = "red"
    canvas.create_rectangle(x0,x1,y0,y1,fill=color)
    canvas.create_text((x0 + x1)//2, (y0 + y1)//2, text=txt,fill="white",font="Montserrat 12")

def createGrids(app, canvas, rows, cols, x0, y0, x1, y1, margins):
    cellWidth = (abs(x0 - x1)) // cols
    cellHeight = (abs(y0 - y1)) // rows
    for row in range(rows):
        for col in range(cols):
            cellX0, cellY0 = x0 + col * cellWidth, y0 + row * cellHeight
            cellX1, cellY1 = cellX0 + cellWidth, cellY0 + cellHeight
            canvas.create_rectangle(cellX0 + margins, cellY0 + margins, cellX1 - margins, cellY1 - margins, fill="lightGreen")

def outputScores(app, canvas, rows, cols, x0, y0, x1, y1, margins):
    cellWidth = (abs(x0 - x1)) // cols
    cellHeight = (abs(y0 - y1)) // rows
    for row in range(rows):
        for col in range(cols):
            cellX0, cellY0 = x0 + col * cellWidth, y0 + row * cellHeight
            cellX1, cellY1 = cellX0 + cellWidth, cellY0 + cellHeight
            index = row * cols + col
            homeScore, awayScore = app.df.iloc[index]['home_score'], app.df.iloc[index]['away_score']
            homeName, awayName = app.df.iloc[index]['home_name'], app.df.iloc[index]['away_name']
            if pd.isna(homeScore): homeScore = '-'
            if pd.isna(awayScore): awayScore = '-'
            canvas.create_text(cellX0 + app.margin + margins, cellY0 + abs(cellY0 - \
                cellY1) // 2, anchor="w", text=f"{homeName} ({homeScore}) vs. {awayName} ({awayScore})", font="Montserrat 16", fill="black")

def redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill="black")
    canvas.create_text(app.width // 2, app.margin, text="varnothing NFL Projector", font="Montserrat 20", fill="white")
    canvas.create_text(app.margin, app.margin + 50, text="NFL Scoreboard and Projections", font="Montserrat 40", fill="lightGreen", anchor="w")
    canvas.create_text(app.margin, app.margin + 100, text=f"Current week: {app.currentWeek}", font="Montserrat 20", fill="white", anchor="w")
    createGrids(app, canvas, 7, 2, app.margin, 140, app.width - app.margin, app.height - app.margin, 5)
    outputScores(app, canvas, 7, 2, app.margin, 140, app.width - app.margin, app.height - app.margin, 5)

#################################################
# main
#################################################

runApp(width=1280, height=720)

def main():
    pass

if __name__ == '__main__':
    main()