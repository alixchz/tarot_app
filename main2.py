from itertools import count

from reflect import Mapping, make_observable
from reflect_antd import (
    Button,
    Card,
    Checkbox,
    Col,
    InputNumber,
    Radio,
    Row,
    Space,
    Typography,
)
from reflect_html import div

Text = Typography.Text
card_style = {"width": 500, "marginTop": 20}
necessary_score_bouts_info = [56, 51, 41, 36]
score_factor_prise_info = {"petite": 1, "garde": 2, "garde_sans": 4, "garde_contre": 6}


class Donne:
    def __init__(
        self,
        id: int,
        prise: str,
        bouts: list,
        pts_preneur: float,
        pts_def: float,
        petit_au_bout=bool,
        chelem=bool,
        display_mode=bool,
    ):
        self.id = id
        self.prise = prise
        self.bouts = bouts
        self.pts_preneur = pts_preneur
        self.pts_def = pts_def
        self.petit_au_bout = petit_au_bout
        self.chelem = chelem
        self.display_mode = display_mode


def show_donne(donne_observable):
    contrat_objectif = necessary_score_bouts_info[len(donne_observable.bouts())]
    result_score_preneur = lambda: (
        25
        + (donne_observable.pts_preneur() - contrat_objectif)
        * score_factor_prise_info[donne_observable.prise()]
        + int(donne_observable.petit_au_bout())
        * 10
        * score_factor_prise_info[donne_observable.prise()]
    )
    nb_bouts = len(donne_observable.bouts())
    return Card(
        [
            div(
                [
                    Text(
                        [
                            "Contrat : {} points ({})".format(
                                contrat_objectif,
                                donne_observable.prise().replace("_", " "),
                            )
                        ]
                    ),
                    Text(
                        [
                            "Résultat : {} points avec {} bout{}".format(
                                donne_observable.pts_preneur(),
                                nb_bouts,
                                "" if nb_bouts == 1 else "s",
                            )
                        ]
                    ),
                    Text(
                        [
                            "Score : {}{} pour le preneur".format(
                                "+" if result_score_preneur() >= 0 else "",
                                result_score_preneur(),
                            )
                        ]
                    ),
                ],
                style={"display": "flex", "flexDirection": "column"},
            ),
            Button(
                "Modifier",
                type="primary",
                onClick=lambda: donne_observable.display_mode.set(False),
                style=dict(marginTop=25),
            ),
        ],
        title="Donne n°{}".format(donne_observable.id()),
        style=card_style,
    )


def edit_donne(donne_observable):
    show_result = make_observable(False)
    annonces_ckb_group = Checkbox.Group(
        Row(
            [
                Col(Checkbox("Simple poignée (10)"), span=10),
                Col(Checkbox("Triple poignée (15)"), span=10),
                Col(Checkbox("Double poignée (13)"), span=10),
                Col(Checkbox("Grand chelem"), span=10),
            ]
        ),
        style=dict(width=150),
    )
    petit_au_bout_ckb = Checkbox(
        "Petit au bout", checked=donne_observable.petit_au_bout
    )
    chelem_ckb = Checkbox("Chelem", checked=donne_observable.chelem)
    radioPrise = Radio.Group(
        [
            Radio("Petite", value="petite"),
            Radio("Garde", value="garde"),
            Radio("Garde sans", value="garde_sans"),
            Radio("Garde contre", value="garde_contre"),
        ],
        value=donne_observable.prise,
    )
    compute_other_score = lambda s: 91 - s if s else ""
    pts_preneur_input = InputNumber(
        value=donne_observable.pts_preneur,
        min=0,
        max=91,
        onChange=lambda s: pts_defense_input.set(compute_other_score(s)),
    )
    pts_defense_input = InputNumber(
        value=donne_observable.pts_def,
        min=0,
        max=91,
        onChange=lambda s: pts_preneur_input.set(compute_other_score(s)),
    )
    contrat_objectif = (
        lambda: f"(contrat de {necessary_score_bouts_info[len(donne_observable.bouts())]} pts)"
    )
    # result_score_preneur = lambda: "{}".format(25 + (20 - float(contrat_objectif)) * score_factor_prise_info[donne_observable.prise])

    return (
        Card(
            [
                radioPrise,
                Space(
                    [
                        Text("Bouts ", strong=True),
                        Checkbox.Group(
                            options=["Petit", "21", "Excuse"],
                            value=donne_observable.bouts,
                            style=dict(marginLeft=28, marginTop=10),
                        ),
                        div(contrat_objectif),
                    ],
                    style=dict(marginTop=20),
                ),
                Space(
                    [
                        Text("Points ", strong=True),
                        Row(
                            [
                                Col(div("Preneur"), className="gutter-row", span=10),
                                Col(div("Défense"), className="gutter-row", span=10),
                                Col(
                                    div(pts_preneur_input),
                                    className="gutter-row",
                                    span=10,
                                ),
                                Col(
                                    div(pts_defense_input),
                                    className="gutter-row",
                                    span=10,
                                ),
                            ],
                            gutter=[0, 0],
                            align="middle",
                            style=dict(marginLeft=25, marginTop=15),
                        ),
                    ]
                ),
                Space(
                    [
                        Text("Bonus ", strong=True),
                        petit_au_bout_ckb,
                        chelem_ckb,
                    ],
                    style=dict(marginTop=15),
                ),
                div(
                    [
                        # Button(
                        #    "Calculer le score",
                        #    onClick=lambda: donne_observable.display_mode.set(True),
                        #    style=dict(marginTop=25)
                        # ),
                        Button(
                            "Valider",
                            type="primary",
                            onClick=lambda: donne_observable.display_mode.set(True),
                            style=dict(marginTop=25, marginLeft=20),
                        ),
                    ]
                ),
            ],
            title="Donne n°{}".format(donne_observable.id()),
            style=card_style,
        ),
    )


def generate_donne_display(donne_observable):
    return (show_donne if donne_observable.display_mode() else edit_donne)(
        donne_observable
    )


def app():
    current_id = count(1)

    def create_new_donne():
        return Donne(next(current_id), "petite", [], 0, 91, False, False, False)

    donnes_observable = make_observable([create_new_donne()], depth=4, key="donnes")
    return div(
        [
            Mapping(generate_donne_display, donnes_observable, key="donnes_mapping"),
            Button(
                "+ Nouvelle donne",
                style=dict(width=150, marginTop=20, marginBottom=20),
                type="primary",
                onClick=lambda: donnes_observable.append(create_new_donne()),
            ),
        ],
        style={"display": "flex", "flexDirection": "column", "marginLeft": 40},
    )
