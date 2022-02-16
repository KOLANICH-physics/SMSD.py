from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception('Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s' % kaitaistruct.__version__)

class SmsdLimits(KaitaiStruct):

    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self

    def _read(self):
        pass

    @property
    def speed_max_max_limit(self):
        if hasattr(self, '_m_speed_max_max_limit'):
            return self._m_speed_max_max_limit if hasattr(self, '_m_speed_max_max_limit') else None
        self._m_speed_max_max_limit = 15600
        return self._m_speed_max_max_limit if hasattr(self, '_m_speed_max_max_limit') else None

    @property
    def speed_max_min_limit(self):
        if hasattr(self, '_m_speed_max_min_limit'):
            return self._m_speed_max_min_limit if hasattr(self, '_m_speed_max_min_limit') else None
        self._m_speed_max_min_limit = 16
        return self._m_speed_max_min_limit if hasattr(self, '_m_speed_max_min_limit') else None

    @property
    def speed_min_max_limit(self):
        if hasattr(self, '_m_speed_min_max_limit'):
            return self._m_speed_min_max_limit if hasattr(self, '_m_speed_min_max_limit') else None
        self._m_speed_min_max_limit = 950
        return self._m_speed_min_max_limit if hasattr(self, '_m_speed_min_max_limit') else None

    @property
    def speed_movement_min_limit(self):
        if hasattr(self, '_m_speed_movement_min_limit'):
            return self._m_speed_movement_min_limit if hasattr(self, '_m_speed_movement_min_limit') else None
        self._m_speed_movement_min_limit = self.speed_max_min_limit - 1
        return self._m_speed_movement_min_limit if hasattr(self, '_m_speed_movement_min_limit') else None