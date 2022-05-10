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
    donnes = make_observable([], depth=3, key="donnes")
    show_result = make_observable(False)
    styleBtns = dict(width=200)
    prise_value = make_observable("petite", key="test")
    compute_other_score = lambda s: 91 - s
    pts_preneur_input = InputNumber(
        defaultValue = 0, 
        min = 0,
        max = 91,
        onChange=lambda s: pts_defense_input.set(compute_other_score(s)),
        )
    pts_defense_input = InputNumber(
        defaultValue = 91, 
        min = 0,
        max = 91,
        onChange=lambda s: pts_preneur_input.set(compute_other_score(s)),
        )
    bouts_ckb_group = Checkbox.Group(options=["Petit", "21", "Excuse"], defaultValue=[], style=dict(marginLeft=28))
    annonces_ckb_group = Checkbox.Group(
        Row([
                Col(Checkbox("Simple poignée (10)"), span=10),
                Col(Checkbox("Triple poignée (15)"), span=10),
                Col(Checkbox("Double poignée (13)"), span=10),
                Col(Checkbox("Grand chelem"), span=10),
            ]),
        style=dict(width="100%"),
        )
    results_ckb_group = Checkbox.Group(options=["Petit au bout","Grand chelem"], defaultValue=[], style=dict(marginTop=20))
    radioPrise = Radio.Group([
                    Radio("Petite", value="petite"),
                    Radio("Garde", value="garde"),
                    Radio("Garde contre", value="gardecontre"),
                    Radio("Garde sans", value="gardesans"),],
                    #defaultValue="prise",
                    value = prise_value,
                    ),
    contrat_objectif = lambda: "{}".format(necessary_score_bouts_info[str(len(bouts_ckb_group()))])
    btn_OK = Button("OK", onClick=show_result.set(True), type="primary", style=styleBtns),
    btn_cancel = Button("Réinitialiser", onClick=show_result.set(False), style=styleBtns),
    result_score_preneur = lambda: "{}".format(25 + (pts_preneur_input() - int(contrat_objectif())) * score_factor_prise_info[prise_value()])
    result_card = Card([
            div(['Résultat du preneur : ', result_score_preneur, ' pts'])
        ],
        title="Résultats",
        style=dict(maginTop=50)
        ) 
    return Space(
        [   
            Card([
                radioPrise,
                Space([
                    annonces_ckb_group,
                ], style=dict(marginTop= 20)),
            ],
            title="Annonces",
            style=dict(width=500, marginTop=10),
            ),
            Card([
                Space([
                    Text("Bouts ", strong=True),
                    bouts_ckb_group,
                    div(['(contrat de ', contrat_objectif, ' pts)']),
                ], style=dict(marginTop= 0)),
                Space([
                    Text("Points ", strong=True),
                    Row([
                        Col(div("Preneur"), className="gutter-row", span=10),
                        Col(div("Défense"), className="gutter-row", span=10),
                        Col(div(pts_preneur_input), className="gutter-row", span=10),
                        Col(div(pts_defense_input), className="gutter-row", span=10),
                    ],
                    gutter=[0, 0],
                    align="middle",
                    style=dict(marginLeft=25, marginTop=10)
                    )
                ]),
                results_ckb_group,
                ],
            title="Fin de donne",
            style=dict(width=500, marginTop=10),
            ),
            Space(
                    [
                        btn_OK,
                        div("*", style={"color": "#FFFFFF"}),
                        btn_cancel,
                        div([show_result()]),
                    ],
                    style=dict(width=500, marginTop=10, marginBottom=70),
                    ),
            result_card,
        ],
        style={"display": "flex", "flexDirection": "column"},
    )

