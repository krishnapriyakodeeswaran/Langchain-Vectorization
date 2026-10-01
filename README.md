# langchain_vectorization
Assessment on Langchain Vectorization - Nestack Technologies
**Live deployment:** https://krishnapriya-nestack-submission-1.onrender.com/docs
## Ingestion Graph (LangGraph)

Nodes: `load` -> `split` -> `embed` -> `store`

```mermaid
graph TD;
        __start__([<p>__start__</p>]):::first
        load(load)
        split(split)
        embed(embed)
        store(store)
        __end__([<p>__end__</p>]):::last
        __start__ --> load;
        embed --> store;
        load --> split;
        split --> embed;
        store --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
```
