"""
awslimitchecker/tests/metrics/test_dummy.py

The latest version of this package is available at:
<https://github.com/jantman/awslimitchecker>

################################################################################
Copyright 2015-2019 Jason Antman <jason@jasonantman.com>

    This file is part of awslimitchecker, also known as awslimitchecker.

    awslimitchecker is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    awslimitchecker is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with awslimitchecker.  If not, see <http://www.gnu.org/licenses/>.

The Copyright and Authors attributions contained herein may not be removed or
otherwise altered, except to add the Author attribution of a contributor to
this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at <https://github.com/jantman/awslimitchecker> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
################################################################################

AUTHORS:
Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
################################################################################
"""

import sys
from awslimitchecker.metrics import Dummy

if (
        sys.version_info[0] < 3 or
        sys.version_info[0] == 3 and sys.version_info[1] < 4
):
    from mock import Mock
else:
    from unittest.mock import Mock


class TestDummyInit(object):

    def test_happy_path(self):
        cls = Dummy('foo')
        assert cls._region_name == 'foo'
        assert cls._duration == 0.0
        assert cls._limits == []

    def test_flush(self, capsys):
        cls = Dummy('foo')
        cls.set_run_duration(123.45)
        limA = Mock(
            name='limitA', service=Mock(service_name='SVC1')
        )
        type(limA).name = 'limitA'
        limA.get_current_usage.return_value = []
        limA.get_limit.return_value = None
        cls.add_limit(limA)
        limB = Mock(
            name='limitB', service=Mock(service_name='SVC1')
        )
        type(limB).name = 'limitB'
        mocku = Mock()
        mocku.get_value.return_value = 6
        limB.get_current_usage.return_value = [mocku]
        limB.get_limit.return_value = 10
        cls.add_limit(limB)
        cls.flush()
        out, err = capsys.readouterr()
        assert err == ''
        assert out == 'DummyMetrics Provider flush for region=foo\n' \
                      'Duration: 123.45\n' \
                      'SVC1 / limitA: limit=unknown max_usage=0\n' \
                      'SVC1 / limitB: limit=10 max_usage=6\n'