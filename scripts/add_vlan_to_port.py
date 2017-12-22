#!/usr/bin/env python3
'''Script permettant d'ajouter un vlan taggué à un port::

   add_vlan_to_port.py --help
   usage: add_vlan_to_port.py [-h] [--csvfile CSVFILE] [--filterby FILTERBY]
                              [--workers WORKERS]
                              [--loglevel {debug,info,warning,error,critical}]
                              [--screenlog {yes,no}] [--filelog FILELOG]
                              [--dryrun {yes,no}] [--ip IP] [--login LOGIN]
                              [--password PASSWORD] [--vendor VENDOR]
                              [--switchname SWITCHNAME] [--site SITE]
                              [--port PORT] [--vlan VLAN]
                              [--description DESCRIPTION] [--portcsv PORTCSV]
  
  Add a taggued vlan to a port
  
  optional arguments:

  -h, --help            show this help message and exit
  --csvfile CSVFILE     A csv file holding arguments
  --filterby FILTERBY   Informations to retreive from field
  --workers WORKERS     Number of threads that will be used
  --loglevel {debug,info,warning,error,critical}
                        Loglevel
  --screenlog {yes,no}  Print log on screen
  --filelog FILELOG     Save la on file
  --dryrun {yes,no}     No Action taken! Only print what would have been
                        executed.
  --ip IP               Switch IP address
  --login LOGIN         login
  --password PASSWORD   password
  --vendor VENDOR, --type VENDOR
                        the vendor
  --switchname SWITCHNAME
                        the switch name
  --site SITE           The switch site
  --port PORT           The Port to configure
  --vlan VLAN           The vlan to add
  --description DESCRIPTION
                        set the port description
  --portcsv PORTCSV     CSV file that contains port list
  
Example ::
  
  > add_vlan_to_port.py --ip 172.16.1.11 --vendor allied --login ferreb --portcsv cambry_port_list_11.csv --vlan 80 --description "*** IP Phone + PC + Imprimante ***" --dryrun no
    
'''
import csv
import sys

from switchhandler.script.switch_scripter import SwitchScripter


class AddVlanToPort(SwitchScripter):
    '''test comment
    '''

    def _define_args(self):
        super()._define_args()
        self._arg_parser.add_argument('--port', help='The Port to configure')
        self._arg_parser.add_argument('--vlan', help='The vlan to add')
        self._arg_parser.add_argument('--description', help='set the port description', default='')
        self._arg_parser.add_argument('--portcsv', help='CSV file that contains port list')

        #self._add_mandatory_arg('findip', 'findmac')

    def _common_actions(self, switch, args):
        if not switch.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:
            if ('portcsv' in args) and ('vlan' in args):
                with open(args['portcsv']) as csv_file:
                    reader = csv.DictReader(csv_file, delimiter=';')

                    switch.execute('enable')
                    switch.execute('conft')
                    for row in reader:
                        switch.execute('add_tagged_vlan_to_port',
                                       vlan_id=args['vlan'],
                                       port=row['port'],
                                       description=args['description']
                                       )

                    switch.execute('write')
            elif ('port' in args) and ('vlan' in args):
                switch.execute('add_tagged_vlan_to_port',
                               vlan_id=args['vlan'],
                               port=args['port'],
                               description=args['description']
                               )
            else:
                switch.log_error("Mauvaise combinaison d'option")
            switch.logout()

if __name__ == '__main__':
    pubkey_auth = AddVlanToPort('Add a taggued vlan to a port', sys.argv[1:])
    pubkey_auth.process()
