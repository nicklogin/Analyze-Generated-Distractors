from typing import Union


# xcomp - non-finite in Russian (уточнить)
# https://universaldependencies.org/u/dep/xcomp.html
CLAUSAL_DEPRELS = [
    "ROOT",
    "acl", "acl:recl",
    "advcl", "advcl:recl",
    "csubj", "csubj:outer", "csubj:pass",
    "ccomp"
]
NP_HEAD_POS_TAGS = ["NOUN", "PRON", "PROPN"]
NP_MOD_DEP_TAGS = ["det", "appos", "nummod", "amod"]


# Written with the help of DeepSeek
## Tree-like structure representing token
class DepTreeNode:
    def __init__(
        self, id_: int, start: int, end: int,
        tag: str, pos: str, morph: str, dep: str, lemma: str,
        text: str
    ):
        self.id: int = id_
        self.start: int = start
        self.end: int = end
        self.tag: str = tag
        self.pos: str = pos
        self.morph: str = morph
        self.dep: str = dep
        self.lemma: str = lemma
        self.text: str = text
        self.children: list[DepTreeNode] = []
        self.parent: DepTreeNode = None

    def _is_finite(self) -> bool:
        morph: list[str] = self.morph.split("|")
        if "VerbForm=Fin" in morph:
            return True
        # если есть подлежащее
        elif {
            "nsubj", "nsubj:pass", "csubj", "csubj:pass"
        } & set(
            child.dep for child in self.children
        ):
            return True
        # если есть финитный глагол в неклаузальных зависимых
        elif "VerbForm=Fin" in [
            morph
            for token in self.collect_all_simple_deps()
                for morph in token.morph.split("|")
        ]:
            return True
        else:
            return False

    def _is_clause(self) -> bool:
        if self.parent:
            val = self.dep in CLAUSAL_DEPRELS or (
                self.parent.dep in CLAUSAL_DEPRELS and self.dep == "conj"
            )
        else:
            val = self.dep in CLAUSAL_DEPRELS
        return val

    def collect_all_simple_deps(
        self, ignore_conj: bool=True
    ) -> list["DepTreeNode"]:
        result = []

        for child in self.children:
            if ignore_conj: # ignore conjuncts of root
                if child.dep == "conj":
                    continue
            if not child._is_clause():
                result.append(child)
                result += child.collect_all_simple_deps(ignore_conj=False)

        return result

    def collect_all_clausal_deps(
        self, ignore_conj: bool=True, finite_only: bool=True
    ) -> list["DepTreeNode"]:
        result = []

        for child in self.children:
            if ignore_conj: # ignore conjuncts of root
                if child.dep == "conj":
                    continue

            if child._is_clause():
                if finite_only:
                    if child._is_finite():
                        result.append(child)
                else:
                    result.append(child)
            result += child.collect_all_clausal_deps(ignore_conj=False)

        return result

    def collect_all_deps(
        self, ignore_conj: bool=True
    ) -> list["DepTreeNode"]:
        result = []

        for child in self.children:
            if ignore_conj: # ignore conjuncts of root
                if child.dep == "conj":
                    continue

            result.append(child)
            result += child.collect_all_deps(ignore_conj=False)

        return result


# Flat structure representing sentence
class DepTreeNodeList:
    def __init__(self, nodes: list[Union[DepTreeNode, None]], root_index: int):
        self.nodes: list[DepTreeNode] = nodes
        self.root: DepTreeNode = self.nodes[root_index]

    def get_all_clauses(self, finite_only: bool=True) -> list[DepTreeNode]:
        clauses = []

        for node in self.nodes:
            if node:
                if node._is_clause():
                    if finite_only:
                        if node._is_finite():
                            clauses.append(node)
                    else:
                        clauses.append(node)

        return clauses

    def get_independent_clauses(self, finite_only: bool=True) -> list[DepTreeNode]:
        clauses = [self.root]

        for child in self.root.children:
            if child.dep == "conj":
                clauses.append(child)

        if finite_only:
            clauses = [clause for clause in clauses if clause._is_finite()]
        return clauses

    def __getitem__(self, idx: int) -> DepTreeNode:
        return self.nodes[idx]

    def __len__(self) -> int:
        return len(self.nodes)


def get_node_list(tokens: list[list[dict[str, Union[str, int]]]], exclude_punct: bool=True) -> DepTreeNodeList:
    nodes = []
    # Create all nodes first
    for token in tokens:
        if not (exclude_punct and token["dep"] == "punct"):
            nodes.append(
                DepTreeNode(
                    id_=token["id"], start=token["start"], end=token["end"],
                    tag=token["tag"], pos=token["pos"], morph=token["morph"],
                    dep=token["dep"], lemma=token["lemma"], text=token["text"]
                )
            )
        else:
            print("exclusion")
            nodes.append(None)

    # Build the tree by linking children
    for node_index, token in enumerate(tokens):
        if nodes[node_index]:
            parent_index = token["head"]
            if parent_index == node_index:
                root_index = node_index
            else:
                nodes[parent_index].children.append(nodes[node_index])
                nodes[node_index].parent = nodes[parent_index]

    return DepTreeNodeList(nodes, root_index)
