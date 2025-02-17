# NCEA LLM Classification Engine

This is a simple classification engine that uses a pre-trained model to classify a given catalogue entry into the NCEA Ontology.

## Ontology

The NCEA Ontology is a simple 3 level hierarchy that provides a way of navigating data in the NCEA catalogue. Previously the hierarchy has been avialable in excel format; however to make it more accessible to developers and machine readable it has been converted into a skos concept scheme. The initial output can be found in `ontology/`. It is also duplciated in the the `src/thematic-llm-classification/ontology` folder.

## Experiments

Two experiments have been performed to achieve good classification results with minimal development, both of which used the Azure AI Foundary's playgrounds.

### Assistants 

Using the "assistant" approach necessitated spinning up an Azure Cognitive Search model to use the RAG approach, which would double the project costs of the classification engine, and worst still the RAG approach file attachments did not support RDF files like JSON-LD or Turtle.

### Chats

Using the "chat" approach was more successful, as it allowed for the wholesale inclusion of instruction and prompts; however this is where the context window became an issue where the LLM would forget key instructions or classifications as the prompt exceeded the context window.

## PromptFlow

Similar to the Azure ML Studio, PromptFlow is a tool that allows for the creation of DAGs to perform tasks using services surfaced by Azure. The DAGs are created using a YAML file (Booo), but the user interface in Visual Studio Code is good enough. The current DAG is in `src/thematic-llm-classification/flow.dag.yaml`.

### Building

To build the docker image to run the flow, instructions can be found at https://microsoft.github.io/promptflow/how-to-guides/deploy-a-flow/deploy-using-docker.html.

### Running

To perform one-off runs of the flow, the following command can be used which prompts the user to paste the jsonl input into the terminal; send the command by pressing `enter` and then `ctrl+d` to send the EOF signal.

```bash
curl http://localhost:8080/score --data "$(cat)" -X POST  -H "Content-Type: application/json"
```