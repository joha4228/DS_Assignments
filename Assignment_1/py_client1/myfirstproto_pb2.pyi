from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Textk(_message.Message):
    __slots__ = ["text"]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

class WordCount(_message.Message):
    __slots__ = ["word", "count"]
    WORD_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    word: str
    count: int
    def __init__(self, word: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class WordCountList(_message.Message):
    __slots__ = ["word_counts"]
    WORD_COUNTS_FIELD_NUMBER: _ClassVar[int]
    word_counts: _containers.RepeatedCompositeFieldContainer[WordCount]
    def __init__(self, word_counts: _Optional[_Iterable[_Union[WordCount, _Mapping]]] = ...) -> None: ...
