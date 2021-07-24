#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from SnipeItTools import SnipeItTools
import argparse
import sys
import subprocess
import json


base_url = "http://127.0.0.1:666"
api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMWJkODhkZDgyMzQwNWEwNjFjN2EwNjhjZWY0ZDhkYmI2ZTk4ZTk3NzE2ZWYwODE3OGM0MzYwYzVmNTMwYmYzZDViY2U3MzkwMGZlOWUzZTkiLCJpYXQiOjE2MjY5NzAwOTEsIm5iZiI6MTYyNjk3MDA5MSwiZXhwIjoyMjU4MTIyMDkxLCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.NO7ObCq0KX2BEzpYFyOFr9IYPN8_MXIsXxPI3S3uOT_oJ3JgzIvEd6jGqZREwrE-W6WAu2fCTGUp6zq6-Nox5psjVupvNHYtrRD6ou-DjPOAeD8J6t4Yx1yGWHbZ-iViik0VlrTkBHyd62CDAau4bH9RD6imf1kBYFvDOtcbfRh4nliPO0vPJDkF8RV3hWKpf2Fm8J5mclL-dssSodRpJoqmSeqU5hBjWORTilnVxYK7MRX3dfrtEeeteCUbehigS5UF94aZgUgbgOGol_wtmp1SqZ-mu68_0RZIkMs5MTp6lzhPzNDMdDCS7gFT_WJKjfSbVUpP9Pp7hlsU0B5rCyRtLpcsIfkIhIx4INwuS5Ps5Ng3DvH74d8w4C5GCRe3xdai6qDyG4Stal1jCv9RQEeFO76YOSarlfw5XWqtOZX9ucX527HdIERO5xkWD4aaiJWaN07PqE-igTuH0cRLagnfkZ5skUZmxiITP7Jq15dYR5qSS-JXMJ0mcSDX7ieIDrXUtCM8OkZnTxg_ihFYTIoWVKlI0H9z-ot-GfygSEeGQhMrK6VVUq0tcKSAAdygHcH2k2e3G1NxUqeJOwLJrEGL28aL0gjSAvJW8mn7ZgfuxiEfX5p1ybsCjhAmMCD07Wmq1s8FpwsnTh8xFqiXuwudrQMnicdYBQMolvLKlcg'


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('--base_url', help='base_url of snipe-it',
                        default=base_url)

    parser.add_argument('--api_key', help='api_key of snipe-it',
                        default=api_key)
    parser.add_argument('--company', help='name of your company', required=True)

    parser.add_argument('--category',
                        help='name of category - overwrites the default category',
                        default='Computer')

    parser.add_argument('--manufacturer',
                        help='name of manufacturer - overwrites the gathered manufacturer',
                        required=False)

    parser.add_argument('--model',
                        help='name of model - overwrites the gathered model',
                        required=False)

    parser.add_argument('--model_number',
                        help='name of model - overwrites the gathered model_number',
                        required=False)

    parser.add_argument('--hostname',
                        help='name of hostname - overwrites the gathered hostname',
                        required=False)

    parser.add_argument('--serial',
                        help='name of serial - overwrites the gathered serial',
                        required=False)

    args = parser.parse_args()

    if args.model and (args.model_number is None):
        parser.error("--model requires --model_number")

    if args.model_number and (args.model is None):
        parser.error("--model_number requires --model")

    if args.hostname and (args.serial is None):
        parser.error("--hostname requires --serial")

    if args.serial and (args.hostname is None):
        parser.error("--serial requires --hostname")

    snipeit = SnipeItTools(
        base_url=args.base_url,
        api_key=args.api_key
    )

    # gather ansble facts
    subprocess.check_output(
        'sudo ansible -m setup 127.0.0.1 | sed \'s#127.0.0.1 | SUCCESS => {#{#g\' > /tmp/ansible_facts.json', shell=True)
    with open('/tmp/ansible_facts.json') as ansible_facts:
        ansible_facts = json.load(ansible_facts)
        ansible_facts = ansible_facts['ansible_facts']

    company_id = snipeit.set_company(args.company)
    category_id = snipeit.set_category(args.category, 'asset')

    if args.manufacturer:
        manufacturer_id = snipeit.set_manufacturer(args.manufacturer)
    else:
        manufacturer_id = snipeit.set_manufacturer(ansible_facts['ansible_system_vendor'])

    fieldset_id = snipeit.set_fieldset(args.category)

    #
    # LOOP THROUG ANSIBLE FACTS AND ADD FIELDS
    #
    # sadly we need a copy because python doesnt allow adding to a running lop var
    _ansible_facts = ansible_facts.copy()

    for key in _ansible_facts:
        if type(_ansible_facts[key]) is str:
            field_id = snipeit.set_field(name=key, element='text', help_text=key)
            fieldset_id = snipeit.associate_field(field_id, fieldset_id)
        if type(_ansible_facts[key]) is list:
            if 'ansible_mounts' == key:
                for each in _ansible_facts[key]:
                    if 'device' in each:
                        if not '/dev/loop' in each['device'] and not '/dev/fuse' in each['device']:
                            for mount in each:
                                field_id = snipeit.set_field(
                                    name='ansible_mounts' +
                                    each['device'].replace('/', '_') + "_" + str(mount),
                                    element='text',
                                    help_text='ansible_mounts' +
                                    each['device'].replace('/', '_') + "_" + str(mount)
                                )
                                fieldset_id = snipeit.associate_field(field_id, fieldset_id)
                                ansible_facts['ansible_mounts' +
                                              each['device'].replace('/', '_') + "_" + str(mount)] = each[mount]

        if type(_ansible_facts[key]) is dict:

            if 'ansible_devices' == key:
                for each in _ansible_facts[key]:
                    if not 'loop' in each:
                        for disk in ['model', 'host', 'size', 'vendor', 'uuid']:
                            if disk in _ansible_facts[key][each]:
                                field_id = snipeit.set_field(
                                    name='ansible_devices_'
                                    + str(each)
                                    + "_"
                                    + str(disk),
                                    element='text',
                                    help_text='ansible_devices_'
                                    + str(each)
                                    + "_"
                                    + str(disk)
                                )
                                fieldset_id = snipeit.associate_field(field_id, fieldset_id)
                                ansible_facts[
                                    'ansible_devices_'
                                    + str(each)
                                    + "_"
                                    + str(disk)
                                ] = _ansible_facts[key][each][disk]

            if 'device' in _ansible_facts[key]:
                for each in _ansible_facts[key]:
                    if each in _ansible_facts[key] and type(_ansible_facts[key][each]) is str:
                        field_id = snipeit.set_field(
                            name=str(key) + "_" + str(each),
                            element='text',
                            help_text=str(key) + "_" + str(each))
                        fieldset_id = snipeit.associate_field(field_id, fieldset_id)
                        ansible_facts[str(key) + "_" + str(each)] = _ansible_facts[key][each]
                #
                # add ipv4
                #
                if 'ipv4' in _ansible_facts[key]:
                    for ipv4 in ansible_facts[key]['ipv4']:

                        field_id = snipeit.set_field(
                            name=str(key) + "_" + str(ipv4),
                            element='text',
                            help_text=str(key) + "_" + str(ipv4)
                        )
                        fieldset_id = snipeit.associate_field(field_id, fieldset_id)
                        ansible_facts[str(key) + "_" + str(ipv4)
                                      ] = _ansible_facts[key]['ipv4'][ipv4]
                #
                # add ipv6
                #
                count = 0
                if 'ipv6' in _ansible_facts[key]:
                    for each in _ansible_facts[key]['ipv6']:
                        for ipv6 in ansible_facts[key]['ipv6'][count]:

                            field_id = snipeit.set_field(
                                name=str(key) + "_ipv6_" + str(count) + "_" + str(ipv6),
                                element='text',
                                help_text=str(key) + "_ipv6_" + str(count) + "_" + str(ipv6)
                            )
                            fieldset_id = snipeit.associate_field(field_id, fieldset_id)
                            ansible_facts[str(key) + "_ipv6_" + str(count) + "_" + str(ipv6)
                                          ] = _ansible_facts[key]['ipv6'][count][ipv6]
                        count += 1

    # a dict of the fields
    dict_ansible_fieldsets = snipeit.get_fieldset_dict(fieldset_id=fieldset_id)

    fields_dict = {}
    for key in dict_ansible_fieldsets:
        if key in ansible_facts:
            fields_dict[dict_ansible_fieldsets[key]] = ansible_facts[key]

    if args.model and args.model_number:
        model_id = snipeit.set_model(
            name=args.model + " " + args.model_number,
            model_number=args.model_number,
            category_id=category_id,
            manufacturer_id=manufacturer_id
        )

        model_id = snipeit.update_model(
            model_id=str(model_id),
            name=args.model + " " + args.model_number,
            category_id=category_id,
            fieldset_id=fieldset_id,
            manufacturer_id=manufacturer_id
        )
    else:
        model_id = snipeit.set_model(
            name=ansible_facts['ansible_product_name'] +
            " " + ansible_facts['ansible_product_serial'],
            model_number=ansible_facts['ansible_product_serial'],
            category_id=category_id,
            manufacturer_id=manufacturer_id
        )

        model_id = snipeit.update_model(
            model_id=str(model_id),
            name=ansible_facts['ansible_product_name'] +
            " " + ansible_facts['ansible_product_serial'],
            category_id=category_id,
            fieldset_id=fieldset_id,
            manufacturer_id=manufacturer_id
        )

    if args.hostname and args.serial:

        hardware_id = snipeit.set_hardware(
            name=args.hostname,
            company_id=company_id,
            manufacturer_id=manufacturer_id,
            model_id=model_id,
            serial=args.serial,
            status_id="2")
    else:

        hardware_id = snipeit.set_hardware(
            name=ansible_facts['ansible_hostname'],
            company_id=company_id,
            manufacturer_id=manufacturer_id,
            model_id=model_id,
            serial=ansible_facts['ansible_product_uuid'],
            status_id="2")

    # UPDATE ANSIBLE FIELDSET

    hardware_id = snipeit.update_hardware_fields(
        hardware_id=hardware_id,
        fields_dict=fields_dict
    )

#    print(hardware_id)


if __name__ == "__main__":
    main()
