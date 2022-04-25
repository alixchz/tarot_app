from reflect_html import h1
from reflect import Controller, make_observable
from reflect_antd import Button, Space, InputNumber, Checkbox, Card, Row, Col, Divider, Select, Radio
from reflect_html import div

score_factor_prise_info =  { "prise":1, "garde":2, "gardecontre":4, "gardesans":6 }

def app():
    style = {"width": 300, "marginTop": 10}
    styleInputs = dict(width=90)
    styleBtns = dict(width=200)
    prise_value = make_observable("prise", key="test")
    pts_preneur = make_observable(0, key="pts_preneur")
    pts_defense = make_observable(91, key="pts_defense")
    pts_preneur_input = InputNumber(value = pts_preneur, style=styleInputs, key="pts_preneur")
    pts_defense_input = InputNumber(value = pts_defense, style=styleInputs, key="pts_defense")
    radioPrise = Radio.Group([
                    Radio("Prise", value="prise"),
                    Radio("Garde", value="garde"),
                    Radio("Garde contre", value="gardecontre"),
                    Radio("Garde sans", value="gardesans"),
                    ],
                    #defaultValue="prise",
                    value = prise_value,
                    ),
    with Controller() as controller:
        btn_OK = Button("OK", onClick=controller.commit, type="primary", style=styleBtns),
        btn_cancel = Button("Annuler", onClick=controller.revert, style=styleBtns),
        result_score_preneur = lambda: "{}".format(pts_preneur() * score_factor_prise_info[prise_value()])
        #select_result = lambda: "{}".format(score_factor_prise_info[prise_value()])
    return Space(
        [   
            Card([
                radioPrise,
                div([
                    'Bouts du preneur : ',
                    Checkbox("Petit"),
                    Checkbox("21"),
                    Checkbox("Excuse"),
                ], style=dict(marginTop= 10)),
                Row(
                    [
                        Col(div("Points du preneur", style=style), className="gutter-row", span=8),
                        Col(div(pts_preneur_input, style=style), className="gutter-row", span=10),
                        Col(div("Points de la défense", style=style), className="gutter-row", span=8),
                        Col(div(pts_defense_input, style=style), className="gutter-row", span=10),
                    ],
                    gutter=[8, 8],
                    align="middle",
                    ),
            ],
            title="Informations de la partie",
            style=dict(width=500, marginTop=10),
            ),
            Space(
                    [
                        btn_OK,
                        div("*", style={"color": "#FFFFFF"}),
                        btn_cancel,
                    ],
                    style=dict(width=500, marginTop=10),
                    ),
            div(['Score du preneur : ', result_score_preneur]),
        ],
        style={"display": "flex", "flexDirection": "column"},
    )

