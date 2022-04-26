from reflect_html import h1
from reflect import Controller, make_observable
from reflect_antd import Button, Space, InputNumber, Checkbox, Card, Row, Col, Divider, Select, Radio, Typography
from reflect_html import div
import numpy as np

Text = Typography.Text
score_factor_prise_info =  { "petite":1, "garde":2, "gardecontre":4, "gardesans":6 }
necessary_score_bouts_info = { "0":56, "1":51, "2":41, "3":36 }

def getType(score):
    score = float(score)
    if score > 0:
        return "success"
    if score == 0:
        return "warning"
    else:
        return "danger"

def app():
    style = {"width": 300, "marginTop": 10}
    styleInputs = dict(width=90)
    styleBtns = dict(width=200)
    prise_value = make_observable("petite", key="test")
    pts_preneur = make_observable(0, key="pts_preneur")
    pts_preneur_input = InputNumber(value = pts_preneur, style=styleInputs, key="pts_preneur")
    #pts_defense_input = InputNumber(value = pts_defense, style=styleInputs, key="pts_defense")
    bouts_ckb_group = Checkbox.Group(options=["Petit", "21", "Excuse"], defaultValue=[])
    #score_objectif = 
    radioPrise = Radio.Group([
                    Radio("Petite", value="petite"),
                    Radio("Garde", value="garde"),
                    Radio("Garde contre", value="gardecontre"),
                    Radio("Garde sans", value="gardesans"),],
                    #defaultValue="prise",
                    value = prise_value,
                    ),
    with Controller() as controller:
        btn_OK = Button("OK", onClick=controller.commit, type="primary", style=styleBtns),
        btn_cancel = Button("Annuler", onClick=controller.revert, style=styleBtns),
        #nb_bouts = lambda: "{}".format(len(bouts_ckb_group()))
        contrat_objectif = lambda: "{}".format(necessary_score_bouts_info[str(len(bouts_ckb_group()))])
        result_score_preneur = lambda: "{}".format(25 + (pts_preneur() - int(contrat_objectif())) * score_factor_prise_info[prise_value()])
        #select_result = lambda: "{}".format(score_factor_prise_info[prise_value()])
    return Space(
        [   
            Card([
                radioPrise,
                Space([
                    Text("Bouts ", strong=True),
                    bouts_ckb_group,
                    div(['(contrat de ', contrat_objectif, ' pts)']),
                ], style=dict(marginTop= 10)),
                Row(
                    [
                        Col(div("Points du preneur", style=style), className="gutter-row", span=8),
                        Col(div(pts_preneur_input, style=style), className="gutter-row", span=10),
                        #Col(div("Points de la défense", style=style), className="gutter-row", span=8),
                        #Col(div(pts_defense_input, style=style), className="gutter-row", span=10),
                    ],
                    gutter=[8, 8],
                    align="middle",
                    ),
            ],
            title="Informations de la donne côté preneur",
            style=dict(width=500, marginTop=10),
            ),
            Space(
                    [
                        btn_OK,
                        div("*", style={"color": "#FFFFFF"}),
                        btn_cancel,
                    ],
                    style=dict(width=500, marginTop=10, marginBottom=70),
                    ),
            #div(['Contrat du preneur : ', contrat_objectif, ' pts']),
            Card([
                div(['Résultat du preneur : ', result_score_preneur, ' pts'])
            ],
            title="Résultats",
            style=dict(maginTop=100)
            )
        ],
        style={"display": "flex", "flexDirection": "column"},
    )

