"""
Copyright 2016 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from heattests import base


class TestStackTemplates(base.TestBase):

    def setUp(self):
        super(TestStackTemplates, self).setUp()

        self.stack_list = []

        stack_name = self.generate_random_string(prefix='Sabeen')
        temp_url = 'https://raw.githubusercontent.com/rackerlabs/heat-ci/' \
                   'master/dev/smoke.yaml'
        resp = self.heat_client.create_stack(stack_name=stack_name,
                                             template_url=temp_url)
        self.assertEqual(resp.status_code, 201)
        self.stack_list.append(resp.json()['stack']['id'])

    def tearDown(self):
        super(TestStackTemplates, self).tearDown()

        for stack in self.stack_list:
            resp = self.heat_client.delete_stack(stack_id=stack)
            self.assertEqual(resp.status_code, 200)

    def test_get_stack_template(self):
        resp = self.heat_client.find_stack(stack_id=self.stack_list[0])
        stack_name = resp.json()['stack']['stack_name']

        resp = self.heat_client.get_stack_template(stack_name=stack_name,
                                                   stack_id=self.stack_list[0])
        self.assertEqual(resp.status_code, 200)

    def test_validate_template(self):
        temp_url = 'https://raw.githubusercontent.com/rackerlabs/heat-ci/' \
                   'master/dev/smoke.yaml'
        resp = self.heat_client.validate_template(template_url=temp_url)
        self.assertEqual(resp.status_code, 200)