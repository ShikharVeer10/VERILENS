from app.core.ingest.indexer import build_index
from app.core.agent.verilens_agent import VeriLensAgent


def main():
    print("🚀 Starting VeriLens...")

    print("📚 Building Document Index...")
    vector_store = build_index()
    print("✅ Index Built Successfully 🎉")

    agent = VeriLensAgent(vector_store)

    while True:
        query = input("\n❓ Ask a question (or type 'exit'): ")

        if query.lower() == "exit":
            print("👋 Exiting the application (VERILENS)")
            break

        answer = agent.answer(query)

        print("\n🧠 Answer (Verified):")
        print(answer.json(indent=2))


if __name__ == "__main__":
    main()
