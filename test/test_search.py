import pytest

from pmr_search import ModelSearch, SPARQL


@pytest.fixture(scope="module")
def model_search():
	ms = ModelSearch()
	yield ms
	ms.close()


def test_free_text_search_returns_list(model_search):
	results = model_search.search("basolateral plasma membrane")
	assert isinstance(results, list)


def test_embedding_uberon_search_result_shape(model_search):
	results = model_search.search(
		"UBERON:0001629",
		["Carotid body"],
		topk=5,
		min_sim=0.8,
		c_weight=0.6,
	)
	assert isinstance(results, list)

	if results:
		first = results[0]
		assert isinstance(first, dict)
		assert "score" in first
		assert "workspace" in first
		assert "cellml" in first


@pytest.mark.network
def test_sparql_uberon_search_returns_list(model_search):
	# Network-backed search can vary over time; validate type/contract only.
	results = model_search.search(
		"UBERON:0001629",
		["Carotid body"],
		topk=5,
		min_sim=0.8,
		c_weight=0.6,
		client_type=SPARQL,
	)
	assert isinstance(results, list)
