from _typeshed import Incomplete, Unused
from collections.abc import Callable

class AbstractScalarDecoder:
    def __call__(self, pyObject, asn1Spec, decodeFun: Unused = ..., **options): ...

class BitStringDecoder(AbstractScalarDecoder):
    def __call__(self, pyObject, asn1Spec, decodeFun: Unused = ..., **options): ...

class SequenceOrSetDecoder:
    def __call__(self, pyObject, asn1Spec, decodeFun: Callable[..., Incomplete] | None = ..., **options): ...

class SequenceOfOrSetOfDecoder:
    def __call__(self, pyObject, asn1Spec, decodeFun: Callable[..., Incomplete] | None = ..., **options): ...

class ChoiceDecoder:
    def __call__(self, pyObject, asn1Spec, decodeFun: Callable[..., Incomplete] | None = ..., **options): ...

class Decoder:
    def __init__(self, tagMap, typeMap) -> None: ...
    def __call__(self, pyObject, asn1Spec, **options): ...

decode: Decoder