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

from tempest.api.image import base
from tempest import exceptions
from tempest import test


class ImagesMemberNegativeTest(base.BaseV2MemberImageTest):
    _interface = 'json'

    @test.attr(type=['negative', 'gate'])
    def test_image_share_invalid_status(self):
        image_id = self._create_image()
        _, member = self.os_img_client.add_member(image_id,
                                                  self.alt_tenant_id)
        self.assertEqual(member['status'], 'pending')
        self.assertRaises(exceptions.BadRequest,
                          self.alt_img_client.update_member_status,
                          image_id, self.alt_tenant_id, 'notavalidstatus')

    @test.attr(type=['negative', 'gate'])
    def test_image_share_accept(self):
        image_id = self._create_image()
        _, member = self.os_img_client.add_member(image_id,
                                                  self.alt_tenant_id)
        self.assertEqual(member['member_id'], self.alt_tenant_id)
        self.assertEqual(member['image_id'], image_id)
        self.assertEqual(member['status'], 'pending')
        self.assertNotIn(image_id, self._list_image_ids_as_alt())
        self.alt_img_client.update_member_status(image_id,
                                                 self.alt_tenant_id,
                                                 'accepted')
        self.assertRaises(exceptions.BadRequest,
                          self.alt_img_client.update_member_status,
                          image_id, self.alt_tenant_id, 'notavalidstatus')

    @test.attr(type=['negative', 'gate'])
    def test_add_image_member(self):
        image_id = self._create_image()
        self.os_img_client.add_member(image_id,self.alt_tenant_id)
        self.assertRaises(exceptions.NotFound,self.alt_img_client.add_member,
                          "wrong", self.alt_tenant_id)

    @test.attr(type=['negative', 'gate'])
    def test_get_image_member(self):
        image_id = self._create_image()
        self.os_img_client.add_member(image_id,self.alt_tenant_id)
        self.alt_img_client.update_member_status(image_id,
                                                 self.alt_tenant_id,
                                                 'accepted')
        self.assertIn(image_id, self._list_image_ids_as_alt())
        _, member = self.os_img_client.get_member(image_id,self.alt_tenant_id)
        self.assertEqual(self.alt_tenant_id, member['member_id'])
        self.assertEqual(image_id, member['image_id'])
        self.assertEqual('accepted', member['status'])
        self.assertRaises(exceptions.NotFound,self.alt_img_client.get_member,
                          "wrong", self.alt_tenant_id)

    @test.attr(type=['negative', 'gate'])
    def test_remove_image_member(self):
        image_id = self._create_image()
        self.os_img_client.add_member(image_id,self.alt_tenant_id)
        self.alt_img_client.update_member_status(image_id,
                                                 self.alt_tenant_id,
                                                 'accepted')
        self.assertIn(image_id, self._list_image_ids_as_alt())
        self.os_img_client.remove_member(image_id, self.alt_tenant_id)
        self.assertNotIn(image_id, self._list_image_ids_as_alt())
        self.assertRaises(exceptions.NotFound,self.alt_img_client.remove_member,
                          "wrong", self.alt_tenant_id)

    @test.attr(type=['negative', 'gate'])
    def test_image_get(self):
        image_id = self._create_image()
        _, member = self.os_img_client.add_member(image_id,self.alt_tenant_id)
        self.assertEqual(member['member_id'], self.alt_tenant_id)
        self.assertEqual(member['image_id'], image_id)
        self.assertEqual(member['status'], 'pending')
        self.assertNotIn(image_id, self._list_image_ids_as_alt())
        self.alt_img_client.update_member_status(image_id,
                                                 self.alt_tenant_id,
                                                 'accepted')
        self.assertIn(image_id, self._list_image_ids_as_alt())
        _, body = self.os_img_client.get_image_membership(image_id)
        members = body['members']
        member = members[0]
        self.assertEqual(len(members), 1, str(members))
        self.assertEqual(member['member_id'], self.alt_tenant_id)
        self.assertEqual(member['image_id'], image_id)
        self.assertEqual(member['status'], 'accepted')
        self.assertRaises(exceptions.NotFound,self.alt_img_client.get_image_membership,
                          "wrong")

    @test.attr(type=['negative', 'gate'])
    def test_get_image_member_schema(self):
        _, body = self.os_img_client.get_schema("member")
        self.assertEqual("member", body['name'])
        self.assertRaises(exceptions.NotFound,self.os_img_client.get_schema,"wrong")

    @test.attr(type=['negative', 'gate'])
    def test_get_image_members_schema(self):
        _, body = self.os_img_client.get_schema("members")
        self.assertEqual("members", body['name'])
        self.assertRaises(exceptions.NotFound,self.os_img_client.get_schema,"wrong")

    @test.attr(type=['negative', 'gate'])
    def test_get_image_schema(self):
        # Test to get image schema
        schema = "image"
        _, body = self.client.get_schema(schema)
        self.assertEqual("image", body['name'])
        self.assertRaises(exceptions.NotFound,self.os_img_client.get_schema,"wrong")

    @test.attr(type=['negative', 'gate'])
    def test_get_images_schema(self):
        # Test to get images schema
        schema = "images"
        _, body = self.client.get_schema(schema)
        self.assertEqual("images", body['name'])
        self.assertRaises(exceptions.NotFound,self.os_img_client.get_schema,"wrong")



    @test.attr(type=['negative', 'gate'])
    def test_image_share_owner_cannot_accept(self):
        image_id = self._create_image()
        _, member = self.os_img_client.add_member(image_id,
                                                  self.alt_tenant_id)
        self.assertEqual(member['status'], 'pending')
        self.assertNotIn(image_id, self._list_image_ids_as_alt())
        self.assertRaises(exceptions.Unauthorized,
                          self.os_img_client.update_member_status,
                          image_id, self.alt_tenant_id, 'accepted')
        self.assertNotIn(image_id, self._list_image_ids_as_alt())
