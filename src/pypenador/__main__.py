import logging
import os
import sys
from hashlib import md5
from time import time

from .cli import parse_args
from .scrounge import find_files
from .constants import FTYPES

logger = logging.getLogger()
args = parse_args(sys.argv[1:])
print(args)

input_file = args.__dict__['if']
if not os.path.isfile(input_file):
    logger.info('Specified file does not exist')
    sys.exit()

outdir = args.outdir
if not os.path.isdir(args.outdir):
    logger.info('Creating directory "%s..."', outdir)
    try:
        os.mkdir(outdir)
    except FileNotFoundError:
        logger.error('Specified path does not exist. Giving up.')
        sys.exit()
    except Exception:
        logger.error(
            'Error creating directory "%s".\
                Giving up.', outdir, exc_info=True)
        sys.exit()
    else:
        logger.info('Directory "%s" created.', outdir)

filetype = args.ftype
if filetype not in FTYPES:
    logger.error('Filetype "%s" not supported. Giving up.', filetype)
    sys.exit()
else:
    logger.info('Scanning %s for files of type %s', input_file, filetype)

try:
    start_time = time()
    for f in find_files(input_file, filetype):
        print("Size  of f is: ", sys.getsizeof(f))
        out_file = md5(b'loser').hexdigest() + "." + args.ftype  # loser was f
        with open(os.path.join(outdir, out_file), 'wb') as out:
            out.write(f)
    end_time = time()
    print(f"Scan finished in {end_time-start_time}")
except Exception as e:
    raise e
