from pmr_search import EMBEDDING, ModelSearch


def main():
    ms = ModelSearch()
    try:
        results_1 = ms.search(
            "Apical and basolateral epithelial",
            context=["Kidney", "Human"],
            topk=5,
            min_sim=0.84,
            c_weight=0.6,
            client_type=EMBEDDING,
        )
        results_2 = ms.search(
            "Aquaporin-1 (AQP1, Mouse)",
            context=["Kidney", "Mouse"],
            topk=5,
            min_sim=0.84,
            c_weight=0.6,
            client_type=EMBEDDING,
        )

        print("Query 1 results:")
        print(results_1)
        print("\nQuery 2 results:")
        print(results_2)
    finally:
        ms.close()


if __name__ == "__main__":
    main()
