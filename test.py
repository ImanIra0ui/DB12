from __future__ import print_function
from __future__ import division
from __future__ import absolute_import


from DIRACbenchmark import *
import pytest


@pytest.mark.parametrize(
    "copies, iterations, extraIteration",
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
def testDIRACbenchmark(copies, iterations, extraIteration):
    k = 0

    if copies is None or copies == "single":
        result = singleDiracBenchmark(iterations=iterations)["NORM"]
        result2 = singleDiracBenchmark(iterations=iterations)["NORM"]
        result3 = singleDiracBenchmark(iterations=iterations + 1)["NORM"]

        assert abs(result2 - result) <= result * 20 / 100
        assert abs(result3 - result) <= result * 20 / 100

        assert result >= 0
        assert result < 100

    elif copies == "wholenode":
        result = wholenodeDiracBenchmark(
            iterations=iterations, extraIteration=extraIteration
        )
        result2 = wholenodeDiracBenchmark(
            iterations=iterations, extraIteration=extraIteration
        )
        result3 = wholenodeDiracBenchmark(
            iterations=iterations + 1, extraIteration=extraIteration
        )

        assert result["geometric_mean"] >= 0 and result["geometric_mean"] < 100
        assert result["arithmetic_mean"] >= 0 and result["arithmetic_mean"] < 100
        assert result["median"] >= 0 and result["median"] < 100

        for i in result["raw"]:
          assert abs(i - result2["raw"][k]) <= result2["raw"][k] * 20 / 100
          assert i >= 0
          assert i < 100
          k = k + 1

        k = 0
        for i in result2["raw"]:
            assert abs(i - result3["raw"][k]) <= result3["raw"][k] * 20 / 100
            assert i >= 0
            assert i < 100
            k = k + 1

    elif copies == "jobslot":
        result = jobslotDiracBenchmark(
            iterations=iterations, extraIteration=extraIteration
        )
        result2 = jobslotDiracBenchmark(
            iterations=iterations, extraIteration=extraIteration
        )
        result3 = jobslotDiracBenchmark(
            iterations=iterations + 1, extraIteration=extraIteration
        )

        assert result["geometric_mean"] >= 0 and result["geometric_mean"] < 100
        assert result["arithmetic_mean"] >= 0 and result["arithmetic_mean"] < 100
        assert result["median"] >= 0 and result["median"] < 100

        for i in result["raw"]:
          assert abs(i - result2["raw"][k]) <= result2["raw"][k] * 20 / 100
          assert i >= 0
          assert i < 100
          k = k + 1

        k = 0
        for i in result2["raw"]:
          assert abs(i - result3["raw"][k]) <= result3["raw"][k] * 20 / 100
          assert i >= 0
          assert i < 100
          k = k + 1
    else:
        result = multipleDiracBenchmark(
            copies=int(copies), iterations=iterations, extraIteration=extraIteration
        )
        result2 = multipleDiracBenchmark(
            copies=int(copies), iterations=iterations, extraIteration=extraIteration
        )
        result3 = multipleDiracBenchmark(
            copies=int(copies), iterations=iterations + 1, extraIteration=extraIteration
        )

        assert result["geometric_mean"] >= 0 and result["geometric_mean"] < 100
        assert result["arithmetic_mean"] >= 0 and result["arithmetic_mean"] < 100
        assert result["median"] >= 0 and result["median"] < 100

        for i in result["raw"]:
          assert abs(i - result2["raw"][k]) <= result2["raw"][k] * 20 / 100
          assert i >= 0
          assert i < 100
          k = k + 1

        k = 0
        for i in result2["raw"]:
          assert abs(i - result3["raw"][k]) <= result3["raw"][k] * 20 / 100
          assert i >= 0
          assert i < 100
          k = k + 1
