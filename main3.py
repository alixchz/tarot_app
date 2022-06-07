from dataclasses import dataclass
from functools import partial
from itertools import count
from typing import Tuple

from reflect_antd import (
    Button,
    Checkbox,
    Col,
    Input,
    InputNumber,
    Modal,
    Radio,
    Table,
    Tabs,
    Transfer,
)
from reflect_html import div
from reflect_utils.antd import centered
from reflect import js, make_observable

necessary_score_bouts_info = { "0":56, "1":51, "2":41, "3":36 }

TITLE = "Tarot"
GREEN = "green"
COLUMNS_DONNES = [
    {"title": "Donne", "dataIndex": "key"},
    {"title": "Prise", "dataIndex": "prise"},
    {"title": "Bouts", "dataIndex": "bouts"},
    {"title": "Joueurs", "dataIndex": "joueurs"},
    {"title": "Preneur", "dataIndex": "pts_preneur"},
    {"title": "Defense", "dataIndex": "pts_defense"},
    {"title": "", "dataIndex": "edit"},
]

COLUMNS_PLAYERS = [
    {"title": "Nom", "dataIndex": "name"},
    {"title": "Points", "dataIndex": "points"},
    {"title": "", "dataIndex": "edit"},
]


@dataclass
class Donne:
    key: int
    prise: str = ""
    pts_preneur: int = 91
    pts_defense: int = 0
    _bouts: Tuple[str] = ()
    _joueur_ids: Tuple[int] = (0,)

    def bouts(self):
        return ", ".join(self._bouts)

    def joueurs(self):
        joueurs = {joueur.key: joueur for joueur in App.instance().players()}
        return ", ".join(joueurs[joueur].name for joueur in self._joueur_ids)


@dataclass
class Player:
    key: int
    name: str = "John"
    points: int = 0


def create_edit_button(observable, show_panel, record):
    def callback():
        observable.set(record)
        show_panel()

    return Button("...", onClick=callback)


class Collection:
    def __init__(self, records, columns, data_type, create_edit_panel, name) -> None:
        self.records = records
        self.columns = columns
        self.data_type = data_type
        self.record_counter = count(1)
        self.edit_record_obs = make_observable(
            data_type(next(self.record_counter)), depth=2
        )
        self.edit_panel_visible = make_observable(False)
        self.hide_edit_panel = partial(self.edit_panel_visible.set, False)
        self.show_edit_panel = partial(self.edit_panel_visible.set, True)
        self.tab_panel = Tabs.TabPane(
            div(
                [
                    Table(
                        columns=self.columns,
                        dataSource=self.generate_rows,
                        pagination=False,
                    ),
                    Modal(
                        create_edit_panel(self.edit_record_obs),
                        title=lambda: f"{name} {self.edit_record_obs.key()}",
                        visible=self.edit_panel_visible,
                        onOk=self.on_edit_ok,
                        onCancel=self.hide_edit_panel,
                        closable=True,
                    ),
                ]
            ),
            key=name,
            tab=name,
        )

    def on_add_record(self):
        self.edit_record_obs.set(self.data_type(next(self.record_counter)))
        self.show_edit_panel()

    def generate_rows(self):
        return [
            dict(
                edit=create_edit_button(
                    self.edit_record_obs,
                    self.show_edit_panel,
                    record,
                ),
                **record.__dict__,
            )
            for record in self.records()
        ] + [{"edit": Button("+", onClick=self.on_add_record), "key": ""}]

    def on_edit_ok(self):
        if self.edit_record_obs.actual_data not in self.records.actual_data:
            self.records.append(self.edit_record_obs)
        self.records.touch()
        self.hide_edit_panel()


def create_donne_edit_panel(players, edit_donne_observable):
    prise = Radio.Group(
        [
            Radio("Petite", value="petite"),
            Radio("Garde", value="garde"),
            Radio("Garde contre", value="garde_contre"),
            Radio("Garde sans", value="garde_sans"),
        ],
        value=edit_donne_observable.prise,
    )
    compute_other_score = lambda s: 91 - s if s else None
    pts_preneur = InputNumber(
        value=edit_donne_observable.pts_preneur,
        min=0,
        max=91,
        onChange=lambda s: pts_defense.set(compute_other_score(s)),
        key="pts_preneur_input",
    )
    pts_defense = InputNumber(
        value=edit_donne_observable.pts_defense,
        min=0,
        max=91,
        onChange=lambda s: pts_preneur.set(compute_other_score(s)),
        key="pts_defense_input",
    )
    bouts = Checkbox.Group(
        options=["Petit", "21", "Excuse"],
        value=edit_donne_observable._bouts,
        style=dict(marginLeft=28, marginTop=10),
    )
    camps = Transfer(
        dataSource=lambda: [player.__dict__ for player in players()],
        titles=["Defense", "Attaque"],
        locale={"itemUnit": "joueur", "itemsUnit": "joueurs"},
        render=js("fetch_attribute", "name"),
        targetKeys=edit_donne_observable._joueur_ids,
        showSelectAll=False,
    )
    contrat_objectif = lambda: "{}".format(necessary_score_bouts_info[str(len(bouts()))])
    return Col(
        [
            centered(prise, style={"padding": "10px"}),
            centered(bouts, style={"padding": "10px"}),
            centered(camps, style={"padding": "10px"}),
            centered(
                ["Preneur", pts_preneur, "Defense", pts_defense],
                style={"padding": "10px"},
            ),
            centered(["Contrat ", contrat_objectif])
        ]
    )


def create_player_edit_panel(edit_player_observable):
    return Col(
        [
            centered(
                Input(value=edit_player_observable.name, placeholder="Nom du joueur"),
            )
        ]
    )


def app():
    donnes = make_observable([], depth=1)
    players = make_observable([], depth=1)
    players.append(Player(0))
    return div(
        Tabs(
            [
                Collection(
                    donnes,
                    COLUMNS_DONNES,
                    Donne,
                    partial(create_donne_edit_panel, players),
                    "Donnes",
                ).tab_panel,
                Collection(
                    players,
                    COLUMNS_PLAYERS,
                    Player,
                    create_player_edit_panel,
                    "Joueurs",
                ).tab_panel,
            ],
            style={"padding": 10},
        ),
        style={"background": GREEN, "height": "100%"},
    )
