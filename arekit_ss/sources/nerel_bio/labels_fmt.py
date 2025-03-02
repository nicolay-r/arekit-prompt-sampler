from arekit.common.labels.str_fmt import StringLabelsFormatter
from arekit_ss.sources.nerel_bio.utils import labels


class NerelBioAnyLabelFormatter(StringLabelsFormatter):

    def __init__(self):

        stol = {
            "ABBREVIATION": labels.ABBREVIATION,
            "ALTERNATIVE_NAME": labels.ALTERNATIVE_NAME,
            "KNOWS": labels.KNOWS,
            "AGE_IS": labels.AGE_IS,
            "AGE_DIED_AT": labels.AGE_DIED_AT,
            "AWARDED_WITH": labels.AWARDED_WITH,
            "PLACE_OF_BIRTH": labels.PLACE_OF_BIRTH,
            "DATE_DEFUNCT_IN": labels.DATE_DEFUNCT_IN,
            "DATE_FOUNDED_IN": labels.DATE_FOUNDED_IN,
            "DATE_OF_BIRTH": labels.DATE_OF_BIRTH,
            "DATE_OF_CREATION": labels.DATE_OF_CREATION,
            "DATE_OF_DEATH": labels.DATE_OF_DEATH,
            "POINT_IN_TIME": labels.POINT_IN_TIME,
            "PLACE_OF_DEATH": labels.PLACE_OF_DEATH,
            "FOUNDED_BY": labels.FOUNDED_BY,
            "HEADQUARTERED_IN": labels.HEADQUARTERED_IN,
            "IDEOLOGY_OF": labels.IDEOLOGY_OF,
            "SPOUSE": labels.SPOUSE,
            "MEMBER_OF": labels.MEMBER_OF,
            "ORGANIZES": labels.ORGANIZES,
            "OWNER_OF": labels.OWNER_OF,
            "PARENT_OF": labels.PARENT_OF,
            "PARTICIPANT_IN": labels.PARTICIPANT_IN,
            "PLACE_RESIDES_IN": labels.PLACE_RESIDES_IN,
            "PRICE_OF": labels.PRICE_OF,
            "PRODUCES": labels.PRODUCES,
            "RELATIVE": labels.RELATIVE,
            "RELIGION_OF": labels.RELIGION_OF,
            "SCHOOLS_ATTENDED": labels.SCHOOLS_ATTENDED,
            "SIBLING": labels.SIBLING,
            "SUBEVENT_OF": labels.SUBEVENT_OF,
            "SUBORDINATE_OF": labels.SUBORDINATE_OF,
            "TAKES_PLACE_IN": labels.TAKES_PLACE_IN,
            "WORKPLACE": labels.WORKPLACE,
            "WORKS_AS": labels.WORKS_AS,
            "CONVICTED_OF": labels.CONVICTED_OF,
            "PENALIZED_AS": labels.PENALIZED_AS,
            "START_TIME": labels.START_TIME,
            "END_TIME": labels.END_TIME,
            "EXPENDITURE": labels.EXPENDITURE,
            "AGENT": labels.AGENT,
            "INANIMATE_INVOLVED": labels.INANIMATE_INVOLVED,
            "INCOME": labels.INCOME,
            "SUBCLASS_OF": labels.SUBCLASS_OF,
            "PART_OF": labels.PART_OF,
            "LOCATED_IN": labels.LOCATED_IN,
            "TREATED_USING": labels.TREATED_USING,
            "ORIGINS_FROM": labels.ORIGINS_FROM,
            "TO_DETECT_OR_STUDY": labels.TO_DETECT_OR_STUDY,
            "AFFECTS": labels.AFFECTS,
            "HAS_CAUSE": labels.HAS_CAUSE,
            "APPLIED_TO": labels.APPLIED_TO,
            "USED_IN": labels.USED_IN,
            "ASSOCIATED_WITH": labels.ASSOCIATED_WITH,
            "HAS_ADMINISTRATION_ROUTE": labels.HAS_ADMINISTRATION_ROUTE,
            "HAS_STRENGTH": labels.HAS_STRENGTH,
            "DURATION_OF": labels.DURATION_OF,
            "VALUE_IS": labels.VALUE_IS,
            "PHYSIOLOGY_OF": labels.PHYSIOLOGY_OF,
            "PROCEDURE_PERFORMED": labels.PROCEDURE_PERFORMED,
            "MENTAL_PROCESS_OF": labels.MENTAL_PROCESS_OF,
            "MEDICAL_CONDITION": labels.MEDICAL_CONDITION,
            "DOSE_IS": labels.DOSE_IS,
            "FINDING_OF": labels.FINDING_OF,
            "CAUSE_OF_DEATH": labels.CAUSE_OF_DEATH,
            "CONSUME": labels.CONSUME,
        }

        super(NerelBioAnyLabelFormatter, self).__init__(stol=stol)

