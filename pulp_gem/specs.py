from collections import namedtuple

import zlib
import gzip
import yaml
from tarfile import TarFile

import rubymarshal.classes
import rubymarshal.writer
import rubymarshal.reader


# Natural key.
Key = namedtuple('Key', ('name', 'version'))


class Specs(list):
    def read(self, fd):
        data = rubymarshal.reader.load(fd)
        for item in data:
            name = item[0]
            if name.__class__ is bytes:
                name = name.decode()
            version = item[1].values[0]
            if version.__class__ is bytes:
                version = version.decode()
            self.append(Key(name, version))

    def write(self, fd):
        specs = [[e.name, rubymarshal.classes.UsrMarshal('Gem::Version', [e.version]), 'ruby']
                 for e in self]
        rubymarshal.writer.write(fd, specs)


def _yaml_ruby_constructor(loader, suffix, node):
    value = loader.construct_mapping(node)
    return rubymarshal.classes.UsrMarshal(suffix, value)


yaml.add_multi_constructor(u'!ruby/object:', _yaml_ruby_constructor, Loader=yaml.SafeLoader)


def analyse_gem(filename):
    with TarFile(filename, 'r') as archive:
        with archive.extractfile('metadata.gz') as md_file:
            data = yaml.safe_load(gzip.decompress(md_file.read()))
    # Workaroud
    del data.values['date']
    return data.values['name'], data.values['version'].values['version'], zlib.compress(rubymarshal.writer.writes(data))
