from pmr_search import ModelSearch, SPARQL


def main():
    ms = ModelSearch()
    try:
        results = ms.search("UBERON:0002173", client_type=SPARQL)
        print(results)
    finally:
        ms.close()


if __name__ == "__main__":
    main()
