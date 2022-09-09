# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import os
import logging
import random
from flask import Flask, request
import numpy as np

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)
moves = ['F', 'T', 'L', 'R']


def solve(pts, pt):
    x, y = pt
    idx = -1
    smallest = float("inf")
    for p in pts:
        if p[0] <= x or p[1] <= y:
            dist = abs(x - p[0]) + abs(y - p[1])
            if dist < smallest:
                idx = pts.index(p)
                smallest = dist
            elif dist == smallest:
                if pts.index(p) < idx:
                    idx = pts.index(p)
                    smallest = dist
    return idx


@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"


@app.route("/", methods=['POST'])
def move():
    # print(request.get_data())
    requestData = request.json

    ## get my location
    # print(requestData)
    location = requestData["arena"]["dims"]
    locationWidth = location[0]
    locationHeight = location[1]
    myLocation = [locationWidth, locationHeight]

    ## get location of others
    arenaState = requestData["arena"]["state"]
    closeArray = []
    me = []
    for opponents in arenaState:
        if opponents == "https://cloud-run-hackathon-python-3pwoxgszfq-uc.a.run.app":
            opponentsData = arenaState[opponents]
            opponentsWidth = opponentsData["x"]
            opponentsHeight = opponentsData["y"]
            opponentsDirection = opponentsData["direction"]
            opponentLocation = [opponentsWidth, opponentsHeight, opponentsDirection,
                                "https://cloud-run-hackathon-python-3pwoxgszfq-uc.a.run.app"]
            me.append(opponentLocation)

    myLocation = [opponentsWidth, opponentsHeight]
    myLocationDetailed = [opponentsWidth, opponentsHeight, opponentsDirection]
    print("My Location: ", myLocationDetailed)
    for opponents in arenaState:
        opponentsData = arenaState[opponents]
        opponentsWidth = opponentsData["x"]
        opponentsHeight = opponentsData["y"]
        opponentsDirection = opponentsData["direction"]
        oppenentsName = opponents
        opponentLocation = [opponentsWidth, opponentsHeight, opponentsDirection, oppenentsName]

        ## if they are with 3 squares face that direction
        if opponentLocation[0] == myLocation[0] - 3:
            closeArray.append(opponentLocation)
        elif opponentLocation[0] == myLocation[0] + 3:
            closeArray.append(opponentLocation)
        elif opponentLocation[1] == myLocation[1] - 3:
            closeArray.append(opponentLocation)
        elif opponentLocation[1] == myLocation[1] + 3:
            closeArray.append(opponentLocation)

    me = (myLocation[0], myLocation[1])
    # get closest enemy
    enemySolveArray = []
    for enemies in closeArray:
        enemy = enemies[0], enemies[1]
        enemySolveArray.append(enemy)

    closestEnemy = solve(closeArray, me)
    enemyToAttack = closeArray[closestEnemy]
    print("Closest Enemy: ", closeArray[closestEnemy])

    if enemyToAttack[2] == 'N':
        if myLocationDetailed == 'N':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                return 'T'
            else:
                return 'F'
        elif myLocationDetailed == 'S':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                return 'T'
            else:
                return 'F'
        elif myLocationDetailed == 'E':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                return 'T'
            else:
                return 'L'
        elif myLocationDetailed == 'W':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                return 'T'
            else:
                return 'R'

    elif enemyToAttack[2] == 'S':
        if myLocationDetailed == 'N':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                return 'T'
            else:
                return 'F'
        elif myLocationDetailed == 'S':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                return 'T'
            else:
                return 'L'
        elif myLocationDetailed == 'E':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                return 'T'
            else:
                return 'L'
        elif myLocationDetailed == 'W':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                return 'T'
            else:
                return 'R'

    elif enemyToAttack[2] == 'E':
        if myLocationDetailed == 'N':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                return 'T'
            else:
                return 'L'
        elif myLocationDetailed == 'S':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                return 'T'
            else:
                return 'R'
        elif myLocationDetailed == 'E':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                return 'T'
            else:
                return 'L'
        elif myLocationDetailed == 'W':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                return 'T'
            else:
                return 'L'

    elif enemyToAttack[2] == 'W':
        if myLocationDetailed == 'N':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                return 'T'
            else:
                return 'L'
        elif myLocationDetailed == 'S':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                return 'T'
            else:
                return 'R'
        elif myLocationDetailed == 'E':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                return 'T'
            else:
                return 'L'
        elif myLocationDetailed == 'W':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                return 'T'
            else:
                return 'F'

    # xarray = []
    # yarray = []
    # for enemies in closeArray:
    #     xarray.append(enemies[0])
    #     yarray.append(enemies[1])

    # xdifference = lambda xarray : abs(xarray - locationWidth)
    # xresult = min(xarray, key=xdifference)
    # print(xresult)
    # ydifference = lambda yarray: abs(yarray - locationHeight)
    # yresult = min(yarray, key=ydifference)
    # print(yresult)

    # minX = 15
    # minY = 13
    # for enemies in closeArray:
    #     if enemies[0] == xresult or enemies[1] == yresult:
    #         closestX = abs(enemies[0]- myLocation[0])
    #         closestY = abs(enemies[1]- myLocation[1])
    #         print("CloseX", closestX)
    #         print("CloseY", closestY)
    #         print("MinX", minX)
    #         print("MinY", minY)
    #         if closestX <= minX:
    #             minX = closestX
    #         elif closestX == minX:
    #             if closestY <= minY:
    #                 minY = closestY
    #                 print(minY)
    #                 print(minX)

    # TODO add your implementation here to replace the random response

    return moves[random.randrange(len(moves))]


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import os
import logging
import random
from flask import Flask, request
import numpy as np

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)
moves = ['F', 'T', 'L', 'R']


def solve(pts, pt):
    x, y = pt
    idx = -1
    smallest = float("inf")
    for p in pts:
        if p[0] <= x or p[1] <= y:
            dist = abs(x - p[0]) + abs(y - p[1])
            if dist < smallest:
                idx = pts.index(p)
                smallest = dist
            elif dist == smallest:
                if pts.index(p) < idx:
                    idx = pts.index(p)
                    smallest = dist
    return idx


@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"


@app.route("/", methods=['POST'])
def move():
    # print(request.get_data())
    requestData = request.json

    ## get my location
    # print(requestData)
    location = requestData["arena"]["dims"]
    locationWidth = location[0]
    locationHeight = location[1]
    myLocation = [locationWidth, locationHeight]

    ## get location of others
    arenaState = requestData["arena"]["state"]
    closeArray = []
    me = []
    for opponents in arenaState:
        if opponents == "https://cloud-run-hackathon-python-3pwoxgszfq-uc.a.run.app":
            opponentsData = arenaState[opponents]
            opponentsWidth = opponentsData["x"]
            opponentsHeight = opponentsData["y"]
            opponentsDirection = opponentsData["direction"]
            opponentLocation = [opponentsWidth, opponentsHeight, opponentsDirection,
                                "https://cloud-run-hackathon-python-3pwoxgszfq-uc.a.run.app"]
            me.append(opponentLocation)

    myLocation = [opponentsWidth, opponentsHeight]
    myLocationDetailed = [opponentsWidth, opponentsHeight, opponentsDirection]
    print("My Location: ", myLocationDetailed)
    for opponents in arenaState:
        opponentsData = arenaState[opponents]
        opponentsWidth = opponentsData["x"]
        opponentsHeight = opponentsData["y"]
        opponentsDirection = opponentsData["direction"]
        oppenentsName = opponents
        opponentLocation = [opponentsWidth, opponentsHeight, opponentsDirection, oppenentsName]

        ## if they are with 3 squares face that direction
        if opponentLocation[0] == myLocation[0] - 3:
            closeArray.append(opponentLocation)
        elif opponentLocation[0] == myLocation[0] + 3:
            closeArray.append(opponentLocation)
        elif opponentLocation[1] == myLocation[1] - 3:
            closeArray.append(opponentLocation)
        elif opponentLocation[1] == myLocation[1] + 3:
            closeArray.append(opponentLocation)

    me = (myLocation[0], myLocation[1])
    # get closest enemy
    enemySolveArray = []
    for enemies in closeArray:
        enemy = enemies[0], enemies[1]
        enemySolveArray.append(enemy)

    closestEnemy = solve(closeArray, me)
    enemyToAttack = closeArray[closestEnemy]
    print("Closest Enemy: ", closeArray[closestEnemy])

    if enemyToAttack[2] == 'N':
        if myLocationDetailed == 'N':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                return 'T'
            else:
                return 'F'
        elif myLocationDetailed == 'S':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                return 'T'
            else:
                return 'F'
        elif myLocationDetailed == 'E':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                return 'T'
            else:
                return 'L'
        elif myLocationDetailed == 'W':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                return 'T'
            else:
                return 'R'

    elif enemyToAttack[2] == 'S':
        if myLocationDetailed == 'N':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                return 'T'
            else:
                return 'F'
        elif myLocationDetailed == 'S':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                return 'T'
            else:
                return 'L'
        elif myLocationDetailed == 'E':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                return 'T'
            else:
                return 'L'
        elif myLocationDetailed == 'W':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                return 'T'
            else:
                return 'R'

    elif enemyToAttack[2] == 'E':
        if myLocationDetailed == 'N':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                return 'T'
            else:
                return 'L'
        elif myLocationDetailed == 'S':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                return 'T'
            else:
                return 'R'
        elif myLocationDetailed == 'E':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                return 'T'
            else:
                return 'L'
        elif myLocationDetailed == 'W':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                return 'T'
            else:
                return 'L'

    elif enemyToAttack[2] == 'W':
        if myLocationDetailed == 'N':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                return 'T'
            else:
                return 'L'
        elif myLocationDetailed == 'S':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                return 'T'
            else:
                return 'R'
        elif myLocationDetailed == 'E':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                return 'T'
            else:
                return 'L'
        elif myLocationDetailed == 'W':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                return 'T'
            else:
                return 'F'

    # xarray = []
    # yarray = []
    # for enemies in closeArray:
    #     xarray.append(enemies[0])
    #     yarray.append(enemies[1])

    # xdifference = lambda xarray : abs(xarray - locationWidth)
    # xresult = min(xarray, key=xdifference)
    # print(xresult)
    # ydifference = lambda yarray: abs(yarray - locationHeight)
    # yresult = min(yarray, key=ydifference)
    # print(yresult)

    # minX = 15
    # minY = 13
    # for enemies in closeArray:
    #     if enemies[0] == xresult or enemies[1] == yresult:
    #         closestX = abs(enemies[0]- myLocation[0])
    #         closestY = abs(enemies[1]- myLocation[1])
    #         print("CloseX", closestX)
    #         print("CloseY", closestY)
    #         print("MinX", minX)
    #         print("MinY", minY)
    #         if closestX <= minX:
    #             minX = closestX
    #         elif closestX == minX:
    #             if closestY <= minY:
    #                 minY = closestY
    #                 print(minY)
    #                 print(minX)

    # TODO add your implementation here to replace the random response

    return moves[random.randrange(len(moves))]


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import os
import logging
import random
from flask import Flask, request
import numpy as np

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)
moves = ['F', 'T', 'L', 'R']


def solve(pts, pt):
    x, y = pt
    idx = -1
    smallest = float("inf")
    for p in pts:
        if p[0] <= x or p[1] <= y:
            dist = abs(x - p[0]) + abs(y - p[1])
            if dist < smallest:
                idx = pts.index(p)
                smallest = dist
            elif dist == smallest:
                if pts.index(p) < idx:
                    idx = pts.index(p)
                    smallest = dist
    return idx


@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"


@app.route("/", methods=['POST'])
def move():
    # print(request.get_data())
    requestData = request.json

    ## get my location
    # print(requestData)
    location = requestData["arena"]["dims"]
    locationWidth = location[0]
    locationHeight = location[1]
    myLocation = [locationWidth, locationHeight]

    ## get location of others
    arenaState = requestData["arena"]["state"]
    closeArray = []
    me = []
    for opponents in arenaState:
        if opponents == "https://cloud-run-hackathon-python-3pwoxgszfq-uc.a.run.app":
            opponentsData = arenaState[opponents]
            opponentsWidth = opponentsData["x"]
            opponentsHeight = opponentsData["y"]
            opponentsDirection = opponentsData["direction"]
            opponentLocation = [opponentsWidth, opponentsHeight, opponentsDirection,
                                "https://cloud-run-hackathon-python-3pwoxgszfq-uc.a.run.app"]
            me.append(opponentLocation)

    myLocation = [opponentsWidth, opponentsHeight]
    myLocationDetailed = [opponentsWidth, opponentsHeight, opponentsDirection]
    print("My Location: ", myLocationDetailed)
    for opponents in arenaState:
        opponentsData = arenaState[opponents]
        opponentsWidth = opponentsData["x"]
        opponentsHeight = opponentsData["y"]
        opponentsDirection = opponentsData["direction"]
        oppenentsName = opponents
        opponentLocation = [opponentsWidth, opponentsHeight, opponentsDirection, oppenentsName]

        ## if they are with 3 squares face that direction
        if opponentLocation[0] == myLocation[0] - 3:
            closeArray.append(opponentLocation)
        elif opponentLocation[0] == myLocation[0] + 3:
            closeArray.append(opponentLocation)
        elif opponentLocation[1] == myLocation[1] - 3:
            closeArray.append(opponentLocation)
        elif opponentLocation[1] == myLocation[1] + 3:
            closeArray.append(opponentLocation)

    me = (myLocation[0], myLocation[1])
    # get closest enemy
    enemySolveArray = []
    for enemies in closeArray:
        enemy = enemies[0], enemies[1]
        enemySolveArray.append(enemy)

    closestEnemy = solve(closeArray, me)
    enemyToAttack = closeArray[closestEnemy]
    print("Closest Enemy: ", closeArray[closestEnemy])
    print("T")
    if enemyToAttack[2] == 'N':
        if myLocationDetailed == 'N':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                print("T")
                return 'T'
            else:
                print("F")
                return 'F'
        elif myLocationDetailed == 'S':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                print("T")
                return 'T'
            else:
                print("F")
                return 'F'
        elif myLocationDetailed == 'E':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                print("T")
                return 'T'
            else:
                print("L")
                return 'L'
        elif myLocationDetailed == 'W':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                print("T")
                return 'T'
            else:
                print("R")
                return 'R'

    elif enemyToAttack[2] == 'S':
        if myLocationDetailed == 'N':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                print("T")
                return 'T'
            else:
                print("F")
                return 'F'
        elif myLocationDetailed == 'S':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                print("T")
                return 'T'
            else:
                print("L")
                return 'L'
        elif myLocationDetailed == 'E':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                print("T")
                return 'T'
            else:
                print("L")
                return 'L'
        elif myLocationDetailed == 'W':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                print("T")
                return 'T'
            else:
                print("R")
                return 'R'

    elif enemyToAttack[2] == 'E':
        if myLocationDetailed == 'N':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                print("T")
                return 'T'
            else:
                print("L")
                return 'L'
        elif myLocationDetailed == 'S':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                print("T")
                return 'T'
            else:
                print("R")
                return 'R'
        elif myLocationDetailed == 'E':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                print("T")
                return 'T'
            else:
                print("L")
                return 'L'
        elif myLocationDetailed == 'W':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                print("T")
                return 'T'
            else:
                print("L")
                return 'L'

    elif enemyToAttack[2] == 'W':
        if myLocationDetailed == 'N':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                print("T")
                return 'T'
            else:
                print("L")
                return 'L'
        elif myLocationDetailed == 'S':
            if enemyToAttack[1] < myLocationDetailed[1] - 3:
                print("T")
                return 'T'
            else:
                print("R")
                return 'R'
        elif myLocationDetailed == 'E':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                print("T")
                return 'T'
            else:
                print("L")
                return 'L'
        elif myLocationDetailed == 'W':
            if enemyToAttack[0] < myLocationDetailed[0] - 3:
                print("T")
                return 'T'
            else:
                print("F")
                return 'F'

    # xarray = []
    # yarray = []
    # for enemies in closeArray:
    #     xarray.append(enemies[0])
    #     yarray.append(enemies[1])

    # xdifference = lambda xarray : abs(xarray - locationWidth)
    # xresult = min(xarray, key=xdifference)
    # print(xresult)
    # ydifference = lambda yarray: abs(yarray - locationHeight)
    # yresult = min(yarray, key=ydifference)
    # print(yresult)

    # minX = 15
    # minY = 13
    # for enemies in closeArray:
    #     if enemies[0] == xresult or enemies[1] == yresult:
    #         closestX = abs(enemies[0]- myLocation[0])
    #         closestY = abs(enemies[1]- myLocation[1])
    #         print("CloseX", closestX)
    #         print("CloseY", closestY)
    #         print("MinX", minX)
    #         print("MinY", minY)
    #         if closestX <= minX:
    #             minX = closestX
    #         elif closestX == minX:
    #             if closestY <= minY:
    #                 minY = closestY
    #                 print(minY)
    #                 print(minX)



    # return moves[random.randrange(len(moves))]


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

