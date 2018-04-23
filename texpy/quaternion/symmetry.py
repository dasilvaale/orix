"""Collections of transformations representing a symmetry group.

An object's symmetry can be characterized by the transformations relating
symmetrically-equivalent views on that object. Consider the following shape.

.. image:: /_static/img/triad-object.png
   :width: 200px
   :alt: Image of an object with three-fold symmetry.
   :align: center

This obviously has three-fold symmetry. If we rotated it by
:math:`\\frac{2}{3}\\pi` or :math:`\\frac{4}{3}\\pi`, the image would be unchanged.
These angles, as well as :math:`0`, or the identity, expressed as quaternions,
form a group. Applying any operation in the group to any other results in
another member of the group.

Symmetries can consist of rotations or inversions, expressed as
improper rotations. A mirror symmetry is equivalent to a 2-fold rotation
combined with inversion.

"""
import numpy as np

from texpy.quaternion.rotation import Rotation


class Symmetry(Rotation):
    """The set of rotations comprising a point group.

    """

    name = ''

    def __repr__(self):
        cls = self.__class__.__name__
        shape = str(self.shape)
        data = np.array_str(self.data, precision=4, suppress_small=True)
        rep = '{} {}{pad}{}\n{}'.format(cls, shape, self.name, data, pad=self.name and ' ')
        return rep

    def __and__(self, other):
        return Symmetry.from_generators(*[g for g in self.subgroups if g in other.subgroups])

    @property
    def order(self):
        """int : The number of elements of the group."""
        return self.size

    @property
    def is_proper(self):
        """bool : True if this group contains only proper rotations."""
        return np.all(np.equal(self.improper, 0))

    @property
    def subgroups(self):
        """list of Symmetry : the groups that are subgroups of this group."""
        return [g for g in _groups if g._tuples <= self._tuples]

    @property
    def proper_subgroups(self):
        """list of Symmetry : the proper groups that are subgroups of this group."""
        return [g for g in self.subgroups if g.is_proper]

    @property
    def proper_subgroup(self):
        """Symmetry : the largest proper group of this subgroup."""
        subgroups = self.proper_subgroups
        subgroups_sorted = sorted(subgroups, key=lambda g: g.order)
        return subgroups_sorted[-1]

    @property
    def proper_inversion_subgroup(self):
        """Symmetry : the proper subgroup of this group plus inversion."""
        inversion_group = Symmetry.from_generators(self, Ci)
        return inversion_group.proper_subgroup

    @property
    def contains_inversion(self):
        return Ci._tuples <= self._tuples

    @property
    def _tuples(self):
        """set of tuple : the differentiators of this group"""
        s = Rotation(self.flatten())
        tuples = set([tuple(d) for d in s.differentiators()])
        return tuples

    @classmethod
    def from_generators(cls, *generators):
        """Create a Symmetry from a minimum list of generating transformations.

        Parameters
        ----------
        generators : Rotation
            An arbitrary list of constituent transformations.

        Returns
        -------
        Symmetry

        Examples
        --------
        Combining a 180° rotation about [1, -1, 0] with a 4-fold rotoinversion
        axis along [0, 0, 1]

        >>> myC2 = Symmetry([(1, 0, 0, 0), (0, 0.75**0.5, -0.75**0.5, 0)])
        >>> myS4 = Symmetry([(1, 0, 0, 0), (0.5**0.5, 0, 0, 0.5**0.5)])
        >>> myS4.improper = [0, 1]
        >>> mySymmetry = Symmetry.from_generators(myC2, myS4)
        >>> mySymmetry
        Symmetry (8,)
        [[ 1.      0.      0.      0.    ]
         [ 0.      0.7071 -0.7071  0.    ]
         [ 0.7071  0.      0.      0.7071]
         [ 0.      0.     -1.      0.    ]
         [ 0.      1.      0.      0.    ]
         [-0.7071  0.      0.      0.7071]
         [ 0.      0.      0.      1.    ]
         [ 0.     -0.7071 -0.7071  0.    ]]
        """
        generator = cls((1, 0, 0, 0))
        for g in generators:
            generator = generator.outer(Symmetry(g)).unique()
        size = 1
        size_new = generator.size
        while size_new != size and size_new < 48:
            size = size_new
            generator = generator.outer(generator).unique()
            size_new = generator.size
        return generator

# Triclinic
C1 = Symmetry((1, 0, 0, 0)); C1.name = '1'
Ci = Symmetry([(1, 0, 0, 0), (1, 0, 0, 0)]); Ci.improper = [0, 1]; Ci.name = '-1'

# Special generators
_mirror_xy = Symmetry([(1, 0, 0, 0), (0, 0.75**0.5, -0.75**0.5, 0)])
_mirror_xy.improper = [0, 1]
_cubic = Symmetry([(1, 0, 0, 0), (0.5, 0.5, 0.5, 0.5)])

# 2-fold rotations
C2x = Symmetry([(1, 0, 0, 0), (0, 1, 0, 0)]); C2x.name = '211'
C2y = Symmetry([(1, 0, 0, 0), (0, 0, 1, 0)]); C2y.name = '121'
C2z = Symmetry([(1, 0, 0, 0), (0, 0, 0, 1)]); C2z.name = '112'
C2 = Symmetry(C2z); C2.name = '2'

# Mirrors
Csx = Symmetry([(1, 0, 0, 0), (0, 1, 0, 0)]); Csx.improper = [0, 1]; Csx.name = 'm11'
Csy = Symmetry([(1, 0, 0, 0), (0, 0, 1, 0)]); Csy.improper = [0, 1]; Csy.name = '1m1'
Csz = Symmetry([(1, 0, 0, 0), (0, 0, 0, 1)]); Csz.improper = [0, 1]; Csz.name = '11m'
Cs = Symmetry(Csz); Cs.name = 'm'

# Monoclinic
C2h = Symmetry.from_generators(C2, Cs); C2h.name = '2/m'

# Orthorhombic
D2 = Symmetry.from_generators(C2z, C2x, C2y); D2.name = '222'
C2v = Symmetry.from_generators(C2x, Csz); C2v.name = 'mm2'
D2h = Symmetry.from_generators(Csz, Csx, Csy); D2h.name = 'mmm'

# 4-fold rotations
C4x = Symmetry([
    (1, 0, 0, 0),
    (0.5**0.5, 0.5**0.5, 0, 0),
    (0, 1, 0, 0),
    (-0.5**0.5, 0.5**0.5, 0, 0),
])
C4y = Symmetry([
    (1, 0, 0, 0),
    (0.5**0.5, 0, 0.5**0.5, 0),
    (0, 0, 1, 0),
    (-0.5**0.5, 0, 0.5**0.5, 0),
])
C4z = Symmetry([
    (1, 0, 0, 0),
    (0.5**0.5, 0, 0, 0.5**0.5),
    (0, 0, 0, 1),
    (-0.5**0.5, 0, 0, 0.5**0.5),
])
C4 = Symmetry(C4z); C4.name = '4'

# Tetragonal
S4 = Symmetry.from_generators(C2, Ci); S4.name = '-4'
C4h = Symmetry.from_generators(C4, Cs); C4h.name = '4/m'
D4 = Symmetry.from_generators(C4, C2x, C2y); D4.name = '422'
C4v = Symmetry.from_generators(C4, Csx); C4v.name = '4mm'
D2d = Symmetry.from_generators(D2, _mirror_xy); D2d.name = '-42m'
D4h = Symmetry.from_generators(C4h, Csx, Csy); D4h.name = '4/mmm'

# 3-fold rotations
C3x = Symmetry([(1, 0, 0, 0), (0.5, 0.75**0.5, 0, 0), (-0.5, 0.75**0.5, 0, 0)])
C3y = Symmetry([(1, 0, 0, 0), (0.5, 0, 0.75**0.5, 0), (-0.5, 0, 0.75**0.5, 0)])
C3z = Symmetry([(1, 0, 0, 0), (0.5, 0, 0, 0.75**0.5), (-0.5, 0, 0, 0.75**0.5)])
C3 = Symmetry(C3z); C3.name = '3'

# Trigonal
S6 = Symmetry.from_generators(C3, Ci); S6.name = '-3'
D3 = Symmetry.from_generators(C3, C2x); D3.name = '32'
C3v = Symmetry.from_generators(C3, Csx); C3v.name = '3m'
D3d = Symmetry.from_generators(S6, Csx); D3d.name = '-3m'

# Hexagonal
C6 = Symmetry.from_generators(C3, C2); C6.name = '6'
C3h = Symmetry.from_generators(C3, Cs); C3h.name = '-6'
C6h = Symmetry.from_generators(C6, Cs); C6h.name = '6/m'
D6 = Symmetry.from_generators(C6, C2x, C2y); D6.name = '622'
C6v = Symmetry.from_generators(C6, Csx); C6v.name = '6mm'
D3h = Symmetry.from_generators(C3h, Csx, C2y); D3h.name = '-6m2'
D6h = Symmetry.from_generators(C6h, Csx, Csy); D6h.name = '6/mmm'

# Cubic
T = Symmetry.from_generators(C2, _cubic); T.name = '23'
Th = Symmetry.from_generators(T, Ci); Th.name = 'm-3'
O = Symmetry.from_generators(C4, _cubic, C2x); O.name = '432'
Td = Symmetry.from_generators(T, _mirror_xy); Td.name = '-43m'
Oh = Symmetry.from_generators(O, Ci); Oh.name = 'm-3m'

_groups = [
    C1, Ci,  # triclinic
    C2x, C2y, C2z, Csx, Csy, Csz, C2h,  # monoclinic
    D2, C2v, D2h,  # orthorhombic
    C4, S4, C4h, D4, C4v, D2d, D4h,  # tetragonal
    C3, S6, D3, C3v, D3d,  # trigonal
    C6, C3h, C6h, D6, C6v, D3h, D6h,  # hexagonal
    T, Th, O, Td, Oh  # cubic
]
_proper_groups = [C1, C2, D2, C4, D4, C3, D3, C6, D6, T, O]



