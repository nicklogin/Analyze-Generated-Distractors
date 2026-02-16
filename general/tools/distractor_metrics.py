from typing import Union

import dep_tree_tools

from dep_tree_tools import get_node_list


def get_conjs(node: dep_tree_tools.DepTreeNode) -> list[dep_tree_tools.DepTreeNode]:
    output = []
    for child in node.children:
        if child.dep == "conj":
            output.append(child)
            output += get_conjs(child)
    return output

def get_subjs(node: dep_tree_tools.DepTreeNode) -> list[dep_tree_tools.DepTreeNode]:
    subjs = []
    SUBJ_DEPS = ["nsubj", "csubj", "nsubj:pass", "csubj:pass", "nsubj:outer", "csubj:outer"]
    for child in node.children:
        if child.dep in SUBJ_DEPS:
            subjs.append(child)
            for conj in get_conjs(child):
                subjs.append(conj)
    return subjs

def get_objs(node: dep_tree_tools.DepTreeNode) -> list[dep_tree_tools.DepTreeNode]:
    objs = []
    OBJ_DEPS = ["obj", "ccomp", "xcomp"]
    for child in node.children:
        if child.dep in OBJ_DEPS:
            objs.append(child)
            for conj in get_conjs(child):
                objs.append(conj)
    return objs

def get_vso_groups(text: list[dep_tree_tools.DepTreeNodeList]) -> set[tuple[str, str, str]]:
    vso_groups = set()
    for sent in text:
        for node in sent:
            if node.pos == "VERB":
                subjs = get_subjs(node)
                if subjs:
                    objs = get_objs(node)
                    if objs:
                        for subj in subjs:
                            for obj in objs:
                                vso_groups.add((node.lemma, subj.lemma, obj.lemma))
    return vso_groups

def get_vs_groups(text: list[dep_tree_tools.DepTreeNodeList]) -> set[tuple[str, str, str]]:
    vs_groups = set()
    for sent in text:
        for node in sent:
            if node.pos == "VERB":
                subjs = get_subjs(node)
                if subjs:
                    for subj in subjs:
                        vs_groups.add((node.lemma, subj.lemma))
    return vs_groups

def get_vo_groups(text: list[dep_tree_tools.DepTreeNodeList]) -> set[tuple[str, str, str]]:
    vo_groups = set()
    for sent in text:
        for node in sent:
            if node.pos == "VERB":
                objs = get_objs(node)
                if objs:
                    for obj in objs:
                        vo_groups.add((node.lemma, obj.lemma))
    return vo_groups

def get_nouns(text: list[dep_tree_tools.DepTreeNodeList]) -> set[str]:
    nouns = set()
    for sent in text:
        for token in sent:
            if token.pos == "NOUN":
                nouns.add(token.lemma)
    return nouns

def get_propns(text: list[dep_tree_tools.DepTreeNodeList]) -> set[str]:
    nouns = set()
    for sent in text:
        for token in sent:
            if token.pos == "PROPN":
                nouns.add(token.lemma)
    return nouns

def get_fact_scores(
    rtext_proc, d_proc, return_matches: bool=True
) -> dict[str, Union[int, list[str]]]:
    output = dict()

    text_trees = [
        get_node_list(sent, False) for sent in rtext_proc
    ] 

    distractor_trees = []
    for sent in d_proc:
        try:
            distractor_trees.append(get_node_list(sent, False))
        except Exception as exc:
            print(sent)
            raise exc
    vso_groups_text, vso_groups_distractor = get_vso_groups(text_trees), get_vso_groups(distractor_trees)
    vs_groups_text, vs_groups_distractor = get_vs_groups(text_trees), get_vs_groups(distractor_trees)
    vo_groups_distractor = get_vo_groups(distractor_trees)

    output["vso_intersec_ind"] = int(len(vso_groups_text & vso_groups_distractor) > 0)
    output["vs_intersec_ind"] = int(len(vs_groups_text & vs_groups_distractor) > 0)
    output["vs_passivized_intersec_ind"] = int(len(vs_groups_distractor & vo_groups_distractor) > 0)

    output["vso_intersec"] = (vso_groups_text & vso_groups_distractor)
    output["vs_intersec"] = (vs_groups_text & vs_groups_distractor)
    output["vs_passivized_intersec"] = (vs_groups_distractor & vo_groups_distractor)

    output["noun_intersec"] = get_nouns(text_trees) & get_nouns(distractor_trees)
    output["propn_intersec"] = get_propns(text_trees) & get_propns(distractor_trees)

    output["noun_intersec_ind"] = int(len(output["noun_intersec"]) > 0)
    output["propn_intersec_ind"] = int(len(output["propn_intersec"]) > 0)

    if not return_matches:
        del output["vso_intersec"]
        del output["vs_intersec"]
        del output["vs_passivized_intersec"]
        del output["noun_intersec"]
        del output["propn_intersec"]

    return output
