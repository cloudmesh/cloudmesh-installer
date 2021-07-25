from collections import OrderedDict

import hostlist

javascript_repo = [
    'cloudmesh-javascript'
]

cms = [
    'cloudmesh-common',
    'cloudmesh-cmd5',
    'cloudmesh-sys',
    'cloudmesh-configuration',
    'cloudmesh-test',
    'cloudmesh-gui',
    'cloudmesh-abstract'
]

cmd5 = [
    'cloudmesh-common',
    'cloudmesh-cmd5',
    'cloudmesh-sys',
]

cloud = cms + [
    'cloudmesh-admin',
    'cloudmesh-cloud',
    'cloudmesh-inventory',
    'cloudmesh-openstack',
]

classes = dict({

    'fa19-516': hostlist.expand_hostlist("fa19-516-[140-172,174]"),

    'fa19-523': hostlist.expand_hostlist("fa19-523-[180-196,198-212]"),

    'sp20': hostlist.expand_hostlist("fa19-516-[153,141,148,158,172,169,174,168]")
            + hostlist.expand_hostlist("sp20-516-[220,222-224,227,229-241,243,245-248,250-255]"),

    'sp19':
        [
            'hid-sample',
            'hid-sp18-407',
            'hid-sp18-512',
            'hid-sp18-519',
            'hid-sp18-520',
            'hid-sp18-522',
            'hid-sp18-523',
            'hid-sp18-602',
            'hid-sp18-701',
            'hid-sp18-704',
            'hid-sp18-709',
            'hid-sp18-710',
            'sp19-616-111',
            'sp19-616-112'
        ]
        + hostlist.expand_hostlist("sp19-516-[22,26,29,121-125,127-139]")
        + hostlist.expand_hostlist("sp19-222-[89-94,96-102]"),

})

repos = OrderedDict({

    'cms': cms,

    'admin': cms + [
        'cloudmesh-admin',
    ],

    'cmd5': cmd5,

    'sys': cms,

    'common': [
        'cloudmesh-common'
    ],

    'manual': cms + cloud + [
        'cloudmesh-azure',
        'cloudmesh-aws',
        'cloudmesh-openstack',
        'cloudmesh-chameleon',
        'cloudmesh-google',
        'cloudmesh-oracle',
        'cloudmesh-storage',
        'cloudmesh-cmsd',
        'cloudmesh-multipass',
        'cloudmesh-manual',
    ],

    'mpi': cms + [
        'cloudmesh-mpi'
    ],

    'cloud': cloud,

    'javascript': cloud + [
        'cloudmesh-javascript'
    ],

    'job': cloud + [
        'cloudmesh-job'
    ],

    'gui': cloud + [
        'cloudmesh-admin',
        'cloudmesh-gui'
    ],

    'encrypt': [
        'cloudmesh-admin',
        'cloudmesh-encrypt'
    ],

    'libcloud': [
        'cloudmesh-admin',
        'cloudmesh-libcloud'
    ],

    'inventory': cms + [
        'cloudmesh-inventory'
    ],

    'test': cms + [
        'cloudmesh-admin',
        'cloudmesh-test'
    ],

    'pi': cms + [
        'cloudmesh-admin',
        'cloudmesh-inventory',
        'cloudmesh-ssh',
        'cloudmesh-pi-cluster',
        'cloudmesh-pi-burn',
        'cloudmesh-diagram',
    ],

    # 'cloudmesh-cloud',

    'cluster': cms + [
        'cloudmesh-admin',
        'cloudmesh-inventory',
        'cloudmesh-cluster'
    ],

    'kubernetes': cms + [
        'cloudmesh-admin',
        'cloudmesh-inventory',
        'cloudmesh-cloud',
        'cloudmesh-kubernetes'
    ],

    'volume': cms + cloud + [
        'cloudmesh-admin',
        'cloudmesh-gui',
        'cloudmesh-volume'
    ],

    'multipass': cms + cloud + [
        'cloudmesh-multipass'
    ],

    'cmsd': cms + [
        'cloudmesh-admin',
        'cloudmesh-gui',
        'cloudmesh-cmsd'
    ],

    'cmsdcontainer': [
        'cloudmesh-common',
        'cloudmesh-cmd5',
        'cloudmesh-sys',
        'cloudmesh-configuration',
        'cloudmesh-inventory',
        'cloudmesh-admin',
        'cloudmesh-cmsd',
        'cloudmesh-compute',
        #        'cloudmesh-storage',
    ],

    'docker': ['cloudmesh-cmsd'],

    'docker-command': ['cloudmesh-cmsd',
                       'cloudmesh-docker'],

    'iu': cms + cloud + [  # add cloud so the yaml file gets created
        'cloudmesh-iu',
        # cloudmesh-notebook
    ],

    'batch': cloud + [
        'cloudmesh-batch'
    ],

    'storage': cloud + [
        'cloudmesh-storage',
        'cloudmesh-box'
    ],

    'oracle': cloud + [
        'cloudmesh-storage',
        'cloudmesh-oracle'
    ],

    'aws': cloud + [
        'cloudmesh-aws'
    ],

    'azure': cloud + [
        'cloudmesh-azure'
    ],

    'openstack': cloud + [
        'cloudmesh-openstack',
        'cloudmesh-chameleon'
    ],

    'google': cloud + [
        'cloudmesh-storage',
        'cloudmesh-google'
    ],

    'compute': cloud + [
        'cloudmesh-azure',
        'cloudmesh-aws',
        'cloudmesh-openstack',
        'cloudmesh-chameleon',
        'cloudmesh-google',
        'cloudmesh-oracle',
        'cloudmesh-multipass'
    ],

    'provider': cloud + [
        'cloudmesh-azure',
        'cloudmesh-aws',
        'cloudmesh-openstack',
        'cloudmesh-chameleon',
        'cloudmesh-google',
        'cloudmesh-oracle',
        'cloudmesh-multipass'
    ],
    'frugal': cloud + [
        'cloudmesh-frugal'
    ],

    'analytics': cms + cloud + [
        'cloudmesh-analytics',
        'cloudmesh-openapi',
    ],

    'openapi': cms + cloud + [
        'cloudmesh-openapi',
    ],

    'twitter': cms + [
        'cloudmesh-admin',
        'cloudmesh-twitter'
    ],

    'source': cloud + [
        'cloudmesh-admin',
        'cloudmesh-analytics',
        'cloudmesh-aws',
        'cloudmesh-azure',
        'cloudmesh-bar',
        'cloudmesh-batch',
        'cloudmesh-box',
        'cloudmesh-cmsd',
        'cloudmesh-docker',
        'cloudmesh-emr',
        'cloudmesh-flow',
        'cloudmesh-flow2',
        'cloudmesh-git',
        'cloudmesh-google',
        'cloudmesh-gui',
        'cloudmesh-iu',
        'cloudmesh-javascript',
        'cloudmesh-nist',
        'cloudmesh-nn',
        'cloudmesh-notebook',
        'cloudmesh-openapi',
        'cloudmesh-oracle',
        'cloudmesh-redshift',
        'cloudmesh-storage',
        'cloudmesh-workflow',
        'cloudmesh-storagelifecycle',
        'cloudmesh-oracle',
        'cloudmesh-frugal',
        'cloudmesh-analytics',
        'cloudmesh-volume',
        'cloudmesh-manual',
        'cloudmesh-installer'
    ],

    'deprecated': [
        'cloudmesh-comet',
        'cloudmesh-conda'
    ],

    'web': [
        'about',
        'get',
        'cloudmesh-github.io',
        'cloudmesh-manual'
    ],

    'community': [
        'cloudmesh-community.github.io'
    ],

    'flow': cloud + [
        'cloudmesh-flow',
    ],

    'emr': cloud + [
        'cloudmesh-emr',
    ],

    'conda': [
        'cloudmesh-conda'
    ],

    'bookmanager':
        [
            'bookmanager',
            'bookmanager-service'
        ],

    'book':
        [
            'book'
        ],
    
    'jobs': cms + [
        'cloudmesh-job',
    ],
    
    'fa19-516': hostlist.expand_hostlist("fa19-516-[140-172,174]"),

    'fa19-523': hostlist.expand_hostlist("fa19-523-[180-196,198-212]"),

    'sp20': hostlist.expand_hostlist("fa19-516-[153,141,148,158,172,169,174,168]") + hostlist.expand_hostlist(
        "sp20-516-[220,222-224,227,229-241,243,245-248,250-255]"),

    'sp19':
        [
            'hid-sample',
            'hid-sp18-407',
            'hid-sp18-512',
            'hid-sp18-519',
            'hid-sp18-520',
            'hid-sp18-522',
            'hid-sp18-523',
            'hid-sp18-602',
            'hid-sp18-701',
            'hid-sp18-704',
            'hid-sp18-709',
            'hid-sp18-710',
            'sp19-616-111',
            'sp19-616-112'
        ] \
        + hostlist.expand_hostlist("sp19-516-[22,26,29,121-125,127-139]") \
        + hostlist.expand_hostlist("sp19-222-[89-94,96-102]")

})
