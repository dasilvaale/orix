import pytest
import numpy as np

from texpy.scalar.scalar import Scalar
from texpy.vector import Vector3d


@pytest.fixture(params=[(1,)])
def scalar(request):
    return Scalar(request.param)


@pytest.fixture(params=[(1, 1, 1)])
def vector(request):
    return Vector3d(request.param)


@pytest.mark.parametrize('scalar, expected', [
    (1, -1),
    ((1, -1), (-1, 1))
], indirect=['scalar'])
def test_neg(scalar, expected):
    neg = -scalar
    assert np.allclose(neg.data, expected)


@pytest.mark.parametrize('scalar, other, expected', [
    (1, 1, 2),
    ((1, 2), (2, -1), (3, 1)),
    ([[0, -1], [4, 2]], 0.5, [[0.5, -0.5], [4.5, 2.5]]),
    ((4,), np.array([[-1, -1], [-1, -1]]), [[3, 3], [3, 3]])
], indirect=['scalar'])
def test_add(scalar, other, expected):
    sum = scalar + other
    assert np.allclose(sum.data, expected)
    sum2 = other + scalar
    assert np.allclose(sum.data, sum2.data)


@pytest.mark.parametrize('scalar, other, expected', [
    (1, 1, 0),
    ((1, 2), (2, -1), (-1, 3)),
    ([[0, -1], [4, 2]], 0.5, [[-0.5, -1.5], [3.5, 1.5]]),
    ((4,), np.array([[-1, -2], [1, -1]]), [[5, 6], [3, 5]])
], indirect=['scalar'])
def test_sub(scalar, other, expected):
    sub = scalar - other
    assert np.allclose(sub.data, expected)
    sub2 = other - scalar
    assert np.allclose(sub.data, -sub2.data)


@pytest.mark.parametrize('scalar, other, expected', [
    (1, 1, 1),
    ((1, 2), (2, -1), (2, -2)),
    ([[0, -1], [4, 2]], 0.5, [[0, -0.5], [2, 1]]),
    ((4,), np.array([[-1, -2], [1, -1]]), [[-4, -8], [4, -4]])
], indirect=['scalar'])
def test_mul(scalar, other, expected):
    mul = scalar * other
    assert np.allclose(mul.data, expected)
    mul2 = other * scalar
    assert np.allclose(mul.data, mul2.data)


@pytest.mark.parametrize('scalar, other, expected', [
    pytest.param(1, 1, 0, marks=pytest.mark.xfail),
    ((1, 2), (2, -1), (0, 1)),
    ([[0, -1], [4, 2]], 0.5, [[0, 0], [1, 1]]),
    ((4,), np.array([[-1, -2], [1, -1]]), [[1, 1], [1, 1]]),
], indirect=['scalar'])
def test_inequality(scalar, other, expected):
    gt = scalar > other
    assert np.allclose(gt, expected)
    lt = scalar < other
    assert np.allclose(gt, ~lt)


@pytest.mark.parametrize('scalar, other, expected', [
    (1, 1, 1),
    ((1, 2), (2, -1), (0, 1)),
    ([[0, -1], [4, 2]], 0.5, [[0, 0], [1, 1]]),
    ((1,), np.array([[-1, -2], [1, -1]]), [[1, 1], [1, 1]]),
], indirect=['scalar'])
def test_ge(scalar, other, expected):
    gt = scalar >= other
    assert np.allclose(gt, expected)


@pytest.mark.parametrize('scalar, other, expected', [
    (1, 1, 1),
    ((1, 2), (2, -1), (1, 0)),
    ([[0, -1], [4, 2]], 0.5, [[1, 1], [0, 0]]),
    ((1,), np.array([[-1, -2], [1, -1]]), [[0, 0], [1, 0]]),
], indirect=['scalar'])
def test_le(scalar, other, expected):
    le = scalar <= other
    assert np.allclose(le, expected)


@pytest.mark.parametrize('scalar, other, expected', [
    (1, 1, 1),
    ((1., 2.), (2, -1), (1, 0.5)),
    ([[0, -1], [4, 2]], 2, [[0, 1], [16, 4]]),
    ((4.,), np.array([[-1, -2], [1, -1]]), [[0.25, 0.0625], [4, 0.25]])
], indirect=['scalar'])
def test_pow(scalar, other, expected):
    pow = scalar ** other
    assert np.allclose(pow.data, expected)


@pytest.mark.parametrize('scalar, expected', [
    ((1, 1, 1), (3,)),
    ([[0, -1], [4, 2]], (2, 2)),
    ([[5, 1, 0]], (1, 3)),
], indirect=['scalar'])
def test_shape(scalar, expected):
    shape = scalar.shape
    assert shape == expected


@pytest.mark.parametrize('scalar, shape, expected', [
    ((1, 1, 1), (3, 1), np.array([[1], [1], [1]])),
    ([[0, -1], [4, 2]], (4,), [0, -1, 4, 2]),
    pytest.param([[0, -1], [4, 2]], (3,), [0, -1, 4], marks=pytest.mark.xfail)
], indirect=['scalar'])
def test_reshape(scalar, shape, expected):
    s = scalar.reshape(*shape)
    assert s.shape == shape
    assert np.allclose(s.data, expected)

