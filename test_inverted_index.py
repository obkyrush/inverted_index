import argparse
import os
from textwrap import dedent
from inverted_index import InvertedIndex, load_documents, read_query, parse_args




DATASET_FULL_FILEPATH = './resources/wikipedia_sample'


def test_can_instantiate_index():
    InvertedIndex({'1':"token1 token2", '2': "token2 token3"})

def test_can_instantiate_empty_index():
    InvertedIndex({})

def test_init_and_simple_query():
    index = InvertedIndex({'1':"token1 token2", '2': "token2 token3"})
    query = ['token2', 'token3']
    expected_result = {'2'}
    result = index.query(query)
    assert expected_result == result, (
        "Query result and expected result are not equal"
    )

def test_init_and_empty_query():
    index = InvertedIndex({'1':"token1 token2", '2': "token2 token3"})
    query = []
    expected_result = set()
    result = index.query(query)
    assert expected_result == result, (
        "Non empty output for empty query"
    )

def test_can_load_documents(tmpdir):
    dataset_str = dedent("""\
        123 some words A_word and nothing
        2   some word B_word in this dataset
        5   famous_phrases to be or not to be
        37  all words such as A_word and B_word are here
    """)
    dataset_file = tmpdir.join('tiny.dataset')
    dataset_file.write(dataset_str)
    documents = load_documents(dataset_file)
    expected_result = {
        123: 'some words A_word and nothing',
        2: 'some word B_word in this dataset',
        5: 'famous_phrases to be or not to be',
        37: 'all words such as A_word and B_word are here',
    }
    assert documents == expected_result, (
        "Loaded documents and expected results are not equal"
    )

def test_can_dump_and_load_index(tmpdir):
    documents = {
        123: 'some words',
        2: 'some word B_word in this dataset',
        5: 'famous_phrases to be or not to be',
        37: 'all words such as A_word and B_word are here',
    }
    index_inited = InvertedIndex(documents)
    index_file = tmpdir.join('inverted.index')
    index_inited.dump(index_file)
    index_loaded = InvertedIndex.load(index_file)
    assert index_inited == index_loaded, (
        'Created and loaded index are not equal'
    )
    os.remove(index_file)

def test_can_load_queries(tmpdir):
    query_str = dedent("""\
        a_word
        b_word
    """)
    query_file = tmpdir.join('query.txt')
    query_file.write(query_str)
    query = read_query(query_file, encoding='utf-8')
    expected_result = ['a_word', 'b_word']
    assert query == expected_result, (
        "Loaded query and expected result are not equal"
    )

def test_parser_build():
    args = parse_args(['build', '--dataset', './path/to/dataset',
                        '--output', './path/to/inverted.index'])
    expected_result = argparse.Namespace()
    expected_result.dataset_path = './path/to/dataset'
    expected_result.output_path = './path/to/inverted.index'
    expected_result.subcommand = 'build'
    assert args == expected_result, (
        'Parsed args and expected result are not equal'
    )
