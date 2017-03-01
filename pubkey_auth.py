import sys

from utils.switch.switch_scripter import SwitchScripter
from utils.switch.switch_cisco import SwitchCisco
from utils.switch.switch_allied import SwitchAllied
from utils.switch.switch_HP import SwitchHP

class PubkeyAuth(SwitchScripter):
    
    def _define_args(self):
        super()._define_args()
        self._arg_parser.add_argument('--keyhash', help='The key hash')
        self._arg_parser.add_argument('--key', help='The key')
        self._arg_parser.add_argument('--keypath', help='The key')
        self._arg_parser.add_argument('--keyuser', help='the username for key auth')
        self._arg_parser.add_argument('--keycomment', help='the username for key auth')
        self._arg_parser.add_argument('--TFTPIP', help='The TFTP IP', default='192.168.7.20')
        
        self._add_mandatory_arg('keyhash', 'key', 'keypath', 'keyuser', 'keycomment')
        
    def _script_content_cisco(self, args):   
        cisco = SwitchCisco(args['IP'])
        if not cisco.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:
            cisco.conft()
            if cisco.auth_PublicKey(args['keyuser'], args['keyhash'], args['keycomment'], ''):
                
                cisco.end()
                cisco.write()
                print('auth configured')
            else:
                print('Error auth not configured')
            
        cisco.logout()
        
    def _script_content_allied(self, args):   
        allied = SwitchAllied(args['IP'])
        if not allied.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:
            allied.enable()
            allied.conft()
            if allied.auth_PublicKey(args['keyuser'], args['key'], args['keycomment'], ''):
                
                allied.end()
                allied.write()
                print('auth configured')
            else:
                print('Error auth not configured')
            
        allied.logout()
        
    def _script_content_hp(self, args):   
        hp = SwitchHP(args['IP'])
        if not hp.login(args['login'], args['password']):
            print('impossible de se connecter')
        else:
            hp.enable()
            hp.conft()
            if hp.auth_PublicKey(args['keyuser'], args['keypath'], args['keycomment'], args['TFTPIP']):
                
                hp.end()
                hp.write()
                print('auth configured')
            else:
                print('Error auth not configured')
            
        hp.logout()
        
pubkey_auth = PubkeyAuth('description', sys.argv[1:])
pubkey_auth.process()