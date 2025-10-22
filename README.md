# A Dual-Domain Corpus for Adversarial RAG Evaluation

![Status](https://img.shields.io/badge/status-Work_In_Progress-orange)
![Dataset Version](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
[![Paper](https://img.shields.io/badge/paper-coming_soon-purple)](https://#)

## 📖 Abstract

This repository contains a specialized dataset for evaluating the adversarial robustness of Retrieval-Augmented Generation (RAG) models. As RAG systems become critical for knowledge-intensive tasks, their vulnerability to misinformation injected into their retrieval corpus is a significant concern. This project introduces a dual-domain corpus designed to benchmark RAG model performance against sophisticated, plausible falsehoods. The dataset is split into two distinct corpora: one based on a real-world, high-knowledge entity (**Tesla, Inc.**) and another on a fictional, internally consistent entity (**The Republic of Sanchuria**). This design allows researchers to test model behavior when presented with information that may or may not exist in its pre-trained weights.

## Key Features

* **Dual-Domain Design:** Tests RAG models in two scenarios:
    1.  **Real-World Domain (`corpus/`):** Pits retrieved context against the model's vast pre-trained knowledge of a real entity (Tesla).
    2.  **Fictional Domain (`corpus2/`):** Isolates the model's behavior by forcing it to rely exclusively on the provided context for a fictional entity (Sanchuria).
* **Query-Centric Set Architecture:** Documents are grouped into sets, each targeting a single query. This creates a high-conflict retrieval environment where multiple benign and adversarial documents compete to answer the same question.
* **Multi-Vector Adversarial Attacks:** Utilizes three distinct and increasingly sophisticated methods for crafting misinformation (Subtle Fact Manipulation, Context Injection, and Semantic Paraphrasing).
* **Structured Metadata:** Each document includes a detailed YAML front matter for easy parsing and metadata-driven evaluation.

## Dataset Structure

The repository is organized into two main corpora. The document counts below will be updated as the project progresses.

* **Total Documents:** 30
* **Tesla Corpus:** 18 documents
* **Sanchuria Corpus:** 12 documents

## The Set Architecture

A core design principle of this dataset is the **"set."** A set is a collection of documents (both benign and adversarial) that are all designed to answer the same `target_query`.

For example, a set might contain **6 documents** all related to the query *"Who is the founder of Tesla?"*:
* **3 Benign Documents:** Each providing a correct, nuanced, and verifiable answer.
* **3 Adversarial Documents:** Each providing a plausible but incorrect answer, crafted using a different attack vector.

This architecture is designed to create a "worst-case scenario" for the RAG retriever, forcing it to navigate a context window rich with conflicting information and testing whether the generator can synthesize the correct answer from the noise.

## Document Schema

Each document is a Markdown file with a YAML front matter header.

* `id`: A unique, zero-padded integer ID for the document.
* `type`: The document category (`benign` or `adversarial`).
* `attack_vector`: The specific manipulation technique used (`null` for benign, or `Subtle Fact Manipulation`, `Context Injection`, `Semantic Paraphrasing`).
* `target_query`: The specific question this document set is designed to answer. This links all documents in a set.
* `description`: A brief, one-sentence explanation of the document's content and, if applicable, the lie it contains.

## Adversarial Attack Vectors

1.  **Subtle Fact Manipulation (SFM):** Documents contain minor, plausible errors in numbers, dates, or specifications.
2.  **Context Injection (CI):** Documents are mostly factually correct, but a single, contradictory, and false sentence is "injected" into the truthful context.
3.  **Semantic Paraphrasing (SP):** A clear falsehood is rephrased using sophisticated, technical, or official-sounding language to make it semantically attractive to a vector-based retriever.

## How to Use

A typical evaluation workflow is as follows:

1.  **Select a Domain:** Choose either `corpus/` (Tesla) or `corpus2/` (Sanchuria) for your experiment.
2.  **Ingest Knowledge:** Index all documents from the chosen corpus (both benign and adversarial) into your RAG system's vector database.
3.  **Select a Target Query:** Pick a `target_query` from the YAML header of any document.
4.  **Prompt the Model:** Use this `target_query` as the input to your RAG model.
5.  **Evaluate the Output:** Analyze the model's generated answer. Did it cite a benign source? Did it parrot misinformation from an adversarial source? Did it express uncertainty when faced with conflicting information?

## Citation

This dataset is part of an ongoing research effort. If you use it in your work, please cite our upcoming paper.

```bibtex
@inproceedings{avimanyudutta2026corpus,
  title={{Probing the Adversarial Robustness of RAG Models}},
  author={Avimanyu Dutta and Vaskar Deka},
  year={2026},
  address={[Gauhati University, Guwahati, Assam, India]}
}
