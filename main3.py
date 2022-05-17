from reflect_antd import (
    Button,
    InputNumber,
    Modal,
    Table,
    Checkbox,
    Col,
    Radio,
    Tabs,
    pagination,
)
from reflect_html import div
from itertools import count, chain
from reflect import make_observable
from reflect_utils.antd import create_form_row

COLUMNS_DONNES = [
    {"title": "Donne", "dataIndex": "key"},
    {"title": "Prise", "dataIndex": "prise"},
    {"title": "Bouts", "dataIndex": "bouts"},
    {"title": "Preneur", "dataIndex": "pts_preneur"},
    {"title": "Defense", "dataIndex": "pts_defense"},
    {"title": "", "dataIndex": "edit"},
]

COLUMNS_PLAYERS = [
    {"title": "Nom", "dataIndex": "key"},
    {"title": "Points", "dataIndex": "points"},
]

TITLE = "Tarot"


class Donne:
    def __init__(self, key) -> None:
        self.prise = ""
        self.bouts = []
        self.pts_preneur = 91
        self.pts_defense = 0
        self.key = key

    def to_dict(self):
        return dict(
            chain(
                ((k, v) for k, v in self.__dict__.items() if k != "bouts"),
                (("bouts", ", ".join(self.bouts)),),
            )
        )


class Player:
    def __init__(self):
        self.key = "test"
        self.points = 0


def update_dict(d, **kwargs):
    return dict(chain(d.items(), kwargs.items()))


class App:
    def __init__(self) -> None:
        self.donnes = make_observable([], depth=1)
        self.show_edit_donne = make_observable(False, key="show_edit_donne")
        self.edit_donne_observable = make_observable(Donne(0), key="show_edit_donne")
        self.donne_counter = count(1)
        self.players = make_observable([Player()], depth=1)

    def create_callback(self, donne):
        def callback():
            self.edit_donne_observable.reset(donne)
            self.show_panel()

        return callback

    def generate_rows_donne(self):
        return [
            update_dict(
                donne.to_dict(), edit=Button("...", onClick=self.create_callback(donne))
            )
            for donne in self.donnes()
        ] + [{"edit": Button("+", onClick=self.on_add), "key": ""}]

    def generate_rows_players(self):
        return [player.__dict__ for player in self.players()]

    def hide_panel(self):
        self.show_edit_donne.set(False)

    def show_panel(self):
        self.show_edit_donne.set(True)

    def on_ok(self):
        if self.edit_donne_observable.obj not in self.donnes():
            self.donnes.append(self.edit_donne_observable.obj)
        self.donnes.touch()
        self.hide_panel()

    def on_add(self):
        self.edit_donne_observable.reset(Donne(next(self.donne_counter)))
        self.show_panel()

    def content(self):
        prise = Radio.Group(
            [
                Radio("Petite", value="petite"),
                Radio("Garde", value="garde"),
                Radio("Garde contre", value="garde_contre"),
                Radio("Garde sans", value="garde_sans"),
            ],
            value=self.edit_donne_observable.prise,
        )
        compute_other_score = lambda s: 91 - s if s else None
        pts_preneur = InputNumber(
            value=self.edit_donne_observable.pts_preneur,
            min=0,
            max=91,
            onChange=lambda s: pts_defense.set(compute_other_score(s)),
            key="pts_preneur_input",
        )
        pts_defense = InputNumber(
            value=self.edit_donne_observable.pts_defense,
            min=0,
            max=91,
            onChange=lambda s: pts_preneur.set(compute_other_score(s)),
            key="pts_defense_input",
        )
        bouts = Checkbox.Group(
            options=["Petit", "21", "Excuse"],
            value=self.edit_donne_observable.bouts,
            style=dict(marginLeft=28, marginTop=10),
        )
        return Tabs(
            [
                Tabs.TabPane(
                    div(
                        [
                            Table(
                                columns=COLUMNS_DONNES,
                                dataSource=self.generate_rows_donne,
                                pagination=False,
                            ),
                            Modal(
                                Col(
                                    [
                                        create_form_row("Prise", prise),
                                        create_form_row("Preneur", pts_preneur),
                                        create_form_row("Defense", pts_defense),
                                        create_form_row("Bouts", bouts),
                                    ]
                                ),
                                title=lambda: f"Donne {self.edit_donne_observable.key()}",
                                visible=self.show_edit_donne,
                                onOk=self.on_ok,
                                onCancel=self.hide_panel,
                                closable=True,
                            ),
                        ]
                    ),
                    key="Donnes",
                    tab="Donnes",
                ),
                Tabs.TabPane(
                    div(
                        [
                            Table(
                                columns=COLUMNS_PLAYERS,
                                dataSource=self.generate_rows_players,
                                pagination=False,
                            )
                        ]
                    ),
                    key="Joueurs",
                    tab="Joueurs",
                ),
            ]
        )
