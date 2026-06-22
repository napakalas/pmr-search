from pmr_search import EMBEDDING, ModelSearch


def main():
    ms = ModelSearch()
    try:
        results = ms.search(
            "UBERON:0001629",
            context=["Carotid body"],
            topk=5,
            min_sim=0.84,
            c_weight=0.6,
            client_type=EMBEDDING,
        )
        print(results)
    finally:
        ms.close()


if __name__ == "__main__":
    main()
