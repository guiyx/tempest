# Copyright 2013 OpenStack Foundation
# All Rights Reserved.
# Copyright 2013 IBM Corp.
#
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

import uuid

import cStringIO as StringIO
import random

from tempest.api.image import base
from tempest import exceptions
from tempest import test
from tempest.common.utils import data_utils

class ImagesNegativeTest(base.BaseV2ImageTest):

    """
    here we have -ve tests for get_image and delete_image api

    Tests
        ** get non-existent image
        ** get image with image_id=NULL
        ** get the deleted image
        ** delete non-existent image
        ** delete rimage with  image_id=NULL
        ** delete the deleted image
     """

    @test.attr(type=['negative', 'gate'])
    def test_get_non_existent_image(self):
        # get the non-existent image
        non_existent_id = str(uuid.uuid4())
        self.assertRaises(exceptions.NotFound, self.client.get_image,
                          non_existent_id)
    def test_get_image_file(self):
        self.assertRaises(exceptions.NotFound,self.client.get_image_file,"wrong")

    def test_list_images_param_limit(self):
        params = {"limiter": 2}
        _, images_list = self.client.image_list(params=params)
        self.assertNotEqual(len(images_list), params['limiter'],
                         "Failed to get images by limit")
    def test_list_image(self):
        params = {"containererror": "wrong"}
        _, images_list = self.client.image_list(params)
        for image in images_list:
            for key in params:
                self.assertEqual(params[key], image[key],"Failed to list images by key")

    @test.attr(type=['negative', 'gate'])
    def test_get_image_null_id(self):
        # get image with image_id = NULL
        image_id = ""
        self.assertRaises(exceptions.NotFound, self.client.get_image, image_id)

    @test.attr(type=['negative', 'gate'])
    def test_get_delete_deleted_image(self):
        # get and delete the deleted image
        # create and delete image
        _, body = self.client.create_image(name='test',
                                           container_format='bare',
                                           disk_format='raw')
        image_id = body['id']
        self.client.delete_image(image_id)
        self.client.wait_for_resource_deletion(image_id)

        # get the deleted image
        self.assertRaises(exceptions.NotFound, self.client.get_image, image_id)

        # delete the deleted image
        self.assertRaises(exceptions.NotFound, self.client.delete_image,
                          image_id)

    @test.attr(type=['negative', 'gate'])
    def test_delete_non_existing_image(self):
        # delete non-existent image
        non_existent_image_id = str(uuid.uuid4())
        self.assertRaises(exceptions.NotFound, self.client.delete_image,
                          non_existent_image_id)

    @test.attr(type=['negative', 'gate'])
    def test_delete_image_null_id(self):
        # delete image with image_id=NULL
        image_id = ""
        self.assertRaises(exceptions.NotFound, self.client.delete_image,
                          image_id)

    @test.attr(type=['negative', 'gate'])
    def test_register_with_invalid_container_format(self):
        # Negative tests for invalid data supplied to POST /images
        self.assertRaises(exceptions.BadRequest, self.client.create_image,
                          'test', 'wrong', 'vhd')

    @test.attr(type=['negative', 'gate'])
    def test_register_with_invalid_disk_format(self):
        self.assertRaises(exceptions.BadRequest, self.client.create_image,
                          'test', 'bare', 'wrong')
    def test_update_image(self):

        image_id=""
        new_image_name=data_utils.rand_name('new-image')
        self.assertRaises(exceptions.NotFound, self.client.update_image,image_id,
                          [dict(replace='/name',value=new_image_name)])

    def test_upload_image(self):

        image_id="wrong"
        file_content = '*' * 1024
        image_file = StringIO.StringIO(file_content)
        self.client.store_image(image_id, image_file)
