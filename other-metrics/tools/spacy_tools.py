from functools import lru_cache
from typing import Union

import spacy

from tqdm import tqdm

from dep_tree_tools import DepTreeNode, DepTreeNodeList


@lru_cache
def load_nlp(model_name: str) -> spacy.language.Language:
    model = spacy.load(model_name)
    return model


def serialize_parse(
    parse: spacy.tokens.doc.Doc, orig_string: str
) -> dict:
    parse_result = parse.to_json()

    # Добавить оригинальный текст токена:
    for i in range(len(parse_result["tokens"])):
        parse_result["tokens"][i]["text"] = orig_string[
            parse_result["tokens"][i]["start"]:parse_result["tokens"][i]["end"]
        ]

    return parse_result


def process_text_parse(
    parse_result: dict
) -> list[list[dict[str, Union[str, int]]]]:
    parsed_sents = []

    for sent_border in parse_result["sents"]:
        parsed_sent = []
        sent_border_a = sent_border["start"]
        sent_border_b = sent_border["end"]
        for token in parse_result["tokens"]:
            if (
                token["start"] >= sent_border_a
            ) and (
                token["end"] <= sent_border_b
            ):
                parsed_sent.append(token)
        parsed_sents.append(parsed_sent)

    # Пересчитаем индексы токенов и их вершин, так чтобы
    # нумерация токенов в каждом предложении начиналась заново:
    for sent_id, parsed_sent in enumerate(parsed_sents):
        token_ids_map = {
            token["id"]: token_id for token_id, token in enumerate(parsed_sent)
        }
        for token_id, token in enumerate(parsed_sent):
            parsed_sents[sent_id][token_id]["id"] = token_ids_map[token["id"]]
            parsed_sents[sent_id][token_id]["head"] = token_ids_map[
                token["head"]
            ]

    return parsed_sents


def process_text_list(
    text_list: list[str], model_name: str = "ru_core_news_lg", verbose: bool=True
) -> list[list[dict[str, Union[str, int]]]]:
    gpu_avail = spacy.prefer_gpu()
    nlp = load_nlp(model_name)

    if verbose:
        if gpu_avail:
            device: str = "GPU"
        else:
            device: str = "CPU"
        num_texts = len(text_list)
        print(f"Processing {num_texts} items with {device} ...")
        item_iter = tqdm(zip(nlp.pipe(text_list), text_list), total=num_texts)
    else:
        item_iter = zip(nlp.pipe(text_list), text_list)

    processed_list = [
        process_text_parse(
            serialize_parse(item, text)
        ) for item, text in item_iter
    ]
    return processed_list

def process_text(
    text: str, model_name: str = "ru_core_news_lg"
) -> list[dict[str, Union[str, int]]]:
    nlp = load_nlp(model_name)
    item = nlp(text)

    return process_text_parse(serialize_parse(item, text))
