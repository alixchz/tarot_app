from reflect_html import h1
from reflect import Controller, make_observable
from reflect_antd import Button, Space, InputNumber, Checkbox, Card
from reflect_html import div

def app():
    style = {"width": 90}
    with Controller() as controller:
        pts_preneur = make_observable(0, key="value")
        pts_preneur_input = InputNumber(value = pts_preneur, style=style, key="Entrez le score de l'attaque :")
        pts_defense_input = InputNumber(value = pts_preneur, style=style, key="Entrez le score de l'attaque :")
        formula = lambda: "{}".format(a() * b())

        return Space(
            [   
                Card([
                    Checkbox("Petit", style=style),
                    Checkbox("21", onChange=controller.commit, style=style),
                    Checkbox("Excuse", onChange=controller.commit, style=style),
                    Space(["Score du preneur :", pts_preneur_input]),
                    Space(["Score de la défense :", pts_defense_input]),
                    Space(
                        [
                            Button("OK", onClick=controller.commit, style=style),
                            div("*", style={"color": "#FFFFFF"}),
                            Button("Annuler", onClick=controller.revert, style=style),
                        ],
                        style=dict(marginTop=10),
                        ),
                ],
                title="Informations de la partie",
                style=dict(width=500, marginTop=10),
                )
            ],
            style={"display": "flex", "flexDirection": "column"},
        )

