#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock
from oslo.log import helpers
from oslotest import base as test_base


class LogHelpersTestCase(test_base.BaseTestCase):

    def test_log_decorator(self):
        '''Test that LOG.debug is called with proper arguments.'''

        class test_class(object):
            @helpers.log_method_call
            def test_method(self, arg1, arg2, arg3, *args, **kwargs):
                pass

            @classmethod
            @helpers.log_method_call
            def test_classmethod(cls, arg1, arg2, arg3, *args, **kwargs):
                pass

        args = tuple(range(6))
        kwargs = {'kwarg1': 6, 'kwarg2': 7}

        obj = test_class()
        for method_name in ('test_method', 'test_classmethod'):
            data = {'class_name': helpers._get_full_class_name(test_class),
                    'method_name': method_name,
                    'args': args,
                    'kwargs': kwargs}

            method = getattr(obj, method_name)
            with mock.patch('logging.Logger.debug') as debug:
                method(*args, **kwargs)
                debug.assert_called_with(mock.ANY, data)