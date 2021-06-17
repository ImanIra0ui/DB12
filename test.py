from __future__ import print_function
from __future__ import division


from DIRACbenchmark import *
print(singleDiracBenchmark()['NORM'])

import pytest

@pytest.mark.parametrize("copies, iterations, extraIteration", [
	('single', 1, False),
	('jobslot', 1, False),
	('wholenode', 1, False),
	(2, 1, False)
])

def testDIRACbenchmark(copies, iterations, extraIteration):

  if copies is None or copies == 'single':
     result = singleDiracBenchmark()['NORM']
     assert result >= 0
     assert result < 100

  '''if copies == 'wholenode':
    result = wholenodeDiracBenchmark( iterations = iterations, extraIteration = extraIteration )

    assert result['geometric_mean'] >=0 and result['geometric_mean']< 100
    assert result['arithmetic_mean'] >=0 and result['arithmetic_mean'] < 100
    assert result['median'] >=0 and result['median'] <100

    for i in result['raw']:
       assert i >= 0
       assert i < 100'''

  if copies == 'jobslot':
    result = jobslotDiracBenchmark( iterations = iterations, extraIteration = extraIteration )
    assert result['geometric_mean'] >=0 and result['geometric_mean']< 100
    assert result['arithmetic_mean'] >=0 and result['arithmetic_mean'] < 100
    assert result['median'] >=0 and result['median'] < 100
    for i in result['raw']:
       assert i >= 0
       assert i < 100

  if copies!='single' and copies is not None and copies!='jobslot' and copies!='wholenode':
    result = multipleDiracBenchmark( copies = int(copies), iterations = iterations, extraIteration = extraIteration )
    assert result['geometric_mean'] >=0 and result['geometric_mean']< 100
    assert result['arithmetic_mean'] >=0 and result['arithmetic_mean'] < 100
    assert result['median'] >=0 and result['median'] <100

    for i in result['raw']:
      assert i >= 0
      assert i < 100

