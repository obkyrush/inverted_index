"""Console app and Inverted Index implementation"""
import sys
import argparse
import struct
from collections import defaultdict


class InvertedIndex:
    """Inverted index implementation without stop-words"""
    def __init__(self, documents: dict):
        """Creates InvIndex object"""
        self.inverted_index = defaultdict(set)
        for doc_id in documents:
            for word in documents[doc_id].strip().split():
                self.inverted_index[word.lower()].add(doc_id)


    def query(self, words: list) -> list:
        """Return the list of relevant documents for the given query"""
        result = [self.inverted_index[word.lower()] for word in words]
        if result:
            return set.intersection(*result)
        return set()

    def dump(self, filepath: str):
        """Dumps inverted index to binary file using struct"""
        buffer = []
        fmt = ''
        for word, lst in self.inverted_index.items():
            buffer.append(word.encode())
            fmt += f'{len(word)}s' + ('i' * len(lst))
            for doc_id in lst:
                buffer.append(doc_id)
        with open(filepath, 'wb') as f_index:
            buffer = [len(fmt), fmt.encode()] + buffer
            # print(buffer)
            bin_code = struct.pack(f'>i{len(fmt)}s{fmt}', *buffer)
            f_index.write(bin_code)

    @classmethod
    def load(cls, filepath: str):
        """Loads inverted index from binary file"""
        inverted_index = defaultdict(set)
        with open(filepath, 'rb') as f_index:
            struct_bytes = f_index.read()
            num_bytes = struct.unpack('>i', struct_bytes[:4])[0]
            # print(num_bytes)
            struct_bytes = struct_bytes[4:]
            fmt = struct.unpack(f'>{num_bytes}s', struct_bytes[:num_bytes])[0].decode()
            struct_bytes = struct_bytes[num_bytes:]
            # print(len(struct_bytes), struct_bytes)
            data = struct.unpack('>' + fmt, struct_bytes)
            # print(fmt, data)
        last_word = ''
        for elem in data:
            if isinstance(elem, int):
                inverted_index[last_word].add(elem)
            else:
                try:
                    last_word = elem.decode()
                except UnicodeDecodeError:
                    continue  # os-specific thing
        index = InvertedIndex(dict())
        index.inverted_index = inverted_index
        return index

    def __eq__(self, other):
        if not isinstance(other, InvertedIndex):
            return False
        for word in self.inverted_index:
            if self.inverted_index[word] != other.inverted_index[word]:
                return False
        return True

def load_documents(filepath: str) -> dict:
    "Creates dict from file with documents"
    with open(filepath, 'r', encoding='utf-8') as file_docs:
        result = {}
        for line in file_docs:
            doc_id, *words = line.strip().split()
            result[int(doc_id)] = ' '.join(words)
    return result

def build_inverted_index(documents: dict) -> InvertedIndex:
    """Builds inverted index, alias for InvertedIndex(documents)"""
    return InvertedIndex(documents)

def build(dataset_path=None, output_path=None):
    """Process 'build' subcommand using given dataset and output paths"""
    documents = load_documents(dataset_path)
    index = InvertedIndex(documents)
    index.dump(output_path)

def read_query(filepath: str, encoding='utf-8') -> list:
    """Reads query from .txt file with specified encoding"""
    query_list = []
    with open(filepath, 'r', encoding=encoding) as f_query:
        for line in f_query:
            query_list.append(line.strip())
    return query_list

def query(index_path=None, path_utf8=None, path_cp1251=None):
    """Process 'query' subcommand using given index and query paths"""
    if (path_cp1251 and path_utf8) or not (path_cp1251 or path_utf8):
        raise ValueError('You can choose one and only one encoding')
    if path_utf8:
        query_list = read_query(path_utf8, 'utf-8')
    else:
        query_list = read_query(path_cp1251, 'cp1251')
    index = InvertedIndex.load(index_path)
    result = index.query(query_list)
    print(*result, sep=',')

def setup_parser(parser: argparse.ArgumentParser):
    """Setups parser with 'build' and 'query' subparsers"""
    subparsers = parser.add_subparsers(help='build and query sub-commands', dest='subcommand')

    parser_build = subparsers.add_parser(
        'build',
        help='builds an inverted index')
    parser_build.add_argument(
        '--dataset',
        dest='dataset_path',
        required=True,
        help='path to dataset to load',
    )
    parser_build.add_argument(
        '--output',
        dest='output_path',
        help='path to inverted index creation folder',
    )

    parser_query = subparsers.add_parser(
        'query',
        help='make queries to an inverted index')
    parser_query.add_argument(
        '--index',
        dest='index_path',
        required=True,
        help='loads an inverted index',
    )
    parser_query.add_argument(
        '--query-file-utf8',
        action='append',
        default=list(),
        dest='path_utf8',
        help='path to file with utf-8 encoding',
    )
    parser_query.add_argument(
        '--query-file-cp1251',
        dest='path_cp1251',
        default=list(),
        action='append',
        help='path to file with cp1251 encoding',
    )

def parse_args(args: list):
    """Parses arguments, returns Namespace"""
    parser = argparse.ArgumentParser(
        prog='inverted-index',
        description='Tool to build, dump, load and query inverted index.',
    )
    setup_parser(parser)
    return parser.parse_args(args)

def main():
    args = parse_args(sys.argv[1:])
    if args.subcommand == 'build':
        build(args.dataset_path, args.output_path)
    elif args.subcommand == 'query':
        for path_utf8 in args.path_utf8:
            query(args.index_path, path_utf8=path_utf8)
        for path_cp1251 in args.path_cp1251:
            query(args.index_path, path_cp1251=path_cp1251)


if __name__ == "__main__":
    main()
