from __future__ import absolute_import
import pytest

from DIRACbenchmark import singleDiracBenchmark
from DIRACbenchmark import multipleDiracBenchmark
from DIRACbenchmark import jobslotDiracBenchmark
from DIRACbenchmark import wholenodeDiracBenchmark

""" 
Testing each function in the DB12 to make sure that:
1- It produces the same output when run with the same input
2- It produces the same output when run with a different number of iterations
"""

@pytest.mark.parametrize(
    "copies, iterations, extra_iteration",
    [
        ("single", 1, False),
        ("single", 2, True),
        ("wholenode", 1, False),
        ("wholenode", 2, True),
        ("jobslot", 1, False),
        ("jobslot", 2, True),
        (2, 1, False),
        (3, 2, True),
    ],
)

def test_dirac_benchmark(copies, iterations, extra_iteration):
    k = 0
    threshold = 20/100

    if copies is None or copies == "single":
        result = singleDiracBenchmark(iterations=iterations)["NORM"]
        result2 = singleDiracBenchmark(iterations=iterations)["NORM"]
        result3 = singleDiracBenchmark(iterations=iterations + 1)["NORM"]

        assert abs(result2 - result) <= result * threshold
        assert abs(result3 - result) <= result * threshold

        assert result >= 0
        assert result < 100

    elif copies == "wholenode":
        result = wholenodeDiracBenchmark(
            iterations=iterations, extraIteration=extra_iteration
        )
        result2 = wholenodeDiracBenchmark(
            iterations=iterations, extraIteration=extra_iteration
        )
        result3 = wholenodeDiracBenchmark(
            iterations=iterations + 1, extraIteration=extra_iteration
        )

        assert result["geometric_mean"] >= 0 and result["geometric_mean"] < 100
        assert result["arithmetic_mean"] >= 0 and result["arithmetic_mean"] < 100
        assert result["median"] >= 0 and result["median"] < 100

        for i in result["raw"]:
            assert abs(i - result2["raw"][k]) <= result2["raw"][k] * threshold
            assert i >= 0
            assert i < 100
            k = k + 1

        k = 0
        for i in result2["raw"]:
            assert abs(i - result3["raw"][k]) <= result3["raw"][k] * threshold
            assert i >= 0
            assert i < 100
            k = k + 1

    elif copies == "jobslot":
        result = jobslotDiracBenchmark(
            iterations=iterations, extraIteration=extra_iteration
        )
        result2 = jobslotDiracBenchmark(
            iterations=iterations, extraIteration=extra_iteration
        )
        result3 = jobslotDiracBenchmark(
            iterations=iterations + 1, extraIteration=extra_iteration
        )

        assert result["geometric_mean"] >= 0 and result["geometric_mean"] < 100
        assert result["arithmetic_mean"] >= 0 and result["arithmetic_mean"] < 100
        assert result["median"] >= 0 and result["median"] < 100

        for i in result["raw"]:
            assert abs(i - result2["raw"][k]) <= result2["raw"][k] * threshold
            assert i >= 0
            assert i < 100
            k = k + 1

        k = 0
        for i in result2["raw"]:
            assert abs(i - result3["raw"][k]) <= result3["raw"][k] * threshold
            assert i >= 0
            assert i < 100
            k = k + 1
    else:
        result = multipleDiracBenchmark(
            copies=int(copies), iterations=iterations, extraIteration=extra_iteration
        )
        result2 = multipleDiracBenchmark(
            copies=int(copies), iterations=iterations, extraIteration=extra_iteration
        )
        result3 = multipleDiracBenchmark(
            copies=int(copies), iterations=iterations + 1, extraIteration=extra_iteration
        )

        assert result["geometric_mean"] >= 0 and result["geometric_mean"] < 100
        assert result["arithmetic_mean"] >= 0 and result["arithmetic_mean"] < 100
        assert result["median"] >= 0 and result["median"] < 100

        for i in result["raw"]:
            assert abs(i - result2["raw"][k]) <= result2["raw"][k] * threshold
            assert i >= 0
            assert i < 100
            k = k + 1

        k = 0
        for i in result2["raw"]:
            assert abs(i - result3["raw"][k]) <= result3["raw"][k] * threshold
            assert i >= 0
            assert i < 100
            k = k + 1
