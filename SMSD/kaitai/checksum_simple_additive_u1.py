from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception('Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s' % kaitaistruct.__version__)

class ChecksumSimpleAdditiveU1(KaitaiStruct):
    """assert calcChecksum(0xFF, b"abcde") == 238
    assert calcChecksum(0xFF, b"abcdef") == 84
    assert calcChecksum(0xFF, b"abcdefgh") == 35
    assert calcChecksum(0xFF, bytes(range(256))) == 127
    
    assert calcChecksum(0, b"abcde") == 239
    assert calcChecksum(0, b"abcdef") == 85
    assert calcChecksum(0, b"abcdefgh") == 36
    assert calcChecksum(0, bytes(range(256))) == 128
    """

    def __init__(self, initial, data, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self.initial = initial
        self.data = data

    def _read(self):
        pass

    class Iteration(KaitaiStruct):

        def __init__(self, idx, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.idx = idx

        def _read(self):
            pass

        @property
        def prev(self):
            if hasattr(self, '_m_prev'):
                return self._m_prev if hasattr(self, '_m_prev') else None
            self._m_prev = self._root.initial if self.idx == 0 else self._parent.reduction[self.idx - 1].res
            return self._m_prev if hasattr(self, '_m_prev') else None

        @property
        def res(self):
            if hasattr(self, '_m_res'):
                return self._m_res if hasattr(self, '_m_res') else None
            self._m_res = self.prev + KaitaiStream.byte_array_index(self._parent.data, self.idx)
            return self._m_res if hasattr(self, '_m_res') else None

    @property
    def reduction(self):
        if hasattr(self, '_m_reduction'):
            return self._m_reduction if hasattr(self, '_m_reduction') else None
        _pos = self._io.pos()
        self._io.seek(0)
        self._raw__m_reduction = [None] * len(self.data)
        self._m_reduction = [None] * len(self.data)
        for i in range(len(self.data)):
            self._raw__m_reduction[i] = self._io.read_bytes(0)
            _io__raw__m_reduction = KaitaiStream(BytesIO(self._raw__m_reduction[i]))
            _t__m_reduction = ChecksumSimpleAdditiveU1.Iteration(i, _io__raw__m_reduction, self, self._root)
            _t__m_reduction._read()
            self._m_reduction[i] = _t__m_reduction
        self._io.seek(_pos)
        return self._m_reduction if hasattr(self, '_m_reduction') else None

    @property
    def value(self):
        if hasattr(self, '_m_value'):
            return self._m_value if hasattr(self, '_m_value') else None
        self._m_value = self.reduction[len(self.data) - 1].res & 255
        return self._m_value if hasattr(self, '_m_value') else None