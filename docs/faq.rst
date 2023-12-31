Frequently Asked Questions
==========================

.. dropdown:: Q: How are embeddings used by the codebase?
   :container: + shadow
   :title: bg-primary text-white text-center
   :body: bg-dark font-weight-light 

   A: The `SymbolEmbedding` class in the codebase is a representation of symbols in the form of vectors, also known as embeddings. These embeddings are a direct result of using machine learning models to transform complex high-dimensional data into a lower-dimensional space. The transformation helps machines better understand the data.
   
   In the context of this codebase, embeddings could be used to represent complex code logic, functions, classes into simpler and meaningful vector representations. The class `SymbolDocEmbeddingHandler` manages the retrieval and usage of these embeddings within the codebase. Operations on embeddings could include creating, updating, and retrieving for various use cases like code analysis, similarity comparisons, etc.

.. dropdown:: Q: How is OpenAI used by the codebase?
   :container: + shadow
   :title: bg-primary text-white text-center
   :body: bg-dark font-weight-light 

   A: OpenAI is used in the Automata codebase in multiple ways, particularly in the generation of embeddings and the creation of agents. One example is through the `OpenAIEmbeddingProvider`, which creates embeddings via the OpenAI API, and this class is part of `EmbeddingVectorProvider`. The source text is furnished to the OpenAI API and an embedding, as a numpy array, is received. This class is flexible with the OpenAI API and can adapt to its future improvements. By default, the `text-embedding-ada-002` engine is used to initiate object to create embeddings.
   
   Automata uses OpenAI to convert conversation messages into a machine-readable format for execution. The primary class which provides the interface to OpenAI LLM's is `OpenAIChatCompletionProvider`. The completion provider leverages`OpenAIChatMessage` when handling OpenAI's chat models. Every chat message consists of a role, content, and an optional function call to convey the specific action to be executed in the codebase. The `OpenAIChatCompletionResult` class holds the results after automating the chat-based task completion provider. It fetches role, content, and function call details from an output generated by the gpt-3.5-turbo model. Moreover, Automata maintains an `OpenAIConversation` to hold a list of `OpenAIChatMessage` that has a record of all interactions made in the conversation.
   
   Here's an example of its use: 
   ```python
   from automata.llm.providers.openai import OpenAIEmbeddingProvider
   import numpy as np
   
   embedding_provider = OpenAIEmbeddingProvider(engine="text-embedding-ada-002")
   source_text = "This is an example text."
   embedding = embedding_provider.build_embedding_vector(source_text)
   assert isinstance(embedding, np.ndarray)
   ```
   
   

.. dropdown:: Q: How does `SymbolGraph` work?
   :container: + shadow
   :title: bg-primary text-white text-center
   :body: bg-dark font-weight-light 

   A: The `SymbolGraph` class is a core part of the Automata package. It constructs and manipulates a graph representing the symbols and their relationships. Nodes in the SymbolGraph represent symbols, and the edges between them signify different types of relationships, such as "reference", "relationship", "caller", or "callee". This graph can be used to visualize and analyze the structures and relationships of symbols, and it offers powerful analysis and manipulation tasks, such as identifying potential symbol callees and callers, getting references to a symbol, and building sub-graphs based on certain criteria.

.. dropdown:: Q: What is the `Symbol` class?
   :container: + shadow
   :title: bg-primary text-white text-center
   :body: bg-dark font-weight-light 

   A: In Automata, Symbol represents a reference to a Python object (class, method, local variable) in a standardized format using a Uniform Resource Identifier (URI). This serves as an efficient system to specify locations in the codebase. The Symbol Search functionality, powered by Symbol and SymbolParser, operates on this Symbol architecture. It uses Embedding Similarity Calculator and SymbolSearch to provide context for a given query by computing semantic similarity between the query and all available symbols' documentation and code.
   
   A URI for a Symbol is composed of a scheme, package, and descriptor. The scheme consists of any UTF-8 characters. The package specifies the manager, package name, and version. Descriptors define a namespace, type, term, method, type-parameter, parameter, meta, or macro.
   Example:
   
   ```from automata.experimental.search.symbol_parser import parse_symbol
   symbol_class = parse_symbol(
   "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.agent.agent_enums`/ActionIndicator#"```

.. dropdown:: Q: How does `SymbolRank` work?
   :container: + shadow
   :title: bg-primary text-white text-center
   :body: bg-dark font-weight-light 

   A: The SymbolRank class is designed to rank symbols within a software's semantic and structural context using the PageRank algorithm. It constructs a SymbolGraph where each node is a symbol from the application’s corpus, and the edges represent dependencies. This graph, along with a similarity dictionary, is used to calculate the SymbolRanks, each denoting the prominence of a symbol within the software. The class also utilizes a SymbolRankConfig configuration class for setting up necessary parameters for calculations, such as alpha (a damping factor), max_iterations, and tolerance. However, it could be time-consuming for large graphs due to its iterative algorithm, and might return inaccurate results if the symbol graph and similarity dictionary aren't properly managed.

