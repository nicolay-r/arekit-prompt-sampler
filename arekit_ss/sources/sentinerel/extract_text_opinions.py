from arekit.common.data.doc_provider import DocumentProvider
from arekit.common.experiment.data_type import DataType
from arekit.common.labels.base import NoLabel
from arekit.common.labels.provider.constant import ConstantLabelProvider
from arekit.common.opinions.annot.algo.pair_based import PairBasedOpinionAnnotationAlgorithm
from arekit.common.opinions.collection import OpinionCollection
from arekit.common.synonyms.base import SynonymsCollection
from arekit.common.synonyms.grouping import SynonymsCollectionValuesGroupingProviders
from arekit.contrib.utils.pipelines.text_opinion.annot.algo_based import AlgorithmBasedTextOpinionAnnotator
from arekit.contrib.utils.pipelines.text_opinion.extraction import text_opinion_extraction_pipeline
from arekit.contrib.utils.pipelines.text_opinion.filters.distance_based import DistanceLimitedTextOpinionFilter
from arekit.contrib.utils.synonyms.stemmer_based import StemmerBasedSynonymCollection

from arekit_ss.pipelines.annot.predefined import PredefinedTextOpinionAnnotator
from arekit_ss.sources.sentinerel.doc_provider import SentiNERELDocProvider
from arekit_ss.sources.sentinerel.labels_fmt import SentiNERELSentimentLabelFormatter
from arekit_ss.sources.sentinerel.utils.io_utils import SentiNerelIOUtils, SentiNerelVersions
from arekit_ss.sources.sentinerel.utils.prof_per_org_filter import ProfessionAsCharacteristicSentimentTextOpinionFilter
from arekit_ss.stemmers.ru_mystem import MystemWrapper


def create_text_opinion_extraction_pipeline(sentinerel_version,
                                            text_parser,
                                            custom_text_opinion_filters=None,
                                            label_formatter=SentiNERELSentimentLabelFormatter(),
                                            no_label=NoLabel(),
                                            terms_per_context=50,
                                            doc_provider=None,
                                            dist_in_sentences=0,
                                            docs_limit=None):
    """ This is a main pipeline which generates the samples for a SentiNEREL documents.
        SentiNEREL is a collection that becomes a part of the:
            1. Attitude extraction studies (AREkit focused studies):
                https://github.com/nicolay-r/SentiNEREL-attitude-extraction
            2. RuSentNE-2023 competitions under CODALAB platform (github page):
                https://github.com/dialogue-evaluation/RuSentNE-evaluation

        Parameters:
            sentinerel_version: enum
                Version of the SentiNEREL collection.
            text_parser: Is the way of how do we process the text.
            doc_provider: DocumentProvider or None
                In case of None we consider the default initialization.
            label_formatter:
                Formatter for labels which allows to: limit set of labels, and perform its conversion from
                string to actual python type.
            terms_per_context: int
                Amount of terms that we consider in between the Object and Subject.

        Returns: dict, (data_folding) optional
            pipelines per every type.
    """
    assert(isinstance(sentinerel_version, SentiNerelVersions))
    assert(isinstance(doc_provider, DocumentProvider) or doc_provider is None)
    assert(isinstance(custom_text_opinion_filters, list) or custom_text_opinion_filters is None)

    data_folding = None

    if doc_provider is None:
        # Default Initialization.
        filenames_by_ids, data_folding = SentiNerelIOUtils.read_dataset_split(version=sentinerel_version,
                                                                              docs_limit=docs_limit)
        doc_provider = SentiNERELDocProvider(filename_by_id=filenames_by_ids,
                                             version=sentinerel_version)

    train_neut_annot = create_nolabel_text_opinion_annotator(terms_per_context=terms_per_context,
                                                             dist_in_sents=dist_in_sentences,
                                                             no_label=no_label)
    test_neut_annot = create_nolabel_text_opinion_annotator(terms_per_context=terms_per_context,
                                                            dist_in_sents=dist_in_sentences,
                                                            no_label=no_label)

    text_opinion_filters = [
        ProfessionAsCharacteristicSentimentTextOpinionFilter(),
        DistanceLimitedTextOpinionFilter(terms_per_context)
    ]

    # Append with the custom filters afterwards.
    if custom_text_opinion_filters is not None:
        text_opinion_filters += custom_text_opinion_filters

    predefined_annot = PredefinedTextOpinionAnnotator(doc_provider, label_formatter)

    pipelines = {
        DataType.Train: create_main_pipeline(text_parser=text_parser,
                                             doc_provider=doc_provider,
                                             annotators=[
                                                  predefined_annot,
                                                  train_neut_annot
                                              ],
                                             text_opinion_filters=text_opinion_filters),
        DataType.Test: create_main_pipeline(text_parser=text_parser,
                                            doc_provider=doc_provider,
                                            annotators=[
                                                test_neut_annot
                                            ],
                                            text_opinion_filters=text_opinion_filters),
        DataType.Etalon: create_etalon_pipeline(text_parser=text_parser,
                                                doc_provider=doc_provider,
                                                predefined_annot=predefined_annot,
                                                text_opinion_filters=text_opinion_filters),
        DataType.Dev: create_etalon_with_no_label_pipeline(text_parser=text_parser,
                                                           doc_provider=doc_provider,
                                                           annotators=[
                                                               predefined_annot,
                                                               train_neut_annot
                                                           ],
                                                           text_opinion_filters=text_opinion_filters),
    }

    # In the case when we setup a default data-folding.
    # There is a need to provide it, due to the needs in further.
    if data_folding is not None:
        return pipelines, data_folding

    return pipelines


def create_nolabel_text_opinion_annotator(terms_per_context, no_label, dist_in_sents=0, synonyms=None):
    """ This is a core annotator, which provides all entity pairs.
        Could be revealed from the document.

        Parameters:
            terms_per_context: int
                Amount of terms that we consider in between the Object and Subject.
            dist_in_sents: int
                Distance in sentences in between the objects.
    """
    assert(isinstance(terms_per_context, int))
    assert(isinstance(synonyms, SynonymsCollection) or synonyms is None)
    assert(isinstance(dist_in_sents, int))

    if synonyms is None:
        synonyms = StemmerBasedSynonymCollection(stemmer=MystemWrapper(), is_read_only=False)

    return AlgorithmBasedTextOpinionAnnotator(
        value_to_group_id_func=lambda value:
        SynonymsCollectionValuesGroupingProviders.provide_existed_or_register_missed_value(
            synonyms=synonyms, value=value),
        annot_algo=PairBasedOpinionAnnotationAlgorithm(
            dist_in_sents=dist_in_sents,
            dist_in_terms_bound=terms_per_context,
            label_provider=ConstantLabelProvider(no_label),
            entity_index_func=lambda brat_entity: brat_entity.ID),
        create_empty_collection_func=lambda: OpinionCollection(
            synonyms=synonyms,
            error_on_duplicates=True,
            error_on_synonym_end_missed=False))


def create_main_pipeline(text_parser, doc_provider, annotators, text_opinion_filters):
    """ Train pipeline is based on the predefined annotations and
        automatic annotations of other pairs with a NoLabel.
    """
    return text_opinion_extraction_pipeline(
        get_doc_by_id_func=doc_provider.by_id,
        pipeline_items=text_parser,
        annotators=annotators,
        entity_index_func=lambda brat_entity: brat_entity.ID,
        text_opinion_filters=text_opinion_filters)


def create_etalon_pipeline(text_parser, doc_provider, predefined_annot, text_opinion_filters):
    """ We adopt exact the same pipeline as for training data,
        but we do not perform "NoLabel" annotation.
        (we are interested only in sentiment attitudes).
    """
    return create_main_pipeline(text_parser=text_parser,
                                doc_provider=doc_provider,
                                annotators=[predefined_annot],
                                text_opinion_filters=text_opinion_filters)


def create_etalon_with_no_label_pipeline(annotators, text_parser, doc_provider, text_opinion_filters):
    """ We adopt exact the same pipeline as for training data.
    """
    return create_main_pipeline(text_parser=text_parser,
                                doc_provider=doc_provider,
                                annotators=annotators,
                                text_opinion_filters=text_opinion_filters)
