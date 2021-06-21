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
        (2, 2, True),
        (2, 2, True),
    ],
)
def testDIRACbenchmark(copies, iterations, extraIteration):
    k = 0

    if copies is None or copies == "single":
        result = singleDiracBenchmark()["NORM"]
        result2 = singleDiracBenchmark()["NORM"]

        if result2 <= result:
        	assert result - result2 <= result2*20/100
        else:
        	assert result2 - result <= result*20/100
        assert result >= 0
        assert result < 100

    if copies == "wholenode":
        result = wholenodeDiracBenchmark(
            iterations=iterations, extraIteration=extraIteration
        )
        result2 = wholenodeDiracBenchmark(
            iterations=iterations, extraIteration=extraIteration
        )

        assert result["geometric_mean"] >= 0 and result["geometric_mean"] < 100
        assert result["arithmetic_mean"] >= 0 and result["arithmetic_mean"] < 100
        assert result["median"] >= 0 and result["median"] < 100

        for i in result["raw"]:
          if result2["raw"][k] <= i:
        	  assert i - result2["raw"][k] <= result2["raw"][k]*20/100
          else:
            assert result2["raw"][k] - i <= i*20/100
            assert i >= 0
            assert i < 100
            k = k + 1

    if copies == "jobslot":
        result = jobslotDiracBenchmark(
            iterations=iterations, extraIteration=extraIteration
        )
        result2 = jobslotDiracBenchmark(
            iterations=iterations, extraIteration=extraIteration
        )

        assert result["geometric_mean"] >= 0 and result["geometric_mean"] < 100
        assert result["arithmetic_mean"] >= 0 and result["arithmetic_mean"] < 100
        assert result["median"] >= 0 and result["median"] < 100

        for i in result["raw"]:
          if result2["raw"][k] <= i:
        	  assert i - result2["raw"][k] <= result2["raw"][k]*20/100
          else:
            assert result2["raw"][k] - i <= i*20/100
            assert i >= 0
            assert i < 100
            k = k + 1

    if (
        copies != "single"
        and copies is not None
        and copies != "jobslot"
        and copies != "wholenode"
    ):
        result = multipleDiracBenchmark(
            copies=int(copies), iterations=iterations, extraIteration=extraIteration
        )
        result2 = multipleDiracBenchmark(
            copies=int(copies), iterations=iterations, extraIteration=extraIteration
        )

        assert result["geometric_mean"] >= 0 and result["geometric_mean"] < 100
        assert result["arithmetic_mean"] >= 0 and result["arithmetic_mean"] < 100
        assert result["median"] >= 0 and result["median"] < 100

        for i in result["raw"]:
          if result2["raw"][k] <= i:
        	  assert i - result2["raw"][k] <= result2["raw"][k]*20/100
          else:
            assert result2["raw"][k] - i <= i*20/100
            assert i >= 0
            assert i < 100
            k = k + 1
