from reflect import make_observable
from reflect_antd import Button, InputNumber, Space
from reflect_html import div
from reflect_html import h1
from reflect import Controller, make_observable
from reflect_antd import Button, Space, InputNumber, Checkbox, Card, Row, Col, Divider, Select, Radio, Typography
import numpy as np
Text = Typography.Text
import copy

necessary_score_bouts_info = { "0":56, "1":51, "2":41, "3":36 }
card_style = dict(width=500, marginTop=0)
score_factor_prise_info =  { "petite":1, "garde":2, "gardecontre":4, "gardesans":6 }

class Donne:
    def __init__(self, prise: str, bouts: list, pts_preneur: float, pts_def: float, petit_au_bout = bool, chelem = bool, display_mode = bool):
        self.prise = prise
        self.bouts = bouts
        self.pts_preneur = pts_preneur
        self.pts_def = pts_def
        self.petit_au_bout = petit_au_bout
        self.chelem = chelem
        self.display_mode = display_mode

def show_donne(donne_observable):
    contrat_objectif = lambda: "{}".format(necessary_score_bouts_info[str(len(donne_observable.bouts()))])
    #result_score_preneur = lambda: "{}".format(25 + (donne_observable.pts_preneur - int(contrat_objectif())) * score_factor_prise_info[donne_observable.prise])
    return Card([
        Space([
            donne_observable.prise(),
            donne_observable.pts_preneur(),
            #result_score_preneur,
        ]),
        Button(
                    "Modifier",
                    type="primary",
                    onClick=lambda: donne_observable.display_mode.set(False),
                    style=dict(marginTop=25)
                )
        ],
        title="Donne ({})".format(donne_observable.prise()),
        style=card_style,
        )

def edit_donne(donne_observable):
    show_result = make_observable(False)
    annonces_ckb_group = Checkbox.Group(
        Row([
                Col(Checkbox("Simple poignée (10)"), span=10),
                Col(Checkbox("Triple poignée (15)"), span=10),
                Col(Checkbox("Double poignée (13)"), span=10),
                Col(Checkbox("Grand chelem"), span=10),
            ]),
        style=dict(width="100%"),
        )
    radioPrise = Radio.Group([
                    Radio("Petite", value="petite"),
                    Radio("Garde", value="garde"),
                    Radio("Garde contre", value="gardecontre"),
                    Radio("Garde sans", value="gardesans"),],
                    value = donne_observable.prise,
                    ),
    compute_other_score = lambda s: 91 - s
    pts_preneur_input = InputNumber(
        value = donne_observable.pts_preneur, 
        min = 0,
        max = 91,
        onChange=lambda s: pts_defense_input.set(compute_other_score(s)),
        )
    pts_defense_input = InputNumber(
        value = donne_observable.pts_def, 
        min = 0,
        max = 91,
        onChange=lambda s: pts_preneur_input.set(compute_other_score(s)),
        )
    bouts_ckb_group = Checkbox.Group(
        options = ["Petit", "21", "Excuse"], 
        value = donne_observable.bouts,
        style=dict(marginLeft=28, marginTop=10)),
    contrat_objectif = necessary_score_bouts_info[str(len(bouts_ckb_group))]
    #result_score_preneur = lambda: "{}".format(25 + (20 - float(contrat_objectif)) * score_factor_prise_info[donne_observable.prise])

    return Card([
                radioPrise,
                #Space([
                #    annonces_ckb_group,
                #], style=dict(marginTop= 20)),
                Space([
                    Text("Bouts ", strong=True),
                    bouts_ckb_group,
                    div(['(contrat de ', contrat_objectif, ' pts)']),
                ], style=dict(marginTop= 20)),
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
                    style=dict(marginLeft=25, marginTop=15)
                    )
                ]),
                div([
                    Button(
                        "Calculer le score",
                        onClick=lambda: donne_observable.display_mode.set(True),
                        style=dict(marginTop=25)
                    ),
                    Button(
                        "Enregistrer",
                        type="primary",
                        onClick=lambda: donne_observable.display_mode.set(True),
                        style=dict(marginTop=25, marginLeft=20)
                    ),
                ]),
            ],
            title="Donne ({})".format(donne_observable.prise()),
            style=card_style,
            ),

def generate_donne_display(donne_observable):
    if donne_observable.display_mode():
        return show_donne(donne_observable)
    else:
        return edit_donne(donne_observable)

def app():
    blank_donne = Donne("petite", [], 0, 91, False, False, False)
    donnes_observable = make_observable([copy.copy(blank_donne)], depth=4, key="donnes")
    def create_new_donne():
        donnes_observable.append(0)
        for i in range(len(donnes_observable()), 2, -1):
            donnes_observable[i] = donnes_observable[i-1] 
        donnes_observable[0] = blank_donne
    return div(
        [
            Button(
                "+ Nouvelle donne",
                style=dict(width=150, marginTop=20, marginBottom=20),
                type="primary",
                onClick=lambda: donnes_observable.append(copy.copy(blank_donne)),
            ),
            lambda: [generate_donne_display(donne) for donne in donnes_observable],
        ],
        style={"display": "flex", "flexDirection": "column", "marginLeft":40},
        )