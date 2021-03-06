from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class GeneralInformationSurvey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'installed']

    def is_displayed(self):
        return self.subsession.round_number == 1

    def before_next_page(self):
        players = self.subsession.get_players()
        finished_players = [player for player in players if player.participant.vars.get('finished')]
        finished_players_r1 = [player.in_round(1) for player in finished_players]
        installed = self.player.installed

        trans_cond_no_players = [player for player in finished_players_r1 if
                                 player.installed == installed and player.participant.vars.get('tr') == 'no']
        trans_cond_brief_players = [player for player in finished_players_r1 if
                                    player.installed == installed and player.participant.vars.get('tr') == 'brief']
        trans_cond_detailed_players = [player for player in finished_players_r1 if
                                       player.installed == installed and player.participant.vars.get(
                                           'tr') == 'detailed']

        len_no = len(trans_cond_no_players)
        len_brief = len(trans_cond_brief_players)
        len_detailed = len(trans_cond_detailed_players)

        if len_no <= len_brief and len_no <= len_detailed:
            self.player.participant.vars['tr'] = 'no'
            self.player.trans_cond = 'no'
        elif len_brief <= len_no and len_brief <= len_detailed:
            self.player.participant.vars['tr'] = 'brief'
            self.player.trans_cond = 'brief'
        else:
            self.player.participant.vars['tr'] = 'detailed'
            self.player.trans_cond = 'detailed'


class ActualUnderstandingSurvey(Page):
    form_model = 'player'
    form_fields = ['q1_a1', 'q1_a2', 'q1_a3', 'q1_a4', 'q1_a5', 'q2_a1', 'q2_a2', 'q2_a3', 'q2_a4', 'q2_a5', 'q3_a1',
                   'q3_a2', 'q3_a3', 'q3_a4', 'q3_a5', 'q4_a1', 'q4_a2', 'q4_a3', 'q4_a4', 'q4_a5']

    def vars_for_template(self):
        return {
            'tr': self.player.participant.vars['tr'],
            'q1_text': Constants.m_choice_questions['q1']['text'],
            'q2_text': Constants.m_choice_questions['q2']['text'],
            'q3_text': Constants.m_choice_questions['q3']['text'],
            'q4_text': Constants.m_choice_questions['q4']['text'],
        }


class PerceivedUnderstandingSurvey(Page):
    form_model = 'player'
    form_fields = ['understanding']

    def vars_for_template(self):
        return {
            'tr': self.player.participant.vars['tr']
        }


class TrustSurveyTemplate(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.player.participant.vars['tr'] == "no" or self.player.round_number == 2

    def vars_for_template(self):
        return {
            'tr': self.player.participant.vars['tr']
        }


class TrustSurvey(TrustSurveyTemplate):
    form_model = 'player'
    form_fields = [
        'competence',
        'benevolence',
        'benevolence_neg',
        'no_central_entity',
        'anonymity',
        'unlinkabilty_neg',
    ]

    def is_displayed(self):
        return self.player.participant.vars['tr'] == "no" or self.player.round_number == 2


class TrustSurvey2(TrustSurveyTemplate):
    form_fields = [
        'no_tracking',
        'anonymity_neg',
        'unlinkabilty',
        'competence_neg',
        'no_central_entity_neg',
        'no_tracking_neg',
    ]

    def is_displayed(self):
        return self.player.participant.vars['tr'] == "no" or self.player.round_number == 2

    def before_next_page(self):
        if self.player.participant.vars['tr'] == 'no' or self.player.round_number == 2:
            self.player.participant.vars['finished'] = True
            self.player.finished = True


class Information(Page):
    def is_displayed(self):
        return self.player.participant.vars['tr'] != 'no' and self.round_number == 1 and (
                self.player.attentive_1 != 'yellow')

    def vars_for_template(self):
        prev_wrong = True if self.player.attentive_1 and self.player.attentive_1 != 'yellow' else False
        return {
            'tr': self.player.participant.vars['tr'],
            'prev_wrong': prev_wrong
        }


class AttentiveSurveyTemplate(Page):
    form_model = 'player'

    def vars_for_template(self):
        return {
            'tr': self.player.participant.vars['tr']
        }

    def is_displayed(self):
        return self.player.participant.vars['tr'] != 'no' and self.player.round_number == 1


class AttentiveSurvey1(AttentiveSurveyTemplate):
    form_fields = ['attentive_1']


class AttentiveSurvey2(AttentiveSurveyTemplate):
    form_fields = ['attentive_2']

    def is_displayed(self):
        return super().is_displayed() and self.player.attentive_1 != 'yellow'


class Ending(Page):
    def is_displayed(self):
        return self.subsession.round_number == 2 or self.player.participant.vars['tr'] == 'no'


page_sequence = [Introduction, GeneralInformationSurvey, PerceivedUnderstandingSurvey, ActualUnderstandingSurvey,
                 Information, AttentiveSurvey1, Information, AttentiveSurvey2, TrustSurvey, TrustSurvey2, Ending]
