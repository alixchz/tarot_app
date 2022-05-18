from dataclasses import dataclass
from functools import partial
from itertools import chain, count
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
from reflect_utils.antd import create_form_row
from reflect import js, make_observable

TITLE = "Tarot"

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


def obj_attributes(obj):
    """like obj.__dict__.items(), but for the fact that it also returns dataclass bound methods"""
    return ((name, getattr(obj, name)) for name in dir(obj))


def to_dict(record):
    return {
        k: (v() if callable(v) else v)
        for k, v in obj_attributes(record)
        if not k.startswith("_")
    }


def update_dict(d, **kwargs):
    return dict(chain(d.items(), kwargs.items()))


@dataclass
class Donne:
    key: int
    prise: str = ""
    _bouts: Tuple[str] = ()
    pts_preneur: int = 91
    pts_defense: int = 0
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


class App:
    def __init__(self) -> None:
        self.donne_counter = count()
        self.player_counter = count()
        self.edit_donne_observable = make_observable(Donne(next(self.donne_counter)))
        self.edit_player_observable = make_observable(Player(next(self.player_counter)))
        self.donnes = make_observable([], depth=1)
        self.players = make_observable([self.edit_player_observable.obj], depth=1)
        self.show_edit_donne = make_observable(False, key="show_edit_donne")
        self.show_edit_player = make_observable(False, key="show_edit_player")
        self.hide_donne_panel = partial(self.show_edit_donne.set, False)
        self.show_donne_panel = partial(self.show_edit_donne.set, True)
        self.hide_player_panel = partial(self.show_edit_player.set, False)
        self.show_player_panel = partial(self.show_edit_player.set, True)

    def create_edit_button(self, observable, show_panel, donne):
        def callback():
            observable.set(donne)
            show_panel()

        return Button("...", onClick=callback)

    def generate_rows_donne(self):
        return [
            update_dict(
                to_dict(donne),
                edit=self.create_edit_button(
                    self.edit_donne_observable,
                    self.show_donne_panel,
                    donne,
                ),
            )
            for donne in self.donnes()
        ] + [{"edit": Button("+", onClick=self.on_add_donne), "key": ""}]

    def generate_rows_players(self):
        return [
            update_dict(
                player.__dict__,
                edit=self.create_edit_button(
                    self.edit_player_observable,
                    self.show_player_panel,
                    player,
                ),
            )
            for player in self.players()
        ] + [{"edit": Button("+", onClick=self.on_add_player), "key": ""}]

    def on_donne_ok(self):
        if self.edit_donne_observable.obj not in self.donnes():
            self.donnes.append(self.edit_donne_observable.obj)
        self.donnes.touch()
        self.hide_donne_panel()

    def on_add_donne(self):
        self.edit_donne_observable.set(Donne(next(self.donne_counter)))
        self.show_donne_panel()

    def on_add_player(self):
        self.edit_player_observable.set(Player(next(self.player_counter)))
        self.show_player_panel()

    def on_player_ok(self):
        if self.edit_player_observable.obj not in self.players():
            self.players.append(self.edit_player_observable.obj)
        self.players.touch()
        self.hide_player_panel()

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
            value=self.edit_donne_observable._bouts,
            style=dict(marginLeft=28, marginTop=10),
        )
        player_name = (
            Input(value=self.edit_player_observable.name, placeholder="Nom du joueur"),
        )
        players = lambda: [player.__dict__ for player in self.players()]
        camps = Transfer(
            dataSource=players,
            titles=["Defense", "Attaque"],
            locale={"itemUnit": "joueur", "itemsUnit": "joueurs"},
            render=js("fetch_attribute", "name"),
            targetKeys=self.edit_donne_observable._joueur_ids,
            showSelectAll=False,
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
                                        create_form_row("Camps", camps),
                                    ]
                                ),
                                title=lambda: f"Donne {self.edit_donne_observable.key()}",
                                visible=self.show_edit_donne,
                                onOk=self.on_donne_ok,
                                onCancel=self.hide_donne_panel,
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
                            ),
                            Modal(
                                Col(
                                    [
                                        create_form_row("Nom", player_name),
                                    ]
                                ),
                                title=lambda: f"Joueur {self.edit_player_observable.name()}",
                                visible=self.show_edit_player,
                                onOk=self.on_player_ok,
                                onCancel=self.hide_player_panel,
                                closable=True,
                            ),
                        ]
                    ),
                    key="Joueurs",
                    tab="Joueurs",
                ),
            ]
        )
