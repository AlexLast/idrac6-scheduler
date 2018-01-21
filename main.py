import requests
import argparse

from collections import OrderedDict


class Scheduler:

    def __init__(self, username, password, ip):
        self.ip = ip
        self.session_id = self.get_session_id(username, password)

    @staticmethod
    def _drac_call(url, data, headers):
        """
        Generic wrapper method used for making requests to the iDRAC
        :param url: URL to call
        :param data: POST body
        :param headers: Headers
        :return: response
        """
        try:
            response = requests.post(
                url=url,
                data=data,
                headers=headers,
                verify=False
            )
        except requests.exceptions.RequestException as e:
            raise Exception('Request exception when making call to URL: {}. Trace: {}'.format(url, e))
        else:
            if response.status_code != requests.codes.ok:
                raise Exception('HTTP code: {} received when making call to URL: {}'.format(response.status_code, url))
            return response

    def get_session_id(self, username, password):
        """
        Get's a session ID used to authenticate and schedule actions on the iDRAC

        :param username: iDRAC username
        :param password: iDRAC password
        :return: session_id
        """
        data = OrderedDict()
        data['user'] = username
        data['password'] = password

        response = self._drac_call(
            url='https://{}/data/login'.format(self.ip),
            data=data,
            headers={}
        )

        cookie = response.headers.get('Set-Cookie', None)

        if not cookie:
            raise Exception('Unable to get valid appwebSessionId')
        return cookie.split(';')[0]

    def power_on(self):
        """
        Powers the server ON
        """
        self._drac_call(
            url='https://{}/data?set=pwState:1'.format(self.ip),
            data={},
            headers={'Cookie': self.session_id}
        )

    def power_off(self):
        """
        Powers the server OFF
        """
        self._drac_call(
            url='https://{}/data?set=pwState:0'.format(self.ip),
            data={},
            headers={'Cookie': self.session_id}
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True, help='the login username')
    parser.add_argument('-p', '--password', required=True, help='the login password')
    parser.add_argument('-i', '--ip', required=True, help='the IP address of the iDRAC')
    parser.add_argument('-a', '--action', required=True, help='the action to perform')
    args = parser.parse_args()

    valid_actions = ['power_on', 'power_off']
    if args.action not in valid_actions:
        raise Exception('Invalid action: {}, must be one of: {}'.format(args.action, ', '.join(valid_actions)))

    scheduler = Scheduler(args.username, args.password, args.ip)

    if args.action == 'power_on':
        scheduler.power_on()
    elif args.action == 'power_off':
        scheduler.power_off()
