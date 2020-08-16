from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import itertools
import random
from django.utils.safestring import mark_safe
import django.forms

author = 'Moritz Gottschling, Anne Mensing, Julia Lauten, Kateryna Kuian'

doc = """
This is the source code for the experiment for our bms seminar paper 2020.
"""


class Constants(BaseConstants):
    name_in_url = 'bms_experiment'
    players_per_group = None
    num_rounds = 2

    labels = {
        'age': 'Age:',
        'gender': 'Gender:',
        'installed': 'Have you installed the corona-warn-app?',
        'competence': 'The app will be able to keep your personal data secured.',
        'competence_neg': 'The app <strong>lacks</strong> the necessary competence to protect your data.',
        'benevolence': 'The app was made to collect your personal data.',
        'benevolence_neg': 'The app acts in your interest.',

        'no_central_entity': 'The app does <strong>not</strong> store my personal data on a central server.',
        'no_central_entity_neg': 'The personal data of mine is stored by the app on a central server.',
        'anonymity': 'The app does <strong>not</strong> allow other users to access/view my personal data.',
        'anonymity_neg': 'My personal data can be accessed/viewed by other users of the app.',
        'no_tracking': 'The app will track my location and collect personal data on my phone.',
        'no_tracking_neg': 'My location and personal data from my phone can <strong>not</strong> be collected by the '
                           'app.',
        'unlinkabilty': 'The app prevents linking back the collected data to my person.',
        'unlinkabilty_neg': 'Using the app it is possible to link the collected data back to my person.',

        'activity': 'What does the app do while being active?',
        'data_stored': 'What data does the app store?',
        'warnings': 'When are warnings given?',
        'infected': 'What happens when you had contact with an infected person.'

    }


class Subsession(BaseSubsession):
    def creating_session(self):
        # randomize to treatments
        transparency_conditions = itertools.cycle(['no', 'brief', 'detailed'])
        for player in self.get_players():
            player.trans_cond = next(transparency_conditions)


class Group(BaseGroup):
    pass


def make_radio(label):
    return models.IntegerField(
        choices=[
            [1, 'Totally Disagree'],
            [2, 'Disagree'],
            [3, 'Undecided'],
            [4, 'Agree'],
            [5, 'Totally Agree'],
        ],
        label=mark_safe(label),
        widget=widgets.RadioSelectHorizontal,
    )


def make_open(label):
    return models.StringField(
        label=mark_safe(label),
        widget=django.forms.Textarea(attrs={
            'rows': 5,
            'cols': 5,
        })
    )


class Player(BasePlayer):
    # automatically selected
    trans_cond = models.StringField();

    # general information
    age = models.IntegerField(label=Constants.labels['age'])
    gender = models.IntegerField(
        choices=random.sample([
            [0, 'Female'],
            [1, 'Male'],
            [2, 'Diverse'],
        ], 3),
        max=99,
        min=0,
        widget=widgets.RadioSelectHorizontal
    )
    installed = models.BooleanField(label=Constants.labels['installed'], widget=widgets.RadioSelectHorizontal)

    # trust
    competence = make_radio(Constants.labels['competence'])
    competence_neg = make_radio(Constants.labels['competence_neg'])
    # benevolence
    benevolence = make_radio(Constants.labels['benevolence'])
    benevolence_neg = make_radio(Constants.labels['benevolence_neg'])

    # integrity
    no_central_entity = make_radio(Constants.labels['no_central_entity'])
    no_central_entity_neg = make_radio(Constants.labels['no_central_entity_neg'])
    anonymity = make_radio(Constants.labels['anonymity'])
    anonymity_neg = make_radio(Constants.labels['anonymity_neg'])
    no_tracking = make_radio(Constants.labels['no_tracking'])
    no_tracking_neg = make_radio(Constants.labels['no_tracking_neg'])
    unlinkabilty = make_radio(Constants.labels['unlinkabilty'])
    unlinkabilty_neg = make_radio(Constants.labels['unlinkabilty_neg'])

    activity = make_open(Constants.labels['activity'])
    data_stored = make_open(Constants.labels['data_stored'])
    warnings = make_open(Constants.labels['warnings'])
    infected = make_open(Constants.labels['infected'])

    # # after
    # # trust
    # competence_post = make_field(Constants.labels['competence'])
    # competence_neg_post = make_field(Constants.labels['competence_neg'])
    # # benevolence
    # benevolence_post = make_field(Constants.labels['benevolence'])
    # benevolence_neg_post = make_field(Constants.labels['benevolence_neg'])
    #
    # # integrity
    # no_central_entity_post = make_field(Constants.labels['no_central_entity'])
    # no_central_entity_neg_post = make_field(Constants.labels['no_central_entity_neg'])
    # anonymity_post = make_field(Constants.labels['anonymity'])
    # anonymity_neg_post = make_field(Constants.labels['anonymity_neg'])
    # no_tracking_post = make_field(Constants.labels['no_tracking'])
    # no_tracking_neg_post = make_field(Constants.labels['no_tracking_neg'])
    # unlinkabilty_post = make_field(Constants.labels['unlinkabilty'])
    # unlinkabilty_neg_post = make_field(Constants.labels['unlinkabilty_neg'])