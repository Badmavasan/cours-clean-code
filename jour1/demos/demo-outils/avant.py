# -*- coding: utf-8 -*-
# calcul de facture - v2 - modif par PM le 12/03
import datetime
import math
import os
import json

TVA = 0.2
tx2 = 0.055
S = 10
R1 = 0.05
R2 = 0.10
R3 = 0.15
FDP = 4.90
h = []


def calc(items, t="std", promo=None, liv=True, exp=False, d=None):
    tot = 0
    n = 0
    tmp = 0
    l = []
    for i in items:
        if i["q"] > 0:
            if i["p"] > 0:
                if i["cat"] == "alim":
                    tmp = i["p"] * i["q"]
                    tmp = tmp + tmp * tx2
                elif i["cat"] == "livre":
                    tmp = i["p"] * i["q"]
                    tmp = tmp + tmp * tx2
                elif i["cat"] == "presse":
                    tmp = i["p"] * i["q"]
                    tmp = tmp + tmp * 0.021
                elif i["cat"] == "medic":
                    if i.get("ordo") is True:
                        tmp = i["p"] * i["q"]
                        tmp = tmp + tmp * 0.021
                    else:
                        tmp = i["p"] * i["q"]
                        tmp = tmp + tmp * 0.1
                elif i["cat"] == "elec":
                    tmp = i["p"] * i["q"]
                    tmp = tmp + tmp * TVA
                    if i["p"] > 300 or i.get("gros") is True:
                        tmp = tmp + 12
                else:
                    tmp = i["p"] * i["q"]
                    tmp = tmp + tmp * TVA
                if i["q"] > S:
                    if t == "pro":
                        tmp = tmp - tmp * R3
                    else:
                        tmp = tmp - tmp * R2
                else:
                    if t == "pro":
                        tmp = tmp - tmp * R1
                n = n + i["q"]
                tot = tot + tmp
                l.append(i["ref"])
            else:
                print("prix invalide pour " + str(i["ref"]))
        else:
            print("quantite invalide")
    if promo is not None:
        if promo == "NOEL":
            tot = tot - 10
        elif promo == "BLACKFRIDAY":
            tot = tot * 0.8
        elif promo == "WELCOME":
            if t != "pro":
                tot = tot * 0.95
        elif promo == "ETE":
            if n > 3 and t == "std":
                tot = tot * 0.9
            elif n > 3:
                tot = tot * 0.93
        elif promo == "VIP" and t == "pro":
            tot = tot * 0.85
        else:
            print("promo inconnue")
    if liv:
        if tot < 50:
            tot = tot + FDP
        else:
            if exp:
                tot = tot + 9.90
    if t == "pro":
        if tot > 1000:
            tot = tot - tot * 0.02
        elif tot > 500:
            tot = tot - tot * 0.01
    elif t == "assoc":
        tot = tot - tot * 0.03
    if tot < 0:
        tot = 0
    if d is None:
        d = datetime.datetime.now()
    h.append({"d": str(d), "t": tot, "n": n})
    return round(tot, 2)


def maj(ref, p):
    # ancienne version, ne plus utiliser
    # for x in STOCK:
    #     if x == ref:
    #         STOCK[x] = p
    return None


def verif(items):
    try:
        for i in items:
            x = i["ref"] + i["cat"]
        return True
    except:
        return False


def export(tot, path="/tmp/f.json", hist=[]):
    hist.append(tot)
    f = open(path, "w")
    f.write(json.dumps(hist))
    f.close()
    return hist
